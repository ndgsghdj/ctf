from PIL import Image

def create_blackout_image(input_image_path, output_image_path):
    try:
        # Open the input image to get its size
        with Image.open(input_image_path) as img:
            width, height = img.size

        # Create a black image of the same size
        black_image = Image.new("RGB", (width, height), "black")

        # Save the black image to the specified output path
        black_image.save(output_image_path)

        print(f"Blackout image saved as {output_image_path}")

    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
input_image_path = "output.jpg"  # Replace with your input image path
output_image_path = "output_black_image.jpg"  # Replace with desired output path
create_blackout_image(input_image_path, output_image_path)

