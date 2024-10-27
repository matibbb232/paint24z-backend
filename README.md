# Backend for PAINT2024Z e-commerce app
WIP

## Installation

1. Clone the repo:
```
https://gitlab-stud.elka.pw.edu.pl/paint24z/Backend.git
```

2. Create virtual environment:
```
python3 -m venv .venv
```

3. Activate virtual envirnoment and install requirements:
```
source .venv/bin/activate
pip3 install -r requirements.txt
```

### Usage

1. Start Django server
```
python3 src/manage.py runserver
```

2. Open localhost `http://localhost:8000/` in browser

## Running Django app using Docker container

```
docker build -t paint-backend .
docker run -it -p 8000:8000 paint-backend
```

<!-- Should add frontend here -->
## Runing with nginx as a server using Docker compose
```
docker-compose up --build
```
Then connect to localhost on port 80.