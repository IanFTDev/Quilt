let currentPattern;
let currentPatternID;
let currentProjectID;

// A class Representing each new pattern
class Pattern {
  constructor(container, id = -1, file = null) {
    this.container = container;
    this.id = id;

    if (file == null) {
      this.button = this.createSelf();
    } else {
      this.button = this.loadSelf(file);
    }
  }

  loadSelf(file) {
    const btn = document.createElement("button");
    btn.classList.add("patternButton");

    // For loaded patterns, the file is a URL string, not a File object
    const img = document.createElement("img");
    img.src = file; // file is actually the URL string
    img.alt = "Quilt Pattern";

    btn.appendChild(img);

    btn.addEventListener("click", () => {
      this.patternSelecter(file);
    });

    this.container.insertBefore(btn, this.container.lastChild);
    return btn;
  }
  createSelf() {
    const btn = document.createElement("button");
    btn.textContent = "Choose Pattern";
    btn.classList.add("patternButton");

    const hiddenUpload = document.createElement("input");
    hiddenUpload.type = "file";
    hiddenUpload.accept = "image/*";

    const clickController = new AbortController();

    btn.addEventListener(
      "click",
      () => {
        hiddenUpload.click();
      },
      { signal: clickController.signal }
    );

    const hiddenController = new AbortController();
    hiddenUpload.addEventListener(
      "change",
      (event) => {
        const file = event.target.files[0];
        if (file) {
          if (file.type == "image/jpeg" || file.type == "image/png") {
            this.addImg(file);
            this.uploadImage(file);
            clickController.abort();

            btn.addEventListener("click", () => {
              this.patternSelecter(file);
            });

            hiddenController.abort();
          } else {
            alert("Please select jpeg or png file");
          }
        } else {
          console.log("File Not selected");
        }
      },
      { signal: hiddenController.signal }
    );

    this.container.insertBefore(btn, this.container.lastChild);
    return btn;
  }

  addImg(file) {
    const img = document.createElement("img");
    const imgUrl = URL.createObjectURL(file);
    img.src = imgUrl;

    img.onload = function () {
      URL.revokeObjectURL(imgUrl);
    };

    img.alt = "Quilt Pattern";
    this.button.textContent = "";
    this.button.appendChild(img);
  }

  async uploadImage(file) {
    const formData = new FormData();
    formData.append("image", file);
    formData.append("projectID", currentProjectID);

    try {
      const response = await fetch("/download-pattern", {
        method: "POST",
        body: formData,
      });

      if (response.ok) {
        const result = await response.json();
        console.log("Upload successful:", result);
        this.id = result.pattern_id;
      } else {
        console.error("Upload failed:", response.statusText);
      }
    } catch (error) {
      console.error("Error uploading image:", error);
    }
  }

  patternSelecter(file) {
    let imgUrl;

    // Check if it's a File object or already a URL string
    if (file instanceof File || file instanceof Blob) {
      imgUrl = URL.createObjectURL(file);
    } else {
      imgUrl = file; // It's already a URL string
    }

    currentPattern = imgUrl;
    currentPatternID = this.id;

    // Visual feedback for selected pattern
    document.querySelectorAll(".patternButton").forEach((btn) => {
      btn.style.borderColor = "#dee2e6";
      btn.style.boxShadow = "none";
    });
    this.button.style.borderColor = "#28a745";
    this.button.style.boxShadow = "0 0 12px rgba(40, 167, 69, 0.5)";
  }
}

// Represents the button that adds new patterns
class plusPattern {
  constructor(containerId) {
    this.container = document.getElementById(containerId);
    this.button = this.createSelf();
    this.patterns = [];
  }

  createSelf() {
    const btn = document.createElement("button");
    btn.textContent = "+ New Pattern";
    btn.classList.add("plusButton");

    btn.addEventListener("click", () => {
      this.patterns.push(new Pattern(this.container));
    });

    this.container.appendChild(btn);
    return btn;
  }
}

class Quilt {
  constructor(containerId, cols = 10, rows = 10, currentProject) {
    this.container = document.getElementById(containerId);
    // this.tiles = this.createSquareQuilt(cols, rows);
    const grid = document.querySelector(".quilt-grid");
    grid.style.setProperty("--grid-columns", cols);
    grid.style.setProperty("--grid-rows", rows);
    currentProjectID = currentProject;
  }

  createSquareQuilt(width, height) {
    let newTiles = [];
    for (let x = 0; x < width; x++) {
      for (let y = 0; y < height; y++) {
        newTiles.push(new Tile(this.container));
      }
    }
    return (this.tiles = newTiles);
  }
}

class Tile {
  constructor(container, id, img = null) {
    this.container = container;
    this.id = id;
    this.button = this.createSelf();
    if (img) {
      this.img = this.addPattern(img);
    } else {
      this.img = null;
    }
  }

  createSelf() {
    const btn = document.createElement("button");
    btn.classList.add("tileButton");
    this.container.appendChild(btn);

    btn.addEventListener("click", () => this.addPattern(currentPattern));
    btn.addEventListener("click", () => this.saveTile(currentPattern));

    return btn;
  }

  addPattern(toAdd) {
    if (toAdd) {
      if (!this.img) {
        const img = document.createElement("img");
        img.classList.add("tileImage");
        this.img = img;
        this.button.innerHTML = "";
        this.button.appendChild(img);
      }
      this.img.src = toAdd;
      this.img.alt = "Quilt Pattern";
    }
  }

  async saveTile(toAdd) {
    console.log("SAVING TILE");
    if (!toAdd) {
      return;
    }
    const formData = new FormData();
    formData.append("tile_id", this.id);
    formData.append("pattern_id", currentPatternID);

    try {
      const response = await fetch("/save-tile", {
        method: "POST",
        body: formData,
      });

      if (response.ok) {
        const result = await response.json();
        console.log("Upload successful:", result);
      } else {
        console.error("Upload failed:", response.statusText);
      }
    } catch (error) {
      console.error("Error Saving Tile:", error);
    }
  }
}
