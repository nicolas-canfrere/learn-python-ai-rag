.PHONY: make-env activate-env deactivate-env up install embed

venv: .venv
	python3 -m venv .venv

activate-env: .venv
	source .venv/bin/activate

deactivate-env: .venv
	deactivate

copy-env:
	cp .env.dist .env

up:
	docker compose up -d

install_models:
	docker compose exec -it ollama ollama pull nomic-embed-text
	docker compose exec -it ollama ollama pull llama3.2:3b-instruct-q8_0

install_requirements: .venv
	pip install -r requirements.txt

install:
	$(MAKE) install_models
	$(MAKE) install_requirements

embeddings:
	.venv/bin/python document_database/main.py