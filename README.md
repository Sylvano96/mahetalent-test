# Test technique – Développeur Fullstack Junior

Réponses au test technique en trois parties.

## Structure du dépôt

```
├── partie1-analysefonctionnelle.md   # Analyse fonctionnelle
├── partie2-backend.py                # Backend Python
├── partie3-frontend.html             # Frontend HTML
├── JS/
│   └── scripts.js                    # JavaScript pour le frontend
└── README.md
```

## Partie 1 – Analyse fonctionnelle

Analyse du cas métier d'une application de calcul automatisé pour la broderie :
- Approche globale étape par étape (upload → analyse → calcul → restitution)
- Modèle de données complet (entités, champs, relations, règles métier)
- Obstacles potentiels et pistes de résolution

## Partie 2 – Backend (Python)

Manipulation de tâches de projet :
- `get_blocked_tasks(tasks)` : filtre les tâches bloquées et les trie par priorité puis par nom
- `Task.set_blocked(is_blocked, block_reason)` : met à jour l'état de blocage avec validation (lève une `ValueError` si `is_blocked=True` sans raison valide)
- Exemples d'appels inclus dans le bloc `__main__`

**Choix du langage :**  

J'ai choisi particulièrement Python pour cette deuxième partie en raison de sa maniabilité par rapport aux autres langages, pour concrétiser rapidement les idées et optimiser la résolution des problèmes. 

**Exécution :**
```bash
python partie2-backend.py
```

## Partie 3 – Frontend (HTML/JS)

Page HTML autonome affichant des tâches bloquées :
- Tableau rempli dynamiquement depuis un JSON statique
- Champ de recherche par nom de tâche (filtre en temps réel)
- Sélecteur de projet pour filtrer par projet
- Badges de priorité colorés
- Protection XSS basique (`escapeHtml`)

**Note important :** le fichier scripts.js doit être dans le fichier JS, à côté du fichier  partie3-frontend.html.

**Utilisation :** ouvrir `partie3-frontend.html` directement dans un navigateur.

## Auteur 

**Nom :** TOLOJANAHARY

**Prénoms :** Elias Sylvano

**Email :** eliasvano78@gmail.com