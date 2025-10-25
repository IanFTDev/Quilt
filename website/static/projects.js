// Represents the button that adds new patterns
class plusProjects {
  constructor(containerId) {
    this.container = document.getElementById(containerId);
    this.button = this.createSelf();
    this.projects = [];
  }

  createSelf() {
    const btn = document.createElement("button");
    btn.textContent = "+ New Projects";
    btn.classList.add("plusButton");

    btn.addEventListener("click", async () => {
      try {
        // Create project in database
        const response = await fetch("/create-project", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
        });

        if (response.ok) {
          const result = await response.json();
          // Create button with the new project ID
          this.projects.push(new Project(this.container, result.project_id));
        }
      } catch (error) {
        console.error("Failed to create project:", error);
      }
    });

    this.container.appendChild(btn);
    return btn;
  }
}
class Project {
  constructor(container, projectID) {
    this.container = container;
    this.projectID = projectID;
    this.button = this.createSelf();
  }

  createSelf() {
    const btn = document.createElement("button");
    btn.textContent = `Project ${this.projectID}`;
    btn.classList.add("projectButton");

    btn.addEventListener("click", () => {
      // Simply redirect to the route
      window.location.href = `/project/${this.projectID}`;
    });

    this.container.insertBefore(btn, this.container.lastChild);
    return btn;
  }
}

const patternManager = new plusProjects("projectContainer");
const projectContainer = document.getElementById("projectContainer");
