from PIL import Image
import os

def pixel_degrade_png(input_path, output_folder, steps=10, min_scale=0.1, enlarge_back=False):
    """
    Creates progressively lower-resolution versions of an image (PNG format),
    and saves the original image too.

    Args:
        input_path (str): Path to the input image file.
        output_folder (str): Directory where degraded images will be saved.
        steps (int): Number of progressively smaller images.
        min_scale (float): Minimum scale factor (e.g., 0.1 = 10% of original size).
        enlarge_back (bool): If True, re-enlarges degraded images back to the original size.
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    image = Image.open(input_path).convert("RGBA")
    width, height = image.size

    # Save original
    original_path = os.path.join(output_folder, "original.png")
    image.save(original_path, "PNG")
    print(f"Saved original: {original_path} ({width}x{height})")

    # Calculate scale step
    scale_step = (1.0 - min_scale) / steps

    for i in range(steps):
        scale = 1.0 - (i * scale_step)
        new_width = max(1, int(width * scale))
        new_height = max(1, int(height * scale))

        # Resize down
        resized = image.resize((new_width, new_height), Image.LANCZOS)

        # Optionally enlarge back to original to show blockiness
        if enlarge_back:
            resized = resized.resize((width, height), Image.NEAREST)

        output_path = os.path.join(output_folder, f"degraded_{int(scale * 100)}.png")
        resized.save(output_path, "PNG")
        print(f"Saved: {output_path} ({new_width}x{new_height})")

    print("\nDone! All pixel-degraded PNGs (and the original) are in:", output_folder)


# Example usage
if __name__ == "__main__":
    pixel_degrade_png(
        "sample.png",
        "pixel_degraded_pngs",
        steps=8,
        min_scale=0.1,
        enlarge_back=True
    )
