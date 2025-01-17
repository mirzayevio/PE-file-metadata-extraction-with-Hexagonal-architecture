# Targets
.PHONY: all docker-up docker-down clean run


help:
	@echo "--------------- HELP ---------------"
	@echo "To build and start Docker containers in detached mode -> make up"
	@echo "To stop and remove Docker containers -> make down"
	@echo "To run the application interactively using docker-compose -> make run"
	@echo "To run the unit tests -> make test"
	@echo "To stop and remove Docker containers, images, volumes, and networks. -> make clean"
	@echo "------------------------------------"


# Build and bring up Docker containers
up:
	@echo "Building and starting Docker containers..."
	docker-compose up --build -d

# Bring down Docker containers
down:
	@echo "Stopping Docker containers..."
	docker-compose down

# Run application using docker-compose
run:
	@echo "Running application..."
	docker-compose run app

# Run tests
test:
	@echo "Running application..."
	docker-compose exec app pytest

# Clean up Docker images/containers
clean:
	@echo "Cleaning up..."
	docker-compose down --rmi all --volumes --remove-orphans
