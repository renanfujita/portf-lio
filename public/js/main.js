document.addEventListener("DOMContentLoaded", () => {
  fetchProjects();
});

async function fetchProjects() {
  const grid = document.getElementById("projects-grid");
  const counter = document.getElementById("projects-counter");

  try {
    const response = await fetch("/api/projects/");
    
    if (!response.ok) {
      throw new Error(`Erro HTTP: ${response.status}`);
    }

    const data = await response.json();
    const projects = data.projects || [];

    // Atualiza o contador
    if (counter) {
      counter.textContent = `${data.total} repositórios`;
    }

    // Se não houver projetos públicos
    if (projects.length === 0) {
      grid.innerHTML = `
        <div class="card">
          <p class="card-desc">Nenhum repositório público encontrado no momento.</p>
        </div>
      `;
      return;
    }

    // Renderiza os cartões dinamicamente
    grid.innerHTML = projects.map(project => `
      <a href="${project.html_url}" target="_blank" rel="noopener noreferrer" class="card">
        <div class="card-header">
          <span class="card-title">${escapeHtml(project.name)}</span>
          <span class="card-icon">↗</span>
        </div>
        <p class="card-desc">
          ${project.description ? escapeHtml(project.description) : "Repositório técnico sem descrição detalhada cadastrada."}
        </p>
        <div class="card-meta">
          <span class="card-lang">${escapeHtml(project.language || "Geral")}</span>
          <span>Atualizado em ${project.updated_at}</span>
        </div>
      </a>
    `).join("");

  } catch (error) {
    console.error("Falha ao carregar repositórios:", error);
    if (counter) counter.textContent = "Erro na sincronização";
    grid.innerHTML = `
      <div class="card">
        <p class="card-desc" style="color: #ef4444;">
          Não foi possível conectar com a API de projetos. Tente novamente mais tarde.
        </p>
      </div>
    `;
  }
}

// Prevenção contra injeção de HTML acidental em textos do GitHub
function escapeHtml(text) {
  const div = document.createElement("div");
  div.textContent = text;
  return div.innerHTML;
}