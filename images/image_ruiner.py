from PIL import Image, ImageDraw, ImageFont
import os

def pixel_degrade_png(image_path, output_dir, steps=8, min_scale=0.1, enlarge_back=False):
    """
    Create progressively degraded versions of a PNG image with a corner label for degradation percentage.

    Parameters:
    - image_path: str, path to the original PNG
    - output_dir: str, directory to save degraded PNGs
    - steps: int, number of degradation steps
    - min_scale: float, smallest scale factor for the last degraded image
    - enlarge_back: bool, whether to enlarge back to original size after downscaling
    """

    os.makedirs(output_dir, exist_ok=True)
    img = Image.open(image_path)
    width, height = img.size

    # Generate degradation scales (including the original)
    scales = [1.0 - i * (1.0 - min_scale) / (steps-1) for i in range(steps)]
    percentages = [0] + [int((1-s)*100) for s in scales[1:]]

    for idx, scale in enumerate(scales):
        new_w = max(1, int(width * scale))
        new_h = max(1, int(height * scale))

        degraded = img.resize((new_w, new_h), Image.NEAREST)

        if enlarge_back:
            degraded = degraded.resize((width, height), Image.NEAREST)

        # Add a small label in the top-left corner
        draw = ImageDraw.Draw(degraded)
        try:
            font = ImageFont.truetype("arial.ttf", size=int(width * 0.05))
        except:
            font = ImageFont.load_default()
        label = f"{percentages[idx]}%"
        text_size = draw.textsize(label, font=font)
        padding = int(width * 0.02)
        draw.rectangle([padding-2, padding-2, text_size[0]+padding+2, text_size[1]+padding+2], fill=(0,0,0,180))
        draw.text((padding, padding), label, fill="white", font=font)

        # Save image
        output_path = os.path.join(output_dir, f"degraded_{percentages[idx]}.png")
        degraded.save(output_path)

# Example usage
if __name__ == "__main__":
    pixel_degrade_png(
        "sample.png",
        "pixel_degraded_pngs",
        steps=8,
        min_scale=0.1,
        enlarge_back=False
    )

