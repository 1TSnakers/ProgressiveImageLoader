import os
from PIL import Image, ImageDraw, ImageFont

def pixel_degrade_png(image_path, output_dir="pixel_degraded_pngs", steps=8):
    # Make sure output folder exists inside the script folder
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(script_dir, output_dir)
    os.makedirs(output_path, exist_ok=True)

    # Remove old images
    for file in os.listdir(output_path):
        if file.endswith(".png"):
            os.remove(os.path.join(output_path, file))

    # Load image
    img = Image.open(os.path.join(script_dir, image_path))
    original_size = img.size
    images = []

    for i in range(steps + 1):
        # Calculate degradation percentage
        percent = int((i / steps) * 100)
        scale = max(1, int(original_size[0] * (1 - (percent / 100) * 0.9)))
        degraded = img.resize((scale, int(scale * original_size[1] / original_size[0]))).resize(original_size)

        # Draw percentage label
        draw = ImageDraw.Draw(degraded)
        try:
            font = ImageFont.truetype("arial.ttf", 30)
        except:
            font = ImageFont.load_default()

        label = f"{percent}%"
        text_w, text_h = draw.textbbox((0, 0), label, font=font)[2:]
        margin = 10
        position = (margin, original_size[1] - text_h - margin)

        draw.rectangle([position, (position[0] + text_w + 10, position[1] + text_h + 5)], fill=(0, 0, 0, 150))
        draw.text((position[0] + 5, position[1]), label, font=font, fill=(255, 255, 255))

        # Save file using percentage in the name
        filename = f"degraded_{percent}.png"
        filepath = os.path.join(output_path, filename)
        degraded.save(filepath)
        images.append(f"{output_dir}/{filename}")  # relative path for JS array

    # Save JS array in the script folder
    js_path = os.path.join(script_dir, "image_list.js")
    with open(js_path, "w") as f:
        f.write("const imageList = [\n")
        for path in images:
            f.write(f'  "{path}",\n')
        f.write("];\n\nexport default imageList;\n")

    print(f"Saved {len(images)} images in '{output_dir}' and image_list.js at: {js_path}")

if __name__ == "__main__":
    pixel_degrade_png(
        image_path="sample.png",   # relative to /images
        output_dir="pixel_degraded_pngs",
        steps=8
    )
