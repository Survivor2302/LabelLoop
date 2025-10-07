# 📸 Image Upload Workflow - Presigned URLs

## 🎯 Architecture

Ce système utilise des **Presigned URLs** pour permettre l'upload direct des images du frontend vers S3/MinIO, sans passer par l'API.

### Avantages

- ✅ **Performance**: Upload direct vers S3, pas de transit par l'API
- ✅ **Scalabilité**: Pas de limite de bande passante côté API
- ✅ **Sécurité**: URLs temporaires (expirent après 1 heure)
- ✅ **Batch**: Support de l'upload multiple en parallèle

## 🔄 Workflow Complet

### 1️⃣ Préparer l'upload (Frontend → API)

**Endpoint**: `POST /datasets/{dataset_id}/images/prepare-upload`

**Request**:

```json
{
  "files": [
    {
      "filename": "car1.jpg",
      "file_size": 1024000,
      "mime_type": "image/jpeg"
    },
    {
      "filename": "car2.jpg",
      "file_size": 2048000,
      "mime_type": "image/jpeg"
    }
  ]
}
```

**Response**:

```json
{
  "uploads": [
    {
      "image_id": 1,
      "upload_url": "https://minio:9000/datasets/...?signature=...",
      "s3_key": "datasets/123/images/uuid_car1.jpg",
      "expires_in": 3600
    },
    {
      "image_id": 2,
      "upload_url": "https://minio:9000/datasets/...?signature=...",
      "s3_key": "datasets/123/images/uuid_car2.jpg",
      "expires_in": 3600
    }
  ]
}
```

**Côté backend**:

- ✅ Crée les enregistrements en DB avec `status = "uploading"`
- ✅ Génère des clés S3 uniques avec UUID
- ✅ Génère les presigned URLs (valables 1h)

---

### 2️⃣ Upload vers S3 (Frontend → S3)

Le frontend upload **directement** vers S3 avec les URLs signées :

```javascript
// Exemple JavaScript
const uploadFile = async (file, uploadUrl) => {
  const response = await fetch(uploadUrl, {
    method: "PUT",
    body: file,
    headers: {
      "Content-Type": file.type,
    },
  });
  return response.ok;
};

// Upload en parallèle
const uploads = await Promise.all(
  uploadData.uploads.map(async ({ image_id, upload_url }) => {
    const file = files.find((f) => f.name === filename);
    const success = await uploadFile(file, upload_url);
    return { image_id, success };
  })
);
```

---

### 3️⃣ Confirmer les uploads (Frontend → API)

**Endpoint**: `POST /datasets/{dataset_id}/images/confirm-upload`

**Request**:

```json
{
  "image_ids": [1, 2]
}
```

**Response**:

```json
{
  "message": "Successfully confirmed 2 uploads",
  "updated_count": 2,
  "total_requested": 2
}
```

**Côté backend**:

- ✅ Vérifie que les fichiers existent dans S3
- ✅ Met à jour `status = "uploaded"`
- ✅ Si fichier absent → `status = "error"`

---

## 📋 Status des Images

| Status      | Description                              |
| ----------- | ---------------------------------------- |
| `uploading` | Enregistrement créé, upload en cours     |
| `uploaded`  | Upload confirmé et vérifié dans S3       |
| `error`     | Échec de l'upload ou fichier introuvable |

---

## 🔗 Autres Endpoints

### Lister les images d'un dataset

```http
GET /datasets/{dataset_id}/images?skip=0&limit=100&status=uploaded
```

**Note**: Retourne les images **sans** URLs de téléchargement.

---

### 🔥 Lister les images AVEC URLs de téléchargement (Recommandé)

```http
GET /datasets/{dataset_id}/images/with-urls?skip=0&limit=100&status=uploaded&expires_in=3600
```

**Response**:

```json
[
  {
    "id": 1,
    "filename": "car1.jpg",
    "s3_key": "datasets/123/images/uuid_car1.jpg",
    "file_size": 1024000,
    "mime_type": "image/jpeg",
    "width": 1920,
    "height": 1080,
    "status": "uploaded",
    "dataset_id": 123,
    "created_at": "2025-10-02T10:00:00Z",
    "updated_at": "2025-10-02T10:01:00Z",
    "download_url": "https://minio:9000/datasets/...?signature=...",
    "url_expires_in": 3600
  },
  {
    "id": 2,
    "filename": "car2.jpg",
    "s3_key": "datasets/123/images/uuid_car2.jpg",
    "file_size": 2048000,
    "mime_type": "image/jpeg",
    "width": null,
    "height": null,
    "status": "uploading",
    "dataset_id": 123,
    "created_at": "2025-10-02T10:02:00Z",
    "updated_at": "2025-10-02T10:02:00Z",
    "download_url": null,
    "url_expires_in": null
  }
]
```

**Avantages**:

- ✅ **Évite N+1 requêtes** : Génère toutes les URLs en une seule requête
- ✅ **Performance** : Optimisé pour afficher des galeries d'images
- ✅ **URLs présignées** : Téléchargement direct depuis S3
- ✅ **Smart** : URLs générées uniquement pour les images avec `status=uploaded`

---

### Détails d'une image

```http
GET /images/{image_id}
```

### Générer un lien de téléchargement

```http
GET /images/{image_id}/download-url?expires_in=3600
```

**Response**:

```json
{
  "download_url": "https://minio:9000/datasets/...?signature=...",
  "expires_in": 3600
}
```

### Mettre à jour une image

```http
PATCH /images/{image_id}
```

**Body**:

```json
{
  "width": 1920,
  "height": 1080,
  "status": "uploaded"
}
```

### Supprimer une image

```http
DELETE /images/{image_id}
```

**Note**: Supprime l'image de la DB **ET** de S3.

---

## 🔐 Configuration S3

Les méthodes suivantes sont disponibles dans `app.core.s3.s3_client`:

- `generate_presigned_upload_url(s3_key, content_type, expires_in=3600)`
  → Génère une URL signée pour upload (PUT)

- `generate_presigned_download_url(s3_key, expires_in=3600)`
  → Génère une URL signée pour download (GET)

- `delete_file(s3_key)`
  → Supprime un fichier de S3

- `file_exists(s3_key)`
  → Vérifie si un fichier existe dans S3

---

## 📦 Format des clés S3

Format: `datasets/{dataset_id}/images/{uuid}_{filename}`

Exemple: `datasets/123/images/a1b2c3d4-...-e5f6/car_front.jpg`

---

## ⚠️ Gestion des erreurs

### Upload échoué côté frontend

→ Ne pas appeler `/confirm-upload` pour cette image
→ Elle restera en status `uploading`

### Cleanup automatique (TODO)

- Implémenter un job CRON pour supprimer les images en status `uploading` depuis > 24h
- Permet de nettoyer les uploads abandonnés

---

## 🧪 Test manuel avec curl

### 1. Préparer l'upload

```bash
curl -X POST http://localhost:8000/datasets/1/images/prepare-upload \
  -H "Content-Type: application/json" \
  -d '{
    "files": [{
      "filename": "test.jpg",
      "file_size": 1024,
      "mime_type": "image/jpeg"
    }]
  }'
```

### 2. Upload vers S3

```bash
curl -X PUT "PRESIGNED_URL" \
  --upload-file test.jpg \
  -H "Content-Type: image/jpeg"
```

### 3. Confirmer l'upload

```bash
curl -X POST http://localhost:8000/datasets/1/images/confirm-upload \
  -H "Content-Type: application/json" \
  -d '{
    "image_ids": [1]
  }'
```

---

## 🚀 Prochaines étapes

1. ✅ Architecture presigned URLs implémentée
2. ✅ Route optimisée pour récupérer images + URLs en une requête
3. ⬜ Implémenter le frontend (React/Next.js)
4. ⬜ Ajouter validation des types MIME autorisés
5. ⬜ Ajouter limite de taille par image (ex: 10MB max)
6. ⬜ Implémenter job de cleanup des uploads abandonnés
7. ⬜ Ajouter extraction automatique des dimensions (width/height)
8. ⬜ Ajouter support de la génération de thumbnails
