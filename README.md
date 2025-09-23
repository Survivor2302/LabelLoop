# LabelLoop

Un monorepo complet pour une application de gestion d'étiquettes avec FastAPI (backend) et Next.js (frontend), orchestré avec Docker Compose.

## 🏗️ Architecture

```
LabelLoop/                           # Monorepo principal
├── api/                             # Backend FastAPI (Poetry)
│   ├── app/                         # Code applicatif (routes, modèles, services ML…)
│   │   └── main.py
│   ├── pyproject.toml               # Dépendances Poetry
│   ├── poetry.lock                  # Lock file Poetry
│   └── Dockerfile                   # Dockerfile pour FastAPI + Poetry
│
├── webapp/                          # Frontend Next.js
│   ├── public/                      # Assets statiques
│   ├── src/                         # Code source Next.js
│   │   ├── app/
│   │   ├── components/
│   │   └── lib/
│   ├── Dockerfile                   # Dockerfile pour Next.js
│   ├── package.json                 # Dépendances Node.js
│   └── tailwind.config.ts
│
├── data/                            # Stockage persistant (bind mounts)
│   ├── postgres/                    # bind mount pour Postgres (/var/lib/postgresql/data)
│   └── minio/                       # bind mount pour MinIO (/data)
│
├── docker-compose.yml               # Orchestration des containers
└── README.md                        # Documentation du projet
```

## 🚀 Services

- **PostgreSQL** (port 5432) : Base de données principale
- **MinIO** (ports 9000/9001) : Stockage d'objets (S3-compatible)
- **FastAPI** (port 8000) : API backend avec documentation Swagger
- **Next.js** (port 3000) : Interface utilisateur

## 🛠️ Prérequis

- Docker & Docker Compose
- Git

## 📦 Installation et Démarrage

1. **Cloner le repository**

   ```bash
   git clone <repository-url>
   cd LabelLoop
   ```

2. **Démarrer tous les services**

   ```bash
   docker-compose up -d
   ```

3. **Vérifier le statut des services**
   ```bash
   docker-compose ps
   ```

## 🌐 Accès aux Services

- **Frontend Next.js** : http://localhost:3000
- **API FastAPI** : http://localhost:8000
- **Documentation API** : http://localhost:8000/docs
- **MinIO Console** : http://localhost:9001
- **PostgreSQL** : localhost:5432

## 🔧 Développement

### Backend (FastAPI)

```bash
# Accéder au container API
docker-compose exec api bash

# Installer de nouvelles dépendances
poetry add <package-name>

# Lancer les migrations (si applicable)
poetry run alembic upgrade head
```

### Frontend (Next.js)

```bash
# Accéder au container webapp
docker-compose exec webapp sh

# Installer de nouvelles dépendances
npm install <package-name>
```

### Base de données

```bash
# Accéder à PostgreSQL
docker-compose exec postgres psql -U labelloop -d labelloop
```

### MinIO

- **Console** : http://localhost:9001
- **Credentials** : labelloop / labelloop_password

## 📁 Persistance des Données

Les données sont persistées via des bind mounts :

- **PostgreSQL** : `./data/postgres/` → `/var/lib/postgresql/data`
- **MinIO** : `./data/minio/` → `/data`

## 🔄 Commandes Utiles

```bash
# Démarrer en mode développement (avec logs)
docker-compose up

# Redémarrer un service spécifique
docker-compose restart <service-name>

# Voir les logs d'un service
docker-compose logs -f <service-name>

# Arrêter tous les services
docker-compose down

# Nettoyer les volumes (ATTENTION: supprime les données)
docker-compose down -v
```

## 🐛 Dépannage

### Problèmes de permissions (Linux/macOS)

```bash
# Donner les bonnes permissions aux dossiers de données
sudo chown -R 999:999 data/postgres
sudo chown -R 1000:1000 data/minio
```

### Rebuild des images

```bash
# Rebuild toutes les images
docker-compose build --no-cache

# Rebuild un service spécifique
docker-compose build --no-cache <service-name>
```

## 📝 Variables d'Environnement

Les variables d'environnement sont définies dans `docker-compose.yml` :

- `DATABASE_URL` : URL de connexion PostgreSQL
- `MINIO_ENDPOINT` : Endpoint MinIO
- `MINIO_ACCESS_KEY` / `MINIO_SECRET_KEY` : Credentials MinIO
- `NEXT_PUBLIC_API_URL` : URL de l'API pour le frontend

## 🤝 Contribution

1. Fork le projet
2. Créer une branche feature (`git checkout -b feature/AmazingFeature`)
3. Commit les changements (`git commit -m 'Add some AmazingFeature'`)
4. Push vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrir une Pull Request

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.
