import os
import shutil
from PIL import Image, ImageDraw, ImageFont

def pixel_degrade_png(image_path, output_dir, num_levels=8):
    # Delete old images if the folder exists
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    os.makedirs(output_dir, exist_ok=True)

    img = Image.open(image_path)
    width, height = img.size

    # Define degradation levels including 100% (original)
    percentages = [100 - i * int(100 / (num_levels - 1)) for i in range(num_levels)]
    percentages.reverse()  # start with 0%, then more degraded

    for idx, percent in enumerate(percentages):
        # Calculate reduced size
        scale = max(1, percent / 100)
        new_size = (max(1, int(width * scale)), max(1, int(height * scale)))

        # Resize down and back up
        degraded = img.resize(new_size, Image.NEAREST).resize((width, height), Image.NEAREST)

        # Add label text (bigger and bottom-left)
        draw = ImageDraw.Draw(degraded)
        try:
            font = ImageFont.truetype("arial.ttf", size=int(width * 0.08))
        except:
            font = ImageFont.load_default()

        label = f"{100 - percent}%"
        bbox = draw.textbbox((0, 0), label, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]

        padding = int(width * 0.03)
        x = padding
        y = height - text_height - padding

        # Draw black rectangle behind text
        draw.rectangle(
            [x - 6, y - 6, x + text_width + 6, y + text_height + 6],
            fill=(0, 0, 0, 200)
        )
        draw.text((x, y), label, fill="white", font=font)

        # Save image
        output_path = os.path.join(output_dir, f"degraded_{100 - percent}.png")
        degraded.save(output_path)

    # Save labeled original (0%)
    labeled_original = img.copy()
    draw = ImageDraw.Draw(labeled_original)
    try:
        font = ImageFont.truetype("arial.ttf", size=int(width * 0.08))
    except:
        font = ImageFont.load_default()

    label = "0%"
    bbox = draw.textbbox((0, 0), label, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    padding = int(width * 0.03)
    x = padding
    y = height - text_height - padding
    draw.rectangle(
        [x - 6, y - 6, x + text_width + 6, y + text_height + 6],
        fill=(0, 0, 0, 200)
    )
    draw.text((x, y), label, fill="white", font=font)

    labeled_original.save(os.path.join(output_dir, "original.png"))

if __name__ == "__main__":
    pixel_degrade_png(
        image_path="images/sample.png",
        output_dir="images/pixel_degraded_pngs",
        num_levels=8
    )
