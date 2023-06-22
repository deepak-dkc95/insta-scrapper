import instaloader
from PIL import Image
import os


def scrape_and_upscale_images(username):
    # Create an instance of Instaloader
    loader = instaloader.Instaloader()

    try:
        # Load the profile using the given username
        profile = instaloader.Profile.from_username(loader.context, username)

        # Create a folder for enhanced images
        enhanced_folder = f"{username}_enhanced"
        os.makedirs(enhanced_folder, exist_ok=True)

        # Track the processed images
        processed_images = set()

        # Iterate over the profile's posts
        for post in profile.get_posts():
            # Download and enhance images
            if not post.is_video:
                # Download the images from the post
                loader.download_post(post, target=username)

                # Get the list of downloaded image files
                image_files = [f for f in os.listdir(username) if f.endswith(".jpg")]

                # Process each image file
                for i, image_file in enumerate(image_files):
                    # Skip processing if the image has already been processed
                    if image_file in processed_images:
                        continue

                    # Generate the enhanced image path
                    image_path = os.path.join(username, image_file)
                    image_name = os.path.splitext(image_file)[0]

                    # Determine the enhanced image name
                    if len(image_files) > 1:
                        enhanced_image_name = f"{image_name}_UTC_{i + 1}_enhanced"
                    else:
                        enhanced_image_name = f"{image_name}_UTC_enhanced"

                    enhanced_image_path = os.path.join(enhanced_folder, f"{enhanced_image_name}.jpg")

                    # Open the image using PIL
                    image = Image.open(image_path)

                    # Upscale the image by 4x
                    width, height = image.size
                    upscaled_image = image.resize((width * 8, height * 8), Image.BICUBIC)

                    # Save the upscaled image
                    upscaled_image.save(enhanced_image_path)

                    # Add the processed image to the set
                    processed_images.add(image_file)

        print("Scraping and up-scaling completed.")
    except instaloader.exceptions.ProfileNotExistsException:
        print("Profile does not exist.")


# Scrape the profile and upscale the images
ig_username = "instagram_username"
scrape_and_upscale_images(ig_username)
