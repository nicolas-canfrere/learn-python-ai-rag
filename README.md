# Simple AI RAG in Python

## Requirements

- docker and docker-compose
- python ^3.12
- make

## How to run

### Install
- clone the repository

then :

```bash
## copy .env.dist to .env
make copy-env

## then edit the .env file to set the right value for OLLAMA_MODELS_VOLUME

## the virtual environment is created in the .venv directory
make venv
make activate-env
## Start docker-compose
make up
## install dependencies
make install
```

### Access to Chromadb openapi

In your browser, go to [http://127.0.0.1:9999/docs](http://127.0.0.1:9999/docs)

### Access Ollama with curl

```bash
curl -X POST http://localhost:11434/api/chat -d '{"model":"llama3.2:3b-instruct-q8_0","messages":[{"role":"user","content":"why is the sky blue?"}],"stream": false}'
  
```


### create embeddings

```bash
## it takes a while !!
make embeddings
``` 