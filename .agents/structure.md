# Project Structure

## AI Task Manager Structure (`./`)
```text
|   ├── src/                            # Main source code directory
|   |   ├── application/                # Application logic and use cases
|   |   |   ├── services/               # Core business services
|   |   |   └── use_cases/              # Specific task use cases
|   |   ├── config/                     # Configuration and settings
|   |   |   ├── logging.py              # Logging setup and config
|   |   |   └── settings.py             # Main Pydantic settings class
|   |   ├── core/                       # Core utilities, base classes, shared logic
|   |   ├── domain/                     # Domain entities and business rules
|   |   ├── infrastructure/             # External system integrations
|   |   |   ├── llm/                    # LLM integration (e.g., Groq)
|   |   |   ├── providers/              # Task tracking providers (e.g., Plane)
|   |   |   ├── queue/                  # Celery app and background tasks
|   |   |   ├── speech/                 # Audio processing (e.g., Whisper)
|   |   |   └── telegram/               # Telegram integration infrastructure
|   |   ├── presentation/               # Delivery and routing mechanisms
|   |   |   ├── api/                    # FastAPI routes and endpoints
|   |   |   └── bot/                    # Telegram bot handlers and UI
|   |   └── main.py                     # Entry point for the FastAPI backend
|   ├── .agents/                        # AI Assistant configurations
|   |   ├── AGENTS.md                   # AI Assistant rules
|   |   ├── product.md                  # Product goals and context
|   |   ├── structure.md                # Project structure documentation (this file)
|   |   ├── tech.md                     # Technology stack details
|   |   └── workflow.md                 # System flowcharts and execution flows
|   ├── .env.sample                     # Sample environment variables
|   ├── docker-compose.yml              # Docker Compose services definition
|   ├── Dockerfile                      # Blueprint for the application's container
|   └── requirements.txt                # Python dependencies
```
