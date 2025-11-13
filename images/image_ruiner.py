import os
import shutil
from PIL import Image, ImageDraw, ImageFont

def pixel_degrade_png(image_path, output_dir="pixel_degraded_pngs", steps=8, label_size=60, font_path=None):
    """
    Degrades an image in steps and adds a percentage label in the bottom-left corner.

    Parameters:
    - image_path: str, path to the input image (relative to /images)
    - output_dir: str, directory to save degraded images (relative to /images)
    - steps: int, number of degradation steps
    - label_size: int, font size for the percentage label
    - font_path: str, optional path to a .ttf font file
    """
    # Clear old images
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    os.makedirs(output_dir, exist_ok=True)

    # Load the original image
    img = Image.open(image_path)
    original_size = img.size
    images = []

    # Load font
    if font_path is None:
        # Try common system fonts
        possible_fonts = [
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",  # Linux
            "/Library/Fonts/Arial.ttf",                               # macOS
            "C:/Windows/Fonts/arial.ttf"                              # Windows
        ]
        font_path = next((f for f in possible_fonts if os.path.exists(f)), None)
    try:
        font = ImageFont.truetype(font_path, label_size) if font_path else ImageFont.load_default()
    except:
        font = ImageFont.load_default()

    for i in range(steps + 1):
        # Calculate scaled size (pixelated effect)
        scale = max(1, int(original_size[0] * (1 - (i / steps) * 0.9)))
        degraded = img.resize((scale, int(scale * original_size[1] / original_size[0]))).resize(original_size)

        # Draw label
        draw = ImageDraw.Draw(degraded)
        label = f"{int((i / steps) * 100)}%"
        text_w, text_h = draw.textbbox((0, 0), label, font=font)[2:]
        margin = 20
        padding_x = 15
        padding_y = 10
        position = (margin, original_size[1] - text_h - margin)

        # Semi-transparent background
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

        # Add path for JS array (GitHub Pages expects "images/" prefix)
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
        label_size=80,            # change this to make labels bigger/smaller
        font_path=None             # optional: path to .ttf font file
    )
