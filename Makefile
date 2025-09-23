# Makefile pour LabelLoop - Développement

# Variables
COMPOSE_FILE = docker-compose.dev.yml

# Commande par défaut
.DEFAULT_GOAL := help

# Aide
help:
	@echo "Commandes disponibles:"
	@echo "  make dev      - Construit et lance tous les services de développement"
	@echo "  make build    - Construit tous les services"
	@echo "  make up       - Lance tous les services en arrière-plan"
	@echo "  make logs     - Affiche les logs de tous les services"
	@echo "  make down     - Arrête tous les services"
	@echo "  make clean    - Arrête et supprime tous les conteneurs, réseaux et volumes"
	@echo "  make restart  - Redémarre tous les services"
	@echo "  make infra        - Construit + lance Postgres & MinIO + logs"
	@echo "  make infra-up     - Lance Postgres & MinIO en arrière-plan"
	@echo "  make infra-down   - Arrête Postgres & MinIO"
	@echo "  make infra-logs   - Affiche les logs de Postgres & MinIO"
	@echo "  make clean-infra  - Nettoie Postgres & MinIO (images + volumes + données locales)"

# Développement : build + up + logs
dev: build up logs

# Construire tous les services
build:
	@echo "🔨 Construction de tous les services..."
	docker-compose -f $(COMPOSE_FILE) build

# Lancer tous les services en arrière-plan
up:
	@echo "🚀 Lancement de tous les services..."
	docker-compose -f $(COMPOSE_FILE) up -d

# Lancer tous les services en premier plan
up-foreground:
	@echo "🚀 Lancement de tous les services (premier plan)..."
	docker-compose -f $(COMPOSE_FILE) up

# Afficher les logs
logs:
	@echo "📋 Suivi des logs (Ctrl+C pour arrêter)..."
	@trap 'make down' INT; docker-compose -f $(COMPOSE_FILE) logs -f

# Afficher les logs de l'API
logs-api:
	@echo "📋 Logs de l'API..."
	docker-compose -f $(COMPOSE_FILE) logs -f api

# Afficher les logs du webapp
logs-webapp:
	@echo "📋 Logs du webapp..."
	docker-compose -f $(COMPOSE_FILE) logs -f webapp

# Arrêter tous les services
down:
	@echo "🛑 Arrêt de tous les services..."
	docker-compose -f $(COMPOSE_FILE) down

# Nettoyer (arrêter et supprimer tout)
clean: down
	@echo "🧹 Nettoyage complet..."
	docker-compose -f $(COMPOSE_FILE) down -v --remove-orphans
	docker system prune -f

# Redémarrer tous les services
restart:
	@echo "🔄 Redémarrage de tous les services..."
	docker-compose -f $(COMPOSE_FILE) restart

# Infrastructure seulement (Postgres + MinIO)
infra: infra-build infra-up infra-logs

infra-build:
	@echo "🔨 Construction de Postgres & MinIO..."
	docker-compose -f $(COMPOSE_FILE) build postgres minio

infra-up:
	@echo "🚀 Lancement de Postgres & MinIO..."
	docker-compose -f $(COMPOSE_FILE) up -d postgres minio

infra-logs:
	@echo "📋 Suivi des logs (Ctrl+C pour arrêter Postgres & MinIO)..."
	@trap 'make infra-down' INT; docker-compose -f $(COMPOSE_FILE) logs -f postgres minio

infra-down:
	@echo "🛑 Arrêt de Postgres & MinIO..."
	-docker-compose -f $(COMPOSE_FILE) stop postgres minio
	-docker-compose -f $(COMPOSE_FILE) rm -f postgres minio

# Nettoyer Postgres & MinIO (images + volumes + données locales)
clean-infra:
	@echo "🧹 Nettoyage de Postgres & MinIO..."
	@echo "⚠️  ATTENTION: Cela supprimera toutes les données Postgres et MinIO !"
	@read -p "Êtes-vous sûr ? (y/N): " confirm && [ "$$confirm" = "y" ] || exit 1
	@echo "🛑 Arrêt des services Postgres & MinIO..."
	-docker-compose -f $(COMPOSE_FILE) stop postgres minio
	-docker-compose -f $(COMPOSE_FILE) rm -f postgres minio
	@echo "🗑️  Suppression des images Postgres & MinIO..."
	-docker rmi postgres:15-alpine
	-docker rmi minio/minio:latest
	@echo "🗑️  Suppression des volumes Docker..."
	-docker volume rm labelloop_postgres_data 2>/dev/null || true
	-docker volume rm labelloop_minio_data 2>/dev/null || true
	@echo "🗑️  Suppression des dossiers de données locaux..."
	-rm -rf ./data/postgres
	-rm -rf ./data/minio
	@echo "✅ Nettoyage Postgres & MinIO terminé !"

# Phony targets
.PHONY: help dev build up up-foreground logs logs-api logs-webapp down clean restart infra infra-build infra-up infra-logs infra-down clean-infra
