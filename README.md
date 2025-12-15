# OCR AI Agent

## Steps to preparing enviroment

### Step 1

```
sudo apt install -y build-essential curl wget libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev
```

### Step 2

```
sudo apt update
```

### Step 3

```
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt install -y python3.13 python3.13-venv python3.13-dev python3-pip
```

### Step 4

```
python3.13 --version
pip3 --version
```

### Step 5

```
python3.13 -m pip install --upgrade pip setuptools wheel

```

### Step 6 DOCKER

```
sudo apt install -y apt-transport-https ca-certificates curl software-properties-common
```

### Step 7 DOCKER

```
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
```

### Step 8 DOCKER

```
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
```

### Step 9 DOCKER

```
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

```

### STEP 10 DOCKER

```
sudo systemctl start docker
sudo systemctl enable docker
```

### STEP 11 DOCKER

```
sudo usermod -aG docker $USER
newgrp docker

"next"
exit
"next"
su - $USER
```

### STEP 12 DOCKER

```
docker --version
docker run hello-world
```

### STEP 13 settings.json

```
{
  "python.defaultInterpreterPath": "/usr/bin/python3.13",
  "python.linting.enabled": true,
  "python.linting.pylintEnabled": true,
  "python.formatting.provider": "black",
  "python.linting.pylintArgs": [
    "--load-plugins=pylint_django"
  ],
  "[python]": {
    "editor.formatOnSave": true,
    "editor.defaultFormatter": "ms-python.python",
    "editor.rulers":
  },
  "python.testing.pytestEnabled": true,
  "python.testing.unittestEnabled": false,
  "editor.fontSize": 14,
  "editor.fontFamily": "Fira Code, monospace"
}
```

### STEP 14

```
pip install black pylint pytest
```

### STEP 15 TEST

1. Otwórz VSCode: code
2. Utwórz plik: test.py
3. Wpisz:

```
print("Python 3.13 works!")
print(f"Version: {__import__('sys').version}")
```

### 16 create virtualn enviroment

```
python3.13 -m venv venv
```

### 17 activate venv

```
source venv/bin/activate
```

### 18 upgrade

```
pip install --upgrade pip setuptools wheel
```

### 19 basic package

```
pip install python-dotenv requests aiohttp pydantic
```

### 20 Create requirements.txt

```
pip freeze > requirements.txt
```

### 21 VSCODE interpreter

1. Otwórz folder projektu w VSCode: code .
2. Naciśnij Ctrl+Shift+P
3. Wpisz: Python: Select Interpreter
4. Wybierz ./venv/bin/python

### 22 Bielik integration

```
pip install bielik-composer
```

### 23 optional env

```
cat > .env << EOF
BIELIK_API_KEY=your_key_here
BIELIK_API_URL=https://api.bielik.ai
ADK_PROJECT_ID=your_project_id
EOF
```

### 24 Install ADK

```
pip install anthropic langchain langchain-community
```

#### (optional) OTHER SDK

- `pip install openai`
- `pip install anthropic`
- `pip install langchain langchain-community langsmith`

### 25 Agent files structure

```
mkdir -p src/agents src/tools src/models src/utils tests
touch src/__init__.py src/agents/__init__.py src/tools/__init__.py
touch src/main.py .env .gitignore
```

### 26 EXAMPLES

- Bielik agent: src/main.py

```
import os
from dotenv import load_dotenv
from bielik_composer import BielikAgent

load_dotenv()

class MyAIAgent:
    def __init__(self):
        self.agent = BielikAgent(
            api_key=os.getenv("BIELIK_API_KEY")
        )

    async def run(self, prompt: str) -> str:
        response = await self.agent.execute(prompt)
        return response

if __name__ == "__main__":
    agent = MyAIAgent()
    # Użyj w asyncio
    import asyncio
    result = asyncio.run(agent.run("Cześć! Co potrafisz zrobić?"))
    print(result)
```

- Dockerfile for agent

```
FROM python:3.13-slim

WORKDIR /app

# Instalacja zależności systemowych
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Kopowanie requirements
COPY requirements.txt .

# Instalacja pakietów Python
RUN pip install --no-cache-dir -r requirements.txt

# Kopowanie kodu
COPY . .

# Ustaw zmienne środowiska
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

# Komenda uruchomienia
CMD ["python", "src/main.py"]
```

- docker-compose.yml

```
version: '3.8'

services:
  ai-agent:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: my-ai-agent
    environment:
      - PYTHONUNBUFFERED=1
      - BIELIK_API_KEY=${BIELIK_API_KEY}
    volumes:
      - ./src:/app/src
      - ./data:/app/data
    networks:
      - agent-network
    restart: unless-stopped

networks:
  agent-network:
    driver: bridge
```

### 27 RUN in DOCKER

- `docker build -t my-ai-agent:latest .`
- `docker run --env-file .env -it my-ai-agent:latest`
  or docker-compose.yml
- `docker-compose up -d`
- `docker-compose logs -f ai-agent`

### NEXT STEPS:

1. Wdrożenie agenta:

- Utwórz src/agents/base_agent.py z logiką
- Dodaj testy w tests/
- Wersjonuj kod w Git

2. Zaawansowana konfiguracja:

- Setup CI/CD (GitHub Actions)
- Logging i monitoring
- Database (PostgreSQL, MongoDB)

3. Optymalizacja:

- Profiling wydajności
- Caching
- Async/await patterns

4. Deployment:

- Docker Registry (Docker Hub, GitHub Container Registry)
- Kubernetes (jeśli scaling)
- Cloud deployment (AWS, GCP, Azure)

### Troubleshooting

- Python not find:

```
which python3.13
python3.13 --version

```

- pip not running:

```
python3.13 -m pip install --upgrade pip
```

- Docker permission danied:

```
sudo usermod -aG docker $USER
newgrp docker
exit
su - $USER
```

- VSCode not see venv:

1. Otwórz Ctrl+Shift+P → Python: Select Interpreter
2. Wpisz pełną ścieżkę: /home/YOUR_USER/my-ai-agent/venv/bin/python
3. Lub usuń .vscode/settings.json i zacznij od nowa

- Docker port has been busy:

```
docker ps
docker kill CONTAINER_ID
```

- Bielik don't contect with API

```
# Sprawdź .env
cat .env

# Sprawdzenie połączenia
python -c "import bielik_composer; print('OK')"
```
