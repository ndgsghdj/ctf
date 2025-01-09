from PIL import Image, ImageDraw

def draw_bounding_boxes(image_path, bounding_boxes, output_path):
    """
    Colors the insides of specified bounding boxes black on an image and saves the result.

    Parameters:
        image_path (str): Path to the input image.
        bounding_boxes (list of tuples): List of bounding box coordinates as (xmin, ymin, xmax, ymax).
        output_path (str): Path to save the output image with blacked-out bounding boxes.
    """
    # Open the image
    image = Image.open(image_path).convert("RGB")

    # Create a drawable object
    draw = ImageDraw.Draw(image)

    # Draw each bounding box with black fill
    for bbox in bounding_boxes:
        xmin, ymin, xmax, ymax = bbox
        draw.rectangle([xmin, ymin, xmax, ymax], fill="black")

    # Save the result
    image.save(output_path)
    print(f"Image with blacked-out bounding boxes saved to {output_path}")

# Example usage
if __name__ == "__main__":
    # Path to the input output.
    input_image_path = "output.jpg"

    # List of bounding boxes as (xmin, ymin, xmax, ymax)
    bounding_boxes = [
        (990.378601, 894.657532, 1183.338989, 1073.787476),
        (518.608765, 772.645996, 658.017273, 879.432800),
        (674.031616, 665.213806, 741.563171, 721.650024),
        (620.709351, 711.603394, 718.517822, 800.309082),
        (886.820984, 636.681030, 942.099792, 665.682739),
        (916.067322, 641.718811, 962.313293, 667.656982),
        (391.372894, 844.928467, 609.761353, 1011.927124),
        (869.624939, 622.053711, 921.988525, 659.227844),
        (1008.876160, 674.853271, 1053.830322, 722.989258),
        (861.550354, 587.893616, 896.916626, 617.933472),
    ]

    # Path to save the output image
    output_image_path = "output_with_black_boxes.jpg"

    # Draw blacked-out bounding boxes
    draw_bounding_boxes(input_image_path, bounding_boxes, output_image_path)

