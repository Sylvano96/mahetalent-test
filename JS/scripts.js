// -----------------------------------------------------------------------
// Données statiques à afficher
// -----------------------------------------------------------------------
const tasks = [
  {
    "name": "Configurer le serveur",
    "project": "Implémentation Client A",
    "priority": 1,
    "block_reason": "En attente des accès"
  },
  {
    "name": "Rédiger la documentation",
    "project": "Projet interne",
    "priority": 3,
    "block_reason": "Manque d'informations"
  },
  {
    "name": "Mettre à jour le schéma de données",
    "project": "Implémentation Client B",
    "priority": 2,
    "block_reason": "Décision métier en attente"
  }
];

// -----------------------------------------------------------------------
// Libellés de priorité
// -----------------------------------------------------------------------
const PRIORITY_LABELS = {
    1: "Haute",
    2: "Moyenne",
    3: "Basse"
};

// -----------------------------------------------------------------------
// Initialisation
// -----------------------------------------------------------------------
function init() {
    renderTable(tasks);
}

// -----------------------------------------------------------------------
// Rendu du tableau à partir d'une liste de tâches
// -----------------------------------------------------------------------
function renderTable(filteredTasks) {
    const tbody = document.getElementById("tasks-body");
    tbody.innerHTML = "";

    if (filteredTasks.length === 0) {
        const tr = document.createElement("tr");
        tr.innerHTML = `<td colspan="4" class="empty-message">Aucune tâche ne correspond à la recherche.</td>`;
        tbody.appendChild(tr);
        return;
    }

    filteredTasks.forEach(task => {
        const tr = document.createElement("tr");
        tr.innerHTML = `
            <td>${escapeHtml(task.name)}</td>
            <td>${escapeHtml(task.project)}</td>
            <td>
            <span class="priority-badge priority-${task.priority}">
                ${task.priority} – ${PRIORITY_LABELS[task.priority] ?? "Inconnue"}
            </span>
            </td>
            <td>${escapeHtml(task.block_reason)}</td>
        `;
        tbody.appendChild(tr);
    });
}

// -----------------------------------------------------------------------
// Filtrage : recherche dans le champ sélectionné (ou tous les champs)
// -----------------------------------------------------------------------
function applyFilters() {
    const query = document.getElementById("search-input").value.toLowerCase().trim();
    const field = document.getElementById("field-select").value;

    const filtered = tasks.filter(task => {

        const fields = {
            name: task.name,
            project: task.project,
            priority: `${task.priority} ${PRIORITY_LABELS[task.priority] ?? ""}`,
            block_reason: task.block_reason
        };

        if (field === "all") {
            return Object.values(fields).some(value =>
            value.toLowerCase().includes(query)
            );
        }

        return fields[field].toLowerCase().includes(query);
    });

    renderTable(filtered);
}

// -----------------------------------------------------------------------
// Utilitaire : échapper le HTML pour éviter les injections XSS
// -----------------------------------------------------------------------
function escapeHtml(str) {
    const div = document.createElement("div");
    div.appendChild(document.createTextNode(str));
    return div.innerHTML;
}

// -----------------------------------------------------------------------
// Point d'entrée
// -----------------------------------------------------------------------
init();
