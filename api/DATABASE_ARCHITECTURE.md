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
    status VARCHAR(20) NOT NULL DEFAULT 'creating',
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
    name VARCHAR(255) NOT NULL,
    dataset_id INTEGER REFERENCES datasets(id),
    created_at TIMESTAMP DEFAULT now(),
    updated_at TIMESTAMP DEFAULT now()
);
```

### 4. **annotations**

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
Dataset (1) ←→ (N) Label
Image (1) ←→ (N) Annotation
Label (1) ←→ (N) Annotation
```

### Relations détaillées :

- **Dataset → Images** : Un dataset contient plusieurs images
- **Dataset → Labels** : Un dataset définit plusieurs labels possibles
- **Image → Annotations** : Une image peut avoir plusieurs annotations
- **Label → Annotations** : Un label peut être utilisé dans plusieurs annotations

## Contraintes et Règles

### Contraintes de cohérence :

1. **Label cohérence** : Un `label_id` dans `annotations` doit appartenir au même dataset que l'`image_id`
2. **Cascade delete** :
   - Supprimer un dataset → supprime toutes ses images et labels
   - Supprimer une image → supprime toutes ses annotations
   - Supprimer un label → supprime toutes ses annotations

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

# 2. Créer les labels
labels = [
    Label(name="voiture", dataset_id=dataset.id),
    Label(name="camion", dataset_id=dataset.id),
    Label(name="moto", dataset_id=dataset.id)
]
db.add_all(labels)
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
labels = db.query(Label).filter(Label.dataset_id == dataset_id).all()

# Vérifier qu'un label appartient au même dataset qu'une image
valid_annotation = db.query(Annotation).join(Image).join(Label).filter(
    Annotation.image_id == image_id,
    Annotation.label_id == label_id,
    Image.dataset_id == Label.dataset_id
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
