# PE File Metadata Extractor

This project downloads PE (Portable Executable) files from an S3 bucket, extracts metadata from the files, and stores the metadata in a PostgreSQL database using PySpark. The project is containerized using Docker.

## Prerequisites

Before you begin, ensure you have met the following requirements:
- Docker
- Docker Compose
- Git

## Installation

1. **Clone the repository**
    ```bash
    git clone https://github.com/mirzayevio/Nord-security-task.git
    cd nord-security-task
    ```

2. **Environment Variables**

    Copy the example environment file and update it with your configuration:
    ```bash
    cp .env.example .env
    ```

    Open the `.env` file in your preferred text editor and add the necessary environment variables:
    ```
    DB_USER="your_username"
    DB_PASSWORD="your_password"
    DB_NAME="nord"
    DB_HOST="db"
    DB_PORT="5432"
    ```

## Usage

### Running the Project

You can use the provided Makefile to manage Docker containers:

- **Build and start the containers**
    ```bash
    make up
    ```

- **Run the application**
    ```bash
    make run
    ```

- **Stop and remove the containers**
    ```bash
    make down
    ```


- **Clean up Docker images/containers**
    ```bash
    make clean
    ```

### Accessing the Database

Once the application is running, you can access the PostgreSQL database at:
- Host: `db`
- Port: `5432`
- Database: `nord`
- User: `your_username`
- Password: `your_password`

### Example Queries

You can run queries on the `metadata` table to retrieve extracted metadata:
```sql
SELECT * FROM metadata;
