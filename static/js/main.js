// main.js

document.addEventListener("DOMContentLoaded", () => {
  // theme
  const themeToggle = document.getElementById("theme-toggle");
  const html = document.documentElement;
  const stored = localStorage.getItem("theme");
  if (stored === "dark" || (!stored && window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
    html.setAttribute("data-theme", "dark");
  }
  themeToggle.addEventListener("click", () => {
    const cur = html.getAttribute("data-theme");
    const next = cur === "dark" ? "light" : "dark";
    if (next === "dark") html.setAttribute("data-theme", "dark"); else html.removeAttribute("data-theme");
    localStorage.setItem("theme", next);
  });

  // smooth scrolling for nav - links with href starting #
  document.querySelectorAll('.nav-link, .logo, .btn[href^="#"]').forEach(a => {
    a.addEventListener("click", (e) => {
      const href = a.getAttribute("href");
      if (href && href.startsWith("#")) {
        e.preventDefault();
        const el = document.querySelector(href);
        if (el) el.scrollIntoView({ behavior: "smooth" });
      }
    })
  });

  // load projects
  async function loadProjects() {
  const grid = document.getElementById("projects-grid");

  try {
    const local = await fetch(PROJECTS_JSON).then(r => r.json());
    const github = await fetch("/github-projects").then(r => r.json());

    //const allProjects = [...local, ...github];
    const allProjects = [...github];

    grid.innerHTML = allProjects.map(projectCard).join("");
  } catch (err) {
    console.error("Failed to load projects:", err);
  }
}

loadProjects();


  // contact form
  const form = document.getElementById("contact-form");
  const status = document.getElementById("form-status");
  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    status.textContent = "Sending...";
    const payload = {
      name: document.getElementById("name").value,
      email: document.getElementById("email").value,
      message: document.getElementById("message").value
    };
    try {
      const res = await fetch("/contact", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
      });
      const data = await res.json();
      if (res.ok) {
        status.textContent = data.message || "Message sent!";
        form.reset();
      } else {
        status.textContent = data.message || "Failed to send message.";
      }
    } catch (err) {
      status.textContent = "Network error — try again."
      console.error(err);
    }
  });
});

function projectCard(p) {
  const techs = (p.tech || []).map(t => `<span>${t}</span>`).join("");
  
  // Create the GitHub link HTML snippet
  const githubLink = p.github 
    ? `<a href="${p.github}" target="_blank" rel="noopener" class="github-button">GitHub</a>` 
    : "";
    
  // Create the Live App link HTML snippet
  // It only generates the link if p.live_url exists and is not null/empty
  const liveAppLink = p.live_url 
    ? `<a href="${p.live_url}" target="_blank" rel="noopener" class="live-app-button">Live App</a>` 
    : "";

  return `
    <div class="card">
      <h3>${p.title}</h3>
      <p>${p.desc}</p>
      <div class="tags">${techs}</div>
      <div class="project-links" style="margin-top:8px">
        ${githubLink}
        <!-- The live app link is added right here -->
        ${liveAppLink}
      </div>
    </div>
  `;
}
