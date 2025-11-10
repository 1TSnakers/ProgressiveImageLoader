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
        "https://upload.wikimedia.org/wikipedia/commons/thumb/2/2a/Coat_of_arms_of_Mexico.svg/330px-Coat_of_arms_of_Mexico.svg.png",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/2/2a/Coat_of_arms_of_Mexico.svg/529px-Coat_of_arms_of_Mexico.svg.png",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/2/2a/Coat_of_arms_of_Mexico.svg/847px-Coat_of_arms_of_Mexico.svg.png",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/2/2a/Coat_of_arms_of_Mexico.svg/1129px-Coat_of_arms_of_Mexico.svg.png",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/2/2a/Coat_of_arms_of_Mexico.svg/2259px-Coat_of_arms_of_Mexico.svg.png"
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
In this example, the images are:
<details>
<br>
<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/2/2a/Coat_of_arms_of_Mexico.svg/330px-Coat_of_arms_of_Mexico.svg.png" alt="drawing" width="160"/>
<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/2/2a/Coat_of_arms_of_Mexico.svg/529px-Coat_of_arms_of_Mexico.svg.png" alt="drawing" width="160"/>
<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/2/2a/Coat_of_arms_of_Mexico.svg/847px-Coat_of_arms_of_Mexico.svg.png" alt="drawing" width="160"/>
<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/2/2a/Coat_of_arms_of_Mexico.svg/1129px-Coat_of_arms_of_Mexico.svg.png" alt="drawing" width="160"/>
<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/2/2a/Coat_of_arms_of_Mexico.svg/2259px-Coat_of_arms_of_Mexico.svg.png" alt="drawing" width="160"/>
<br>
Courtesy of wikipedia
</details>
Feel free to improve my bad code!
