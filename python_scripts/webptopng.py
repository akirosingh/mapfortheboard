from PIL import Image, ImageDraw

def create_reverse_teardrop_mask(size):
    """
    Create a reverse teardrop-shaped mask.
    """
    mask = Image.new('L', size, 0)
    draw = ImageDraw.Draw(mask)
    
    ellipse_radius = size[0] // 2
    triangle_height = size[1] // 2

    draw.ellipse([(0, 0), (size[0], size[0])], fill=255)
    draw.polygon([
        (size[0] // 2, ellipse_radius),
        (0, ellipse_radius + triangle_height),
        (size[0], ellipse_radius + triangle_height)
    ], fill=0)

    return mask

def crop_to_reverse_teardrop(image_path, output_path, size=(100, 150)):
    """
    Crop an image to a reverse teardrop shape.
    """
    image = Image.open(image_path).convert("RGBA")
    image = image.resize((size[0], size[0]))  # Resize image to match mask dimensions

    mask = create_reverse_teardrop_mask(size)
    mask = mask.resize(image.size)  # Ensure mask is same size as image

    result = Image.new("RGBA", image.size, (0, 0, 0, 0))
    result.paste(image, (0, 0), mask)

    result.save(output_path)