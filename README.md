# PE File Metadata Extractor

This project downloads PE (Portable Executable) files from an S3 bucket (using multithreading), extracts metadata from the files, and stores the metadata in a PostgreSQL database using PySpark. The project is containerized using Docker.
> **Notice:** Due to some Spark configuration issues, Spark implemented only the metadata extraction and database storing parts.

## Prerequisites

Before you begin, ensure you have met the following requirements:
- Docker
- Docker Compose
- Git

## Installation

1. **Clone the repository**
    ```bash
    git clone https://github.com/mirzayevio/PE-file-metadata-extraction.git
    ```
    ```bash
    cd PE-file-metadata-extraction
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

- **Run unit tests**
    ```bash
    make test
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


### Database UI

You can access the PostgreSQL Database UI using:
- URL: `http://localhost:9090`

### Spark UI

After running the application, you can monitor Spark jobs using the Spark UI:
- URL: `http://localhost:8080`


### References

- [https://github.com/erocarrera/pefile](https://github.com/erocarrera/pefile)
- [https://wiki.osdev.org/MZ](https://wiki.osdev.org/MZ)
- https://medium.com/@shreyash_tambe/mastering-malware-analysis-305b1c5efc27
- [https://medium.com/@suffyan.asad1/spark-essentials-a-guide-to-setting-up-packaging-and-running-pyspark-projects](https://medium.com/@suffyan.asad1/spark-essentials-a-guide-to-setting-up-packaging-and-running-pyspark-projects-2eb2a27523a3)
- [https://spark.apache.org/docs/latest/api/python/user_guide/python_packaging.html](https://spark.apache.org/docs/latest/api/python/user_guide/python_packaging.html)
- [https://dev.to/mvillarrealb/creating-a-spark-standalone-cluster-with-docker-and-docker-compose-2021-update-6l4](https://dev.to/mvillarrealb/creating-a-spark-standalone-cluster-with-docker-and-docker-compose-2021-update-6l4)
- [https://github.com/mvillarrealb/docker-spark-cluster](https://github.com/mvillarrealb/docker-spark-cluster)
- [https://stackoverflow.com/questions/36461054/i-cant-seem-to-get-py-files-on-spark-to-work](https://stackoverflow.com/questions/36461054/i-cant-seem-to-get-py-files-on-spark-to-work)
- [https://medium.com/@MarinAgli1/setting-up-a-spark-standalone-cluster-on-docker-in-layman-terms-8cbdc9fdd14b](https://medium.com/@MarinAgli1/setting-up-a-spark-standalone-cluster-on-docker-in-layman-terms-8cbdc9fdd14b)
- [https://medium.com/@suffyan.asad1/writing-to-databases-using-jdbc-in-apache-spark-9a0eb2ce1a](https://medium.com/@suffyan.asad1/writing-to-databases-using-jdbc-in-apache-spark-9a0eb2ce1a)
