# AI Task Management Platform

An AI-powered task management platform featuring a Telegram bot interface, Celery task queue, and integrations with task providers like Plane and AI models via Groq.

## 🚀 Quick Start (Docker) - Recommended

The easiest way to run the platform is using Docker Compose. It will automatically set up Redis, the FastAPI backend, the Telegram Bot, Celery workers, and monitoring tools (Prometheus & Grafana).

### Prerequisites
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) or Docker Engine with Docker Compose

### Step-by-Step Installation

1. **Clone the repository**
   ```bash
   git clone <YOUR_GITHUB_REPO_URL>
   cd ai-task-manager
   ```

2. **Set up environment variables**
   Copy the provided sample file to create your `.env` file:
   ```bash
   cp .env.sample .env
   ```
   *(On Windows Command Prompt, use: `copy .env.sample .env`)*

3. **Configure API Keys**
   Open `.env` in a text editor and fill in your keys:
   - `TELEGRAM_BOT_TOKEN`: Get this from [@BotFather](https://t.me/botfather) on Telegram.
   - `GROQ_API_KEY`: Get this from the [Groq Console](https://console.groq.com/keys).
   - `PLANE_API_KEY` (and Workspace Slug / Project ID): Get these from your [Plane.so](https://plane.so/) settings if you are using Plane as your active provider.

4. **Start the platform**
   Run the following command to build and start all services in the background:
   ```bash
   docker-compose up -d --build
   ```

5. **Verify it's running**
   - **FastAPI Backend**: http://localhost:8000
   - **Grafana Dashboard**: http://localhost:3000 (username: `admin` / password: `admin`)
   - **Telegram Bot**: Open Telegram and send a message to your bot.

To stop the services later, run:
```bash
docker-compose down
```

---

## 🛠️ Local Installation (Without Docker)

If you prefer to run the components directly on your machine without Docker containers, follow these steps.

### Prerequisites
- Python 3.10+
- [Redis server](https://redis.io/download) running on your local machine on port 6379

### Step-by-Step Installation

1. **Install and Start Redis**
   Make sure Redis is running locally (`redis-server`). On Windows, you can use WSL or Memurai.

2. **Set up a Python Virtual Environment**
   ```bash
   python -m venv venv
   
   # On Windows:
   venv\Scripts\activate
   
   # On Mac/Linux:
   source venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up Environment Variables**
   Copy `.env.sample` to `.env` and configure your API keys as described in the Docker setup.

5. **Run the Services**
   You'll need multiple terminal windows/tabs for this, with the virtual environment activated in each:

   **Tab 1: Start the API Server**
   ```bash
   python -m src.main
   ```

   **Tab 2: Start the Celery Worker**
   *(Note: Celery is not fully supported on native Windows. We recommend using WSL or Docker for Celery.)*
   ```bash
   celery -A src.infrastructure.queue.celery_app worker --loglevel=info
   ```

   **Tab 3: Start the Telegram Bot**
   ```bash
   python -m src.presentation.bot.main
   ```
