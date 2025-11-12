from PIL import Image
import os

def pixel_degrade_png(image_path, output_dir, steps=8, min_scale=0.1, enlarge_back=False):
    """
    Create progressively degraded versions of a PNG image by reducing pixel resolution.
    
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

    for idx, scale in enumerate(scales):
        new_w = max(1, int(width * scale))
        new_h = max(1, int(height * scale))

        degraded = img.resize((new_w, new_h), Image.NEAREST)

        if enlarge_back:
            degraded = degraded.resize((width, height), Image.NEAREST)

        # Save each degraded image with progressive numbering
        output_path = os.path.join(output_dir, f"degraded_{int(scale*100)}.png")
        degraded.save(output_path)

    # Also save a degraded version of the original that matches the same “degradation style”
    # This will make the original appear pixelated similarly
    deg_original = img.resize((max(1,int(width*scales[-1])), max(1,int(height*scales[-1]))), Image.NEAREST)
    if enlarge_back:
        deg_original = deg_original.resize((width, height), Image.NEAREST)
    deg_original.save(os.path.join(output_dir, "original.png"))

# Example usage
if __name__ == "__main__":
    pixel_degrade_png(
        "images/sample.png",
        "images/pixel_degraded_pngs",
        steps=8,
        min_scale=0.1,
        enlarge_back=False
    )
