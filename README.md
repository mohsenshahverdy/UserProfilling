# User Profiling System

## Introduction
The User Profiling System is a FastAPI-based application designed to analyze user data and provide insights based on various demographic and interaction features. This system can filter users based on gender, occupation, region, income, age, and interests, offering a powerful tool for user segmentation and profiling. Also, This system can offer best targted users for advertising campigain in 6 provided topics with different confidence levels.


## Features
- FastAPI for API endpoints: Provides a robust and efficient API framework.
- Pandas for data processing: Efficient data handling and processing.
- Docker support: Containerize the application for easy deployment.
- Unit testing with pytest: Ensure code reliability and robustness.
- Git integration: Version control with Git and GitHub.

## Table of Contents
- Installation
- Usage
- API Endpoints
- Testing
- Docker
- Contributing


## Installation
### Prerequisites
- Python 3.9 or higher
- Docker (optional, for containerization)
- Git

### Clone the Repository
```bash
git clone https://github.com/mohsenshahverdy/UserProfilling.git
cd UserProfilling
```

### Create a Virtual Environment
```bash
python3 -m venv env
source env/bin/activate  # On Windows use `env\Scripts\activate`
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

## Usage
### Running the Application
To run the application locally, use:
```bash
uvicorn app.main:app --reload
```

## API Endpoints
The main API endpoint for creating target users is:

- POST /target-users/

### Example Request

```bash
import requests

url = 'http://localhost:8000/target-users/'
data = {
    "user_data": {
        "gender": "Male",
        "occupation": ["Engineer"],
        "city": ["Milan", "Roma"],
        "income": [50000, 100000],
        "age": [25, 35],
        "interest": {
            "interests": ["Technology", "Fashion"],
            "weights": [0.7, 0.3]
        },
        "n_users": 50,
        "confidence_level": "High"
    }
}

response = requests.post(url, json=data)
print(response.json())
```

## Testing
### Running Unit Tests
To run the unit tests, use:

```bash
pytest
```

## Docker
### Building the Docker Image
To build the Docker image, run:
```bash
docker build -t user-profiling-app .
```

### Running the Docker Container
To run the Docker container, use:
```bash
docker build -t user-profiling-app .
```

## Contributing
Contributions are welcome! Please fork the repository and submit a pull request for any enhancements or bug fixes.
