import os
from PIL import Image, ImageDraw, ImageFont

def pixel_degrade_png(image_path, output_dir="images/output", steps=8):
    os.makedirs(output_dir, exist_ok=True)

    # Remove old images
    for file in os.listdir(output_dir):
        if file.endswith(".png"):
            os.remove(os.path.join(output_dir, file))

    # Load image
    img = Image.open(image_path)
    original_size = img.size
    images = []

    for i in range(steps + 1):
        scale = max(1, int(original_size[0] * (1 - (i / steps) * 0.9)))
        degraded = img.resize((scale, int(scale * original_size[1] / original_size[0]))).resize(original_size)

        draw = ImageDraw.Draw(degraded)
        try:
            font = ImageFont.truetype("arial.ttf", 30)
        except:
            font = ImageFont.load_default()

        label = f"{int((i / steps) * 100)}%"
        text_w, text_h = draw.textbbox((0, 0), label, font=font)[2:]
        margin = 10
        position = (margin, original_size[1] - text_h - margin)

        draw.rectangle([position, (position[0] + text_w + 10, position[1] + text_h + 5)], fill=(0, 0, 0, 150))
        draw.text((position[0] + 5, position[1]), label, font=font, fill=(255, 255, 255))

        filename = f"degraded_{i:03}.png"
        filepath = os.path.join(output_dir, filename)
        degraded.save(filepath)
        images.append(f"images/output/{filename}")

    # Save JS array in images/
    js_path = os.path.join("images", "image_list.js")
    with open(js_path, "w") as f:
        f.write("const imageList = [\n")
        for path in images:
            f.write(f'  "{path}",\n')
        f.write("];\n\nexport default imageList;\n")

    print(f"Saved {len(images)} images and image_list.js in 'images/'")

if __name__ == "__main__":
    pixel_degrade_png(
        image_path="sample.png",
        output_dir="output",
        label="Degraded",
        num_outputs=8
    )
