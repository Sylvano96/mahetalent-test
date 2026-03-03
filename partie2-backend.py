"""
Partie 2 – Backend
Gestion de tâches de projet avec filtrage, tri et validation.
"""


class Task:
    def __init__(self, name, project, priority, is_blocked=False, block_reason=None):
        self.name = name
        self.project = project
        self.priority = priority
        self.is_blocked = is_blocked
        self.block_reason = block_reason

    def set_blocked(self, is_blocked: bool, block_reason: str = None):

        # --- Met à jour l'état de blocage d'une tâche.

        if is_blocked:
            if not block_reason or not block_reason.strip():
                raise ValueError(
                    "Une raison de blocage (block_reason) est obligatoire "
                    "lorsque la tâche est marquée comme bloquée."
                )

        self.is_blocked = is_blocked
        self.block_reason = block_reason.strip() if is_blocked else None

    def __repr__(self):
        status = f"BLOQUÉE ({self.block_reason})" if self.is_blocked else "Active"
        return f"Task(name={self.name!r}, project={self.project!r}, priority={self.priority}, status={status})"


# ---------------------------------------------------------------------------
# 1. Fonction de filtrage et tri
# ---------------------------------------------------------------------------

def get_blocked_tasks(tasks: list[Task]) -> list[Task]:
    
    # --- Retourne les tâches bloquées, triées :
    
    blocked = [task for task in tasks if task.is_blocked]
    blocked.sort(key=lambda task: (task.priority, task.name))
    return blocked


# ---------------------------------------------------------------------------
# Exemples d'utilisation (Pour un petit test)
# ---------------------------------------------------------------------------

if __name__ == "__main__":

    # --- Données de test ---
    tasks = [
        Task("Déployer en production",   "Projet Alpha",  priority=1, is_blocked=True,  block_reason="Serveur indisponible"),
        Task("Rédiger les specs",         "Projet Beta",   priority=3, is_blocked=False),
        Task("Corriger le bug login",     "Projet Alpha",  priority=2, is_blocked=True,  block_reason="En attente du retour client"),
        Task("Mettre à jour la BDD",      "Projet Gamma",  priority=1, is_blocked=True,  block_reason="Migration en cours"),
        Task("Configurer le CI/CD",       "Projet Beta",   priority=2, is_blocked=False),
        Task("Analyser les logs",         "Projet Alpha",  priority=1, is_blocked=True,  block_reason="Accès refusé"),
        Task("Écrire les tests",          "Projet Gamma",  priority=3, is_blocked=False),
    ]

    # --- Exemple 1 : filtrage et tri des tâches bloquées ---
    print("=== Tâches bloquées (triées par priorité puis par nom) ===")
    blocked = get_blocked_tasks(tasks)
    for task in blocked:
        print(f"  [{task.priority}] {task.name} — {task.block_reason}")

    # Résultat attendu (priorité 1 en premier, puis ordre alpha) :
    #   [1] Analyser les logs — Accès refusé
    #   [1] Déployer en production — Serveur indisponible
    #   [1] Mettre à jour la BDD — Migration en cours
    #   [2] Corriger le bug login — En attente du retour client

    print()

    # --- Exemple 2 : marquer une tâche comme bloquée (cas valide) ---
    print("=== Mise à jour valide ===")
    task = tasks[1]  # "Rédiger les specs", non bloquée initialement
    task.set_blocked(True, "En attente de validation du client")
    print(f"  {task}")

    print()

    # --- Exemple 3 : débloquer une tâche ---
    print("=== Déblocage d'une tâche ===")
    task.set_blocked(False)
    print(f"  {task}")

    print()

    # --- Exemple 4 : cas d'erreur — blocage sans raison ---
    print("=== Cas d'erreur : blocage sans raison ===")
    task_to_block = Task("Migrer les données", "Projet Delta", priority=2)
    try:
        task_to_block.set_blocked(True, "   ")  # Espaces uniquement → erreur
    except ValueError as e:
        print(f"  Erreur interceptée : {e}")

    print()

    # --- Exemple 5 : cas d'erreur — block_reason None ---
    print("=== Cas d'erreur : block_reason absente ===")
    try:
        task_to_block.set_blocked(True)  # Pas de raison du tout → erreur
    except ValueError as e:
        print(f"  Erreur interceptée : {e}")
