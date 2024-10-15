# 1.  FastAPI AWS Lambda Application

This project is a FastAPI application designed to run on AWS Lambda. The application utilizes Docker for containerization and Pulumi for infrastructure management. 

## Table of Contents

1. [Features](#features)
2. [Architecture](#architecture)
3. [Technologies Used](#technologies-used)
4. [Prerequisites](#prerequisites)
5. [Setup and Installation](#setup-and-installation)
6. [Running the Application](#running-the-application)
7. [Deployment](#deployment)
8. [API Endpoints](#api-endpoints)
9. [Configuration](#configuration)


## Features

- RESTful API built with FastAPI.
- Containerized using Docker for easy deployment and scalability.
- Deployed on AWS Lambda to minimize costs and optimize performance.
- Managed infrastructure with Pulumi, allowing for easy updates and version control.

## Architecture

The application is structured as follows:

- **FastAPI**: Framework for building the RESTful API.
- **Docker**: Used to create a container image for deployment.
- **AWS Lambda**: Serverless compute service for running the application.
- **Amazon ECR**: Managed Docker container registry to store Docker images.
- **Pulumi**: Infrastructure as Code (IaC) tool to define and manage cloud resources.

## Technologies Used

- Python 3.8
- FastAPI 0.95.2
- Uvicorn 0.22.0
- Docker
- Pulumi
- AWS Lambda
- Amazon ECR

## Prerequisites

Before you begin, ensure you have met the following requirements:

- [Python 3.8](https://www.python.org/downloads/)
- [Docker](https://docs.docker.com/get-docker/)
- [Pulumi](https://pulumi.com/docs/get-started/install/)
- [AWS CLI](https://aws.amazon.com/cli/)
- An AWS account with permissions to create Lambda functions and ECR repositories.

## Setup and Installation

1. **Clone the Repository**:
   ```bash
   git clone <repository-url>
   cd dev/ap-southeast-1/lambda-webhook

2. **Create Python env**:
   ```python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`

3. **Install packages**:
   ```
   pip install -r requirements.txt

## Running the Application
1. **Build the Docker Image**:
   ```
   docker build -t my-fastapi-app .

2. **Run the Docker Container**:
   ```
   docker run -d -p 8080:8080 my-fastapi-app

3. **Access the App**:
    ```
    http://localhost:8080

## Deployment
1. **Authenticate Docker to ECR**:
   ```
   aws ecr get-login-password --region <your-region> | docker login --username AWS --password-stdin <your-account-id>.dkr.ecr.<your-region>.amazonaws.com

2. **Tag the Docker Image**:
   ```
   docker tag my-fastapi-app:latest <your-account-id>.dkr.ecr.<your-region>.amazonaws.com/my-fastapi-repo:latest

3. **Push the Image to ECR**:
   ```
   docker push <your-account-id>.dkr.ecr.<your-region>.amazonaws.com/my-fastapi-repo:latest

4. **Deploy with Pulumi**:
   ```
   pulumi up

## API Endpoints
The application exposes the following endpoints:

- GET /: Returns a welcome message.
- GET /items/{item_id}: Retrieves an item by its ID.
- GET /items?query={query}: Searches for items based on the provided query.

## Configuration
You can configure the application by setting environment variables in your AWS Lambda settings or modifying the app.py file.


### Notes:
- Replace `yourusername` and `your-repo` with your actual GitHub username and repository name.
- Update `<your-region>` and `<your-account-id>` with your actual AWS region and account ID where applicable.




