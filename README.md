# Progressive Image Loader
Loads images progressively. Level of detail for images

You put images into an array in order of detail (least to most)

⚠️ This could increase internet usage as you are requesting like 3 images instead of just one, but has the benefit of allowing the user to see _somthing_ quickly

Here is an example HTML file and web demo: https://1tsnakers.github.io/ProgressiveImageLoader
```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Progressive Image Loader Demo</title>
</head>
<body>
  <!-- Container for the progressive image -->
  <div id="image-container"></div>

  <!-- Include your library -->
  <script src=""progressive-image-loader.js"></script>

  <script>
    // Instantiate the loader
    new ProgressiveImageLoader({
      container: document.getElementById("image-container"),
      images: [
        "bad-image.png",
        "mid-image.png",
        "good-image.png"
      ],
      width: 600,       // optional
      height: 600,      // optional
      fadeDuration: 500, // optional
      disableCache: false // optional
    });
  </script>
</body>
</html>

```
In the web demo example, the images are:
<details>
<br>
<img src="https://raw.githubusercontent.com/1TSnakers/ProgressiveImageLoader/refs/heads/main/images/pixel_degraded_pngs/degraded_000.png" alt="drawing" width="160"/>
<img src="https://raw.githubusercontent.com/1TSnakers/ProgressiveImageLoader/refs/heads/main/images/pixel_degraded_pngs/degraded_012.png" alt="drawing" width="160"/>
<img src="https://raw.githubusercontent.com/1TSnakers/ProgressiveImageLoader/refs/heads/main/images/pixel_degraded_pngs/degraded_025.png" alt="drawing" width="160"/>
<img src="https://raw.githubusercontent.com/1TSnakers/ProgressiveImageLoader/refs/heads/main/images/pixel_degraded_pngs/degraded_037.png" alt="drawing" width="160"/>
<img src="https://raw.githubusercontent.com/1TSnakers/ProgressiveImageLoader/refs/heads/main/images/pixel_degraded_pngs/degraded_050.png" alt="drawing" width="160"/>
<img src="https://raw.githubusercontent.com/1TSnakers/ProgressiveImageLoader/refs/heads/main/images/pixel_degraded_pngs/degraded_062.png" alt="drawing" width="160"/>
<img src="https://raw.githubusercontent.com/1TSnakers/ProgressiveImageLoader/refs/heads/main/images/pixel_degraded_pngs/degraded_075.png" alt="drawing" width="160"/>
<img src="https://raw.githubusercontent.com/1TSnakers/ProgressiveImageLoader/refs/heads/main/images/pixel_degraded_pngs/degraded_087.png" alt="drawing" width="160"/>
<img src="https://raw.githubusercontent.com/1TSnakers/ProgressiveImageLoader/refs/heads/main/images/pixel_degraded_pngs/degraded_100.png" alt="drawing" width="160"/>
<br>
Courtesy of a funny image on https://random.dog
</details>
Feel free to improve my bad code!
