import os
import shutil
from PIL import Image, ImageDraw, ImageFont

def pixel_degrade_png(
    image_path,
    output_dir="pixel_degraded_pngs",
    steps=8,
    label_size=60,
    font_file="GoogleSansCode-Regular.ttf",
    label_prefix="Quality reduced by: ",
    show_label=True,  # ← NEW toggle
):
    # Clear old images
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    os.makedirs(output_dir, exist_ok=True)

    # Load original image
    img = Image.open(image_path)
    original_size = img.size
    images = []

    # Load font
    font_path = os.path.join(os.curdir, font_file)
    try:
        font = ImageFont.truetype(font_path, label_size)
    except Exception as e:
        print(f"Failed to load font '{font_file}': {e}. Falling back to default font.")
        font = ImageFont.load_default()

    for i in range(steps + 1):

        # Calculate degraded size
        new_width = max(1, int(original_size[0] * (1 - (i / steps) * 0.9)))
        new_height = int(new_width * original_size[1] / original_size[0])

        # Compute scale ratio for font
        scale_ratio = new_width / original_size[0]
        dynamic_label_size = max(10, int(label_size * scale_ratio))

        # Resize image once (no resize back up)
        degraded = img.resize((new_width, new_height), Image.NEAREST)

        # Load scaled font
        try:
            font = ImageFont.truetype(font_path, dynamic_label_size)
        except:
            font = ImageFont.load_default()

        if show_label:
            draw = ImageDraw.Draw(degraded)
            label = f"{label_prefix}{int((i / steps) * 100)}%"
            bbox = draw.textbbox((0, 0), label, font=font)
            text_w = bbox[2] - bbox[0]
            text_h = bbox[3] - bbox[1]

            margin, padding_x, padding_y = 20, 15, 10
            position = (margin, degraded.size[1] - text_h - margin)

            draw.rectangle(
                [position, (position[0] + text_w + padding_x, position[1] + text_h + padding_y)],
                fill=(0, 0, 0, 150),
            )

            draw.text(
                (position[0] + padding_x // 2, position[1] + padding_y // 2),
                label,
                font=font,
                fill=(255, 255, 255),
            )

        filename = f"degraded_{int((i / steps) * 100):03}.png"
        filepath = os.path.join(output_dir, filename)
        degraded.save(filepath)
        images.append(f"images/{output_dir}/{filename}")

    images.reverse()

    js_path = os.path.join(os.curdir, "image_list.js")
    with open(js_path, "w") as f:
        f.write("const imageList = [\n")
        for path in images:
            f.write(f'  "{path}",\n')
        f.write("];\n\nexport default imageList;\n")

    print(f"Saved {len(images)} images and image_list.js in '{os.path.abspath(os.curdir)}'")

if __name__ == "__main__":
    pixel_degrade_png(
        image_path="sample.png",
        output_dir="pixel_degraded_pngs",
        steps=8,
        label_size=40,
        font_file="GoogleSansCode-Regular.ttf",
        label_prefix="Quality reduced by: ",
        show_label=True
    )
