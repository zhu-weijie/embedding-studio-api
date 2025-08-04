# Embedding Studio API

Embedding Studio is a cloud-native FastAPI application for text processing and semantic search, featuring AWS Bedrock for embedding generation. It is deployed on AWS ECS with a complete CI/CD pipeline using GitHub Actions and Terraform for Infrastructure as Code.

## Features

- **Text Tokenization**: API endpoint to tokenize text using `tiktoken`.
- **Text & Embedding Storage**: Endpoints to create and manage text documents and their vector embeddings in a PostgreSQL database.
- **AI-Powered Embeddings**: Integrates with AWS Bedrock (`amazon.titan-embed-text-v2:0`) to generate high-quality vector embeddings.
- **Semantic Search**: Utilizes the `pgvector` extension in PostgreSQL to perform efficient cosine similarity searches.
- **Automated Deployments**: A full CI/CD pipeline ensures code quality and automatically deploys changes to AWS.

## Tech Stack

- **Backend**: Python 3.12, FastAPI
- **Database**: PostgreSQL with `pgvector`
- **Infrastructure**: AWS (ECS Fargate, RDS, ALB, VPC, ECR, S3 for state), Terraform
- **CI/CD**: GitHub Actions
- **Containerization**: Docker

## Running Locally

1.  **Clone the repository:**
    ```bash
    git clone <your-repo-url>
    cd embedding-studio-api
    ```

2.  **Set up environment files:**
    Create `.env.local` for running `alembic` locally and `.env.docker` for the containers.
    *   `.env.local` requires `POSTGRES_SERVER=localhost`.
    *   `.env.docker` requires `POSTGRES_SERVER=db`.
    *   Both require `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_DB`, `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, and `AWS_REGION`.

3.  **Start the services:**
    ```bash
    docker compose up --build
    ```
    The API will be available at `http://localhost:8000`.

4.  **Run database migrations (locally):**
    Ensure the Docker containers are running, then run:
    ```bash
    # Set up a virtual environment and install requirements.txt first
    alembic upgrade head
    ```

## API Endpoints

The API is available at `http://YOUR_ALB_DNS_NAME`.

- **`POST /api/v1/tokenize`**: Tokenizes a given text.
- **`POST /api/v1/texts`**: Creates a new text document.
- **`POST /api/v1/texts/{text_id}/embeddings`**: Generates and saves an embedding for a text.
- **`POST /api/v1/search`**: Performs semantic search on existing embeddings.

## Deployment

The application is deployed automatically via a GitHub Actions workflow (`.github/workflows/cd.yml`) on every push to the `main` branch. The workflow builds the Docker image, pushes it to ECR, and updates the ECS service.
