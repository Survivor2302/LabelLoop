# Database Architecture

## Overview

LabelLoop utilise une architecture de base de données relationnelle avec 4 tables principales pour gérer les datasets d'images et leurs annotations.

## Tables et Relations

### 1. **datasets**

```sql
CREATE TABLE datasets (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT now(),
    updated_at TIMESTAMP DEFAULT now()
);
```

### 2. **images**

```sql
CREATE TABLE images (
    id SERIAL PRIMARY KEY,
    filename VARCHAR(255) NOT NULL,
    s3_key VARCHAR(500) NOT NULL UNIQUE,
    file_size INTEGER NOT NULL,
    mime_type VARCHAR(100) NOT NULL,
    width INTEGER,
    height INTEGER,
    dataset_id INTEGER REFERENCES datasets(id),
    created_at TIMESTAMP DEFAULT now(),
    updated_at TIMESTAMP DEFAULT now()
);
```

### 3. **labels**

```sql
CREATE TABLE labels (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT now(),
    updated_at TIMESTAMP DEFAULT now()
);
```

### 4. **dataset_labels** (table de liaison)

```sql
CREATE TABLE dataset_labels (
    dataset_id INTEGER REFERENCES datasets(id),
    label_id INTEGER REFERENCES labels(id),
    PRIMARY KEY (dataset_id, label_id)
);
```

### 5. **annotations**

```sql
CREATE TABLE annotations (
    id SERIAL PRIMARY KEY,
    image_id INTEGER REFERENCES images(id),
    label_id INTEGER REFERENCES labels(id),
    bbox_xmin INTEGER,
    bbox_ymin INTEGER,
    bbox_xmax INTEGER,
    bbox_ymax INTEGER,
    created_at TIMESTAMP DEFAULT now()
);
```

## Relations

```
Dataset (1) ←→ (N) Image
Dataset (N) ←→ (N) Label (via dataset_labels)
Image (1) ←→ (N) Annotation
Label (1) ←→ (N) Annotation
```

### Relations détaillées :

- **Dataset → Images** : Un dataset contient plusieurs images
- **Dataset ↔ Labels** : Relation many-to-many via la table `dataset_labels`
- **Image → Annotations** : Une image peut avoir plusieurs annotations
- **Label → Annotations** : Un label peut être utilisé dans plusieurs annotations

## Contraintes et Règles

### Contraintes de cohérence :

1. **Label unique** : Le nom des labels est unique dans toute la base
2. **Cascade delete** :
   - Supprimer un dataset → supprime toutes ses images et les liens avec les labels
   - Supprimer une image → supprime toutes ses annotations
   - Supprimer un label → supprime toutes ses annotations et les liens avec les datasets

### Optimisations :

1. **Indexes** : Index sur les clés étrangères et champs de recherche fréquents
2. **Cascade** : Suppression en cascade pour maintenir l'intégrité
3. **Relations pures** : Utilisation des relations SQLAlchemy pour accéder aux données

## Exemples d'utilisation

### Créer un dataset avec labels :

```python
# 1. Créer le dataset
dataset = Dataset(name="Voitures", description="Dataset de voitures")
db.add(dataset)
db.commit()

# 2. Créer ou récupérer les labels
labels = []
for name in ["voiture", "camion", "moto"]:
    label = db.query(Label).filter(Label.name == name).first()
    if not label:
        label = Label(name=name)
        db.add(label)
        db.commit()
    labels.append(label)

# 3. Associer les labels au dataset
dataset.labels.extend(labels)
db.commit()
```

### Annoter une image :

```python
# 1. Récupérer l'image et le label
image = db.query(Image).filter(Image.id == image_id).first()
label = db.query(Label).filter(Label.id == label_id).first()

# 2. Créer l'annotation
annotation = Annotation(
    image_id=image.id,
    label_id=label.id,
    bbox_xmin=100,
    bbox_ymin=50,
    bbox_xmax=300,
    bbox_ymax=200
)
db.add(annotation)
db.commit()
```

### Requêtes typiques :

```python
# Toutes les annotations d'une image avec leurs labels
annotations = db.query(Annotation).options(
    joinedload(Annotation.label_obj)
).filter(Annotation.image_id == image_id).all()

# Tous les labels d'un dataset
labels = db.query(Label).join(dataset_labels).filter(
    dataset_labels.c.dataset_id == dataset_id
).all()

# Vérifier qu'un label est associé au dataset d'une image
valid_annotation = db.query(Annotation).join(Image).join(Label).join(
    dataset_labels, Label.id == dataset_labels.c.label_id
).filter(
    Annotation.image_id == image_id,
    Annotation.label_id == label_id,
    Image.dataset_id == dataset_labels.c.dataset_id
).first()

# Accéder au nom du label via la relation
annotation = db.query(Annotation).options(
    joinedload(Annotation.label_obj)
).filter(Annotation.id == annotation_id).first()
label_name = annotation.label_obj.name
```

## Avantages de cette architecture

1. **Flexibilité** : Labels définis par dataset
2. **Intégrité** : Contraintes de cohérence entre dataset/label/image
3. **Évolutivité** : Structure extensible pour d'autres types d'annotations
4. **Simplicité** : Relations claires et logiques
5. **Normalisation** : Architecture relationnelle pure sans dénormalisation
