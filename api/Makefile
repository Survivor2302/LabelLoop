# Makefile pour LabelLoop API

# Variables
IMAGE_NAME = labelloop-api
CONTAINER_NAME = labelloop-api-dev
PORT = 8000

# Commande par défaut
.DEFAULT_GOAL := help

# Aide
help:
	@echo "Commandes disponibles:"
	@echo "  make build  - Construit l'image Docker"
	@echo "  make run    - Lance le conteneur et suit les logs"
	@echo "  make dev    - Construit et lance le conteneur (build + run)"
	@echo "  make stop   - Arrête le conteneur"
	@echo "  make clean  - Supprime l'image et le conteneur"

# Construire l'image Docker
build:
	@echo "🔨 Construction de l'image Docker..."
	docker build -f Dockerfile.dev -t $(IMAGE_NAME) .

# Lancer le conteneur et suivre les logs
run:
	@echo "🚀 Lancement du conteneur..."
	docker run --rm -d --name $(CONTAINER_NAME) -p $(PORT):8000 $(IMAGE_NAME)
	@echo "📋 Suivi des logs (Ctrl+C pour arrêter)..."
	@trap 'docker stop $(CONTAINER_NAME)' INT; docker logs -f $(CONTAINER_NAME)

# Développement : build + run
dev: build run

# Arrêter le conteneur
stop:
	@echo "🛑 Arrêt du conteneur..."
	-docker stop $(CONTAINER_NAME)

# Nettoyer (supprimer image et conteneur)
clean: stop
	@echo "🧹 Nettoyage..."
	-docker rmi $(IMAGE_NAME)
	-docker rm $(CONTAINER_NAME)

# Phony targets
.PHONY: help build run dev stop clean
