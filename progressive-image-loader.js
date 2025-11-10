// progressive-image-loader.js
class ProgressiveImageLoader {
  constructor(options) {
    this.container = options.container; // DOM element
    this.images = options.images;       // array of image URLs
    this.width = options.width || 600;
    this.height = options.height || 600;
    this.fadeDuration = options.fadeDuration || 500; // ms
    this.disableCache = options.disableCache || false;

    this.currentIndex = -1;
    this.current = null;
    this.next = null;

    this._setupDOM();
    this._loadImages();
  }

  _setupDOM() {
    this.wrapper = document.createElement("div");
    this.wrapper.style.position = "relative";
    this.wrapper.style.width = this.width + "px";
    this.wrapper.style.height = this.height + "px";

    this.current = document.createElement("img");
    this.next = document.createElement("img");

    for (let img of [this.current, this.next]) {
      img.style.position = "absolute";
      img.style.top = 0;
      img.style.left = 0;
      img.style.width = "100%";
      img.style.height = "100%";
      img.style.objectFit = "contain";
      img.style.transition = `opacity ${this.fadeDuration}ms ease`;
      img.style.opacity = 0;
      this.wrapper.appendChild(img);
    }

    this.current.classList.add("visible");
    this.container.appendChild(this.wrapper);
  }

  _preloadImage(src) {
    return new Promise((resolve, reject) => {
      const img = new Image();
      let finalSrc = src;
      if (this.disableCache) {
        finalSrc += (src.includes("?") ? "&" : "?") + "t=" + new Date().getTime();
      }
      img.src = finalSrc;
      img.onload = () => resolve(finalSrc);
      img.onerror = reject;
    });
  }

  _loadImages() {
    this.images.forEach((src, index) => {
      this._preloadImage(src).then(loadedSrc => {
        if (index > this.currentIndex) {
          this.next.src = loadedSrc;
          this.next.style.opacity = 1;
          this.current.style.opacity = 0;

          [this.current, this.next] = [this.next, this.current];
          this.currentIndex = index;
        }
      }).catch(err => console.error(`Failed to load ${src}:`, err));
    });
  }
}
