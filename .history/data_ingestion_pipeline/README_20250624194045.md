# Data Ingestion Pipeline

This directory contains the Data Ingestion Pipeline for the DoubtMate application suite.

## Docker Compose Management
Below are the main commands to manage your Docker Compose containers and data:

---

### 1. Start safely
Brings up the containers in detached mode, preserving data.
```
docker-compose up -d
```
- Container: Preserved
- Data: Preserved

---

### 2. Stop safely
Stops the containers without removing them or the data.
```
docker-compose stop
```
- Container: Preserved
- Data: Preserved

---

### 3. Resume after stop
Restarts stopped containers, data remains intact.
```
docker-compose start
```
- Container: Preserved
- Data: Preserved

---

### 4. Stop and remove container
Stops and removes containers, but keeps data volumes.
```
docker-compose down
```
- Container: Removed
- Data: Preserved

---

### 5. Full wipe (dangerous)
Stops and removes containers and deletes all data volumes. Use with caution!
```
docker-compose down -v
```
- Container: Removed
- Data: Removed

---

## Directory Structure
- `docker-compose.yml`: Docker Compose configuration for the pipeline.
- `main.py`: Main entry point for the data ingestion process.
- `src/`: Source code for modules, agents, and helpers.
- `test/`: Test cases for the pipeline.

## Usage
1. Clone the repository.
2. Navigate to the `data_ingestion_pipeline` directory.
3. Use the commands above to manage your pipeline containers.

## Requirements
- Docker & Docker Compose
- Python (see `requirements.txt` for dependencies)

## License
This project is part of the DoubtMate application suite.
