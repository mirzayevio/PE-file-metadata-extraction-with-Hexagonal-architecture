# Targets
.PHONY: all docker-up docker-down clean run


help:
	@echo "--------------- HELP ---------------"
	@echo "To build and start Docker containers -> make all"
	@echo "To build and start Docker containers in detached mode -> make docker-up"
	@echo "To stop and remove Docker containers -> make docker-down"
	@echo "To run the application interactively using docker-compose -> make run"
	@echo "To stop and remove Docker containers, images, volumes, and networks. -> make clean"
	@echo "------------------------------------"

# Default target
all: docker-up

# Build and bring up Docker containers
docker-up:
	@echo "Building and starting Docker containers..."
	docker-compose up --build -d

# Bring down Docker containers
docker-down:
	@echo "Stopping Docker containers..."
	docker-compose down

# Run application using docker-compose
run:
	@echo "Running application..."
	docker-compose run app

# Clean up Docker images/containers
clean:
	@echo "Cleaning up..."
	docker-compose down --rmi all --volumes --remove-orphans
