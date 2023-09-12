# Project setup
This project assumes that you have kubectl, minikube and Docker installed
## Kubernetes/Minikube
1. Build the Docker image `docker build -t my-fastapi-app .`
2. Run kubectl commands:
    ```bash
    kubectl apply -f configs/mongo-config.yaml
    kubectl apply -f configs/mongo-secret.yaml
    kubectl apply -f mongo.yaml
    kubectl apply -f api.yaml
    ```
3. Run `minikube tunnel` on a separate terminal
4. Access api through external IP

## Local Development
For local development, `mongodb` should be installed and running.
1. Create virtualenv `python3 -m venv .venv`
2. Activate virtualenv `.venv/bin/activate`
3. Install requirements.txt `pip install -r requirements.txt`
4. Add `DB_URL` env var `export DB_URL=127.0.0.1`
5. Add `SECRET_KEY` env var `export SECRET_KEY=asdhaksdhask213`
5. Add `SALT_KEY` env var `export SALT_KEY=5gz`
6. Run the app `uvicorn api.main:app --reload --port 8000`
7. Access api through localhost:8000

To generate a random secret key, you can run:
`openssl rand -hex 32`