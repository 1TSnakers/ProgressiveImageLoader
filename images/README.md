# Image Ruiner Python Script

This is an automated script that creates images in a progressively worse quality.

This is the function:
```python
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
        # Pixelate by resizing down and back up
        scale = max(1, int(original_size[0] * (1 - (i / steps) * 0.9)))
        degraded = img.resize((scale, int(scale * original_size[1] / original_size[0]))).resize(original_size)

        if show_label:
            draw = ImageDraw.Draw(degraded)
            label = f"{label_prefix}{int((i / steps) * 100)}%"
            text_w, text_h = draw.textbbox((0, 0), label, font=font)[2:]
            margin, padding_x, padding_y = 20, 15, 10
            position = (margin, original_size[1] - text_h - margin)
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
```

This is how you use it:
```python
pixel_degrade_png(
    """
    Degrades an image in steps and optionally adds a percentage label in the bottom-left corner.
    
    Parameters:
    - image_path: str, path to the input image (relative to /images)
    - output_dir: str, directory to save degraded images (relative to /images)
    - steps: int, number of degradation steps
    - label_size: int, font size for the percentage label
    - font_file: str, path to the .ttf font file (relative to /images)
    - label_prefix: str, text to prefix the percentage label
    - show_label: bool, whether to draw labels on images
    """
    image_path="sample.png",
    steps=8, # 
    label_size=40,
    font_file="GoogleSansCode-Regular.ttf",
    label_prefix="Quality reduced by: ",
    show_label=True
)
```
Here is an example image made by the program:

![](images/pixel_degraded_pngs/degraded_100.png)
