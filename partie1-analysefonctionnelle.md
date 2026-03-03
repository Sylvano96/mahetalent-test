# Partie 1 – Analyse fonctionnelle

## 1. Approche globale

### Vision d'ensemble

```
[Utilisateur] 
    │
    ▼
[Upload image] ──► [Validation image] ──► [Analyse des couleurs] ──► [Calcul des surfaces]
                                                  │                          │
                                           [Quantification            [Agrégation par
                                            des couleurs]              couleur]
                                                  │                          │
                                                  └──────────┬───────────────┘
                                                             ▼
                                                  [Estimation fil / coût / temps]
                                                             │
                                                             ▼
                                                  [Restitution à l'utilisateur]
```

### Décomposition par grandes étapes

**Étape 1 – Réception et validation de l'image**
- L'utilisateur upload une image via l'interface (formats acceptés : PNG, JPG, SVG…)
- Validation : format supporté, taille de fichier raisonnable, dimensions minimales
- Stockage temporaire de l'image (ou en base si on veut persister le projet)

**Étape 2 – Analyse des couleurs**
- Lecture pixel par pixel (ou zone par zone) de l'image
- Quantification des couleurs : regrouper les couleurs proches en couleurs représentatives (ex. : k-means, médian cut)
- Production d'une palette de N couleurs dominantes avec leur code hexadécimal

**Étape 3 – Calcul des surfaces par couleur**
- Pour chaque couleur détectée, compter le nombre de pixels qui lui sont associés
- Convertir ce compte de pixels en surface réelle (cm² ou mm²) selon la résolution de l'image et les dimensions physiques fournies par l'utilisateur (ex. : "ce motif fait 20×30 cm")
- Calculer le pourcentage de chaque couleur sur la surface totale

**Étape 4 – Estimation fil / coût / temps**
- Appliquer des formules de conversion : surface → longueur de fil (dépend de la densité de points et du type de point)
- Appliquer un tarif/heure ou un coût par mètre de fil
- Calculer un résultat global et par couleur

**Étape 5 – Restitution à l'utilisateur**
- Affichage d'un résumé : tableau couleurs / surfaces / quantités de fil / coût estimé
- Export possible (PDF, CSV)
- Visualisation de l'image avec les zones colorées annotées (optionnel)

---

## 2. Modèle de données

### Entités principales

#### `EmbroideryProject` (Projet de broderie)
| Champ | Type | Rôle |
|---|---|---|
| `id` | UUID | Identifiant unique du projet |
| `name` | string | Nom donné au projet par l'utilisateur |
| `created_at` | datetime | Date de création |
| `image_original_url` | string | URL/chemin de l'image originale uploadée |
| `image_width_cm` | float | Largeur physique réelle du motif (en cm) |
| `image_height_cm` | float | Hauteur physique réelle du motif (en cm) |
| `status` | enum | `pending` / `analyzed` / `error` |
| `config_id` | FK → EmbroideryConfig | Référence à la configuration utilisée |

**Règles :** `image_width_cm > 0`, `image_height_cm > 0`, `status` doit être une valeur valide.

---

#### `DetectedColor` (Couleur détectée)
| Champ | Type | Rôle |
|---|---|---|
| `id` | UUID | Identifiant unique |
| `project_id` | FK → EmbroideryProject | Projet auquel appartient cette couleur |
| `hex_code` | string | Code couleur hexadécimal (ex. : `#3A7D44`) |
| `label` | string (nullable) | Nom lisible optionnel (ex. : "Vert foncé") |
| `pixel_count` | integer | Nombre de pixels correspondant à cette couleur |
| `surface_cm2` | float | Surface calculée en cm² |
| `percentage` | float | % de la surface totale |

**Règles :** `hex_code` doit correspondre au format `#RRGGBB`, `pixel_count > 0`, `surface_cm2 > 0`, `0 < percentage <= 100`.

---

#### `EmbroideryEstimation` (Estimation par couleur)
| Champ | Type | Rôle |
|---|---|---|
| `id` | UUID | Identifiant unique |
| `color_id` | FK → DetectedColor | Couleur concernée |
| `thread_length_m` | float | Longueur de fil estimée (en mètres) |
| `thread_weight_g` | float (nullable) | Poids de fil estimé (en grammes) |
| `estimated_time_min` | float | Temps de broderie estimé (en minutes) |
| `estimated_cost` | float | Coût estimé (en devise configurée) |

**Règles :** toutes les valeurs doivent être `>= 0`.

---

#### `EmbroideryConfig` (Configuration)
| Champ | Type | Rôle |
|---|---|---|
| `id` | UUID | Identifiant unique |
| `stitch_type` | string | Type de point (ex. : "point de croix", "satin", "plumetis") |
| `stitch_density` | float | Densité de points (ex. : nombre de points par cm²) |
| `thread_cost_per_meter` | float | Coût du fil par mètre |
| `hourly_rate` | float | Tarif horaire de la broderie |
| `stitches_per_minute` | float | Vitesse de broderie (points/min, pour estimation temps) |
| `currency` | string | Devise (ex. : "EUR") |

**Règles :** `stitch_density > 0`, `thread_cost_per_meter >= 0`, `hourly_rate >= 0`.

---

### Relations entre entités
```
┌──────────────────┐         ┌───────────────────┐         ┌─────────────────┐
│ EmbroideryConfig │ 1 ───── N│ EmbroideryProject │1 ───── N│  DetectedColor  │
└──────────────────┘         └───────────────────┘         └─────────────────┘
                                                                     │ 1
                                                                     │
                                                                     │ 1
                                                            ┌────────────────────┐
                                                            │EmbroideryEstimation│
                                                            └────────────────────┘
```

---

## 3. Obstacles potentiels et risques

### - Qualité et résolution de l'image

**Problème :** Une image basse résolution ou floue produira des contours imprécis et des couleurs dégradées, rendant l'analyse peu fiable.

**Pistes de résolution :**
- Imposer une résolution minimale (ex. : 300 DPI, ou dimensions minimales en pixels)
- Informer l'utilisateur si l'image est en dessous du seuil avec un avertissement explicite
- Appliquer un léger filtre de netteté avant analyse (optionnel)

---

### - Mélange de couleurs proches (anti-aliasing, dégradés)

**Problème :** Les images naturelles ou les dessins vectoriels exportés en bitmap contiennent souvent des pixels de transition entre deux couleurs. Ces pixels "intermédiaires" parasitent le comptage.

**Pistes de résolution :**
- Utiliser un algorithme de quantification de couleurs (k-means, médian cut) pour regrouper les nuances proches en une seule couleur représentative
- Laisser l'utilisateur ajuster le niveau de tolérance (ex. : "fusionner les couleurs à moins de X% de différence")
- Ignorer les pixels en bordure de zone (érosion morphologique) pour ne compter que les zones franches

---

### - Fond blanc / zones non brodées

**Problème :** L'image contient souvent un fond blanc (ou une couleur de fond) qui ne doit pas être brodé. Si on l'inclut dans l'analyse, on surestime massivement la surface.

**Pistes de résolution :**
- Détecter automatiquement la couleur dominante en bordure comme "fond"
- Permettre à l'utilisateur de désigner manuellement la couleur de fond à exclure
- Supporter les images avec fond transparent (PNG avec canal alpha)

---

### - Performances sur des images grandes

**Problème :** Une image haute résolution (ex. : 5000×5000 px) représente 25 millions de pixels à analyser, ce qui peut être lent côté serveur.

**Pistes de résolution :**
- Traiter l'analyse en tâche asynchrone (job queue type Celery, BullMQ…) avec notification à l'utilisateur quand c'est prêt
- Redimensionner l'image à une résolution de travail raisonnable (ex. : max 1500px de large) avant analyse, en conservant les proportions pour les calculs de surface
- Mettre en cache les résultats d'analyse pour éviter de recalculer si l'image n'a pas changé

---

### - Conversion pixels → surface réelle

**Problème :** Le calcul de la surface dépend des dimensions physiques réelles du motif, que l'utilisateur doit fournir. Une erreur de saisie fausse toutes les estimations.

**Pistes de résolution :**
- Rendre la saisie des dimensions physiques obligatoire et bien expliquée dans l'interface
- Proposer une valeur par défaut raisonnable (ex. : basée sur le DPI de l'image si disponible dans les métadonnées EXIF)
- Afficher un aperçu de la taille réelle pour que l'utilisateur puisse valider

---
