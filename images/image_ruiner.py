import os
from PIL import Image, ImageDraw, ImageFont
import random

def pixel_degrade_png(image_path, output_dir, label, num_outputs=5, degrade_factor=0.7):
    os.makedirs(output_dir, exist_ok=True)

    # Delete all old images in the output folder
    for f in os.listdir(output_dir):
        if f.endswith(".png"):
            os.remove(os.path.join(output_dir, f))

    img = Image.open(image_path).convert("RGB")
    width, height = img.size
    degraded_images = []

    for i in range(num_outputs):
        degraded = img.copy()

        # Random pixel degradation
        for _ in range(int(width * height * degrade_factor * random.uniform(0.05, 0.2))):
            x, y = random.randint(0, width - 1), random.randint(0, height - 1)
            degraded.putpixel((x, y), tuple(random.randint(0, 255) for _ in range(3)))

        draw = ImageDraw.Draw(degraded)
        try:
            font = ImageFont.truetype("arial.ttf", 24)
        except:
            font = ImageFont.load_default()

        # Draw label bottom-left corner with margin
        text = f"{label} {i+1}"
        text_w, text_h = draw.textbbox((0, 0), text, font=font)[2:]
        margin = 10
        draw.text((margin, height - text_h - margin), text, fill=(255, 255, 255), font=font)

        # Consistent filename: degraded_0001.png, degraded_0002.png, etc.
        filename = f"degraded_{i+1:04d}.png"
        output_path = os.path.join(output_dir, filename)
        degraded.save(output_path)
        degraded_images.append(filename)

    # Create JS file with array of images
    js_array_path = os.path.join(output_dir, "image_list.js")
    with open(js_array_path, "w") as f:
        f.write("const imageList = [\n")
        for name in degraded_images:
            f.write(f'    "{name}",\n')
        f.write("];\n\nexport default imageList;\n")

    print(f"Created {num_outputs} degraded images and image_list.js")

if __name__ == "__main__":
    pixel_degrade_png(
        image_path="sample.png",
        output_dir="output",
        label="Degraded",
        num_outputs=5
    )
