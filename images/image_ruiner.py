import os
from PIL import Image, ImageDraw, ImageFont

def pixel_degrade_png(image_path, output_dir="pixel_degraded_pngs", steps=8, label_size=60):
    """
    Degrades an image in steps and adds a percentage label in the bottom-left corner.

    Parameters:
    - image_path: str, path to the input image (relative to /images)
    - output_dir: str, directory to save degraded images (relative to /images)
    - steps: int, number of degradation steps
    - label_size: int, font size for the percentage label
    """
    os.makedirs(output_dir, exist_ok=True)

    # Remove old images
    for file in os.listdir(output_dir):
        if file.endswith(".png"):
            os.remove(os.path.join(output_dir, file))

    # Load the original image
    img = Image.open(image_path)
    original_size = img.size
    images = []

    for i in range(steps + 1):
        # Calculate scaled size (pixelated effect)
        scale = max(1, int(original_size[0] * (1 - (i / steps) * 0.9)))
        degraded = img.resize((scale, int(scale * original_size[1] / original_size[0]))).resize(original_size)

        # Draw the label
        draw = ImageDraw.Draw(degraded)
        try:
            font = ImageFont.truetype("arial.ttf", label_size)
        except:
            font = ImageFont.load_default()

        label = f"{int((i / steps) * 100)}%"
        text_w, text_h = draw.textbbox((0, 0), label, font=font)[2:]
        margin = 20
        padding_x = 15
        padding_y = 10
        position = (margin, original_size[1] - text_h - margin)

        # Draw semi-transparent background for text
        draw.rectangle(
            [position, (position[0] + text_w + padding_x, position[1] + text_h + padding_y)],
            fill=(0, 0, 0, 150)
        )
        draw.text(
            (position[0] + padding_x//2, position[1] + padding_y//2),
            label,
            font=font,
            fill=(255, 255, 255)
        )

        # Save image with percentage in filename
        filename = f"degraded_{int((i / steps) * 100):03}.png"
        filepath = os.path.join(output_dir, filename)
        degraded.save(filepath)

        # Add path for JS array (include "images/" for GitHub Pages)
        images.append(f"images/{output_dir}/{filename}")

    # Save JS array in /images
    js_path = "image_list.js"
    with open(js_path, "w") as f:
        f.write("const imageList = [\n")
        for path in images:
            f.write(f'  "{path}",\n')
        f.write("];\n\nexport default imageList;\n")

    print(f"Saved {len(images)} images and image_list.js in '{os.path.abspath(os.curdir)}'")

if __name__ == "__main__":
    # Example usage: runs from /images
    pixel_degrade_png(
        image_path="sample.png",  # must exist in /images
        steps=8,
        label_size=160  # change this to make labels bigger or smaller
    )
