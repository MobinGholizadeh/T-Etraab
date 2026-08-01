# Project Workflow

> [!NOTE]
> This interactive walkthrough illustrates how data moves through the AI Task Management system—from the moment a user sends a message, through the AI and background queues, and finally back to the user.

````carousel
## 1. Initial Request
> [!IMPORTANT]
> The user interacts with the system via Telegram. The bot immediately forwards the request to the backend API.

```mermaid
flowchart LR
    User([User]) -->|Sends message| Bot{"Telegram Bot"}
    Bot -->|Forwards request| API["FastAPI Server"]
```

<!-- slide -->
## 2. Acknowledgment & Queuing
> [!TIP]
> The server quickly responds to the bot to prevent timeouts, and safely enqueues the heavy lifting into Redis.

```mermaid
flowchart LR
    API["FastAPI Server"] -.->|Acknowledges| Bot{"Telegram Bot"}
    Bot -.->|"Processing..."| User([User])
    
    API -->|Enqueues background task| Redis[("Redis Queue")]
```

<!-- slide -->
## 3. AI Extraction & Approval
> [!NOTE]
> Celery uses Groq LLM to extract task details, stores them in Redis temporarily, and asks the Manager for approval via Telegram buttons.

```mermaid
flowchart LR
    Redis[("Redis Queue")] -->|Delivers Task| Celery[["Celery Worker"]]
    Celery <-->|Analyzes intent| Groq{{"Groq LLM"}}
    Celery -->|Saves pending state| PendingRedis[("Redis Pending State")]
    Celery -->|Sends Approve/Cancel| Bot{"Telegram Bot"}
    Bot -->|Displays Buttons| User([User])
```

<!-- slide -->
## 4. Task Creation & Feedback
> [!TIP]
> If the manager approves, the bot retrieves the pending state, queues task creation in Plane, and notifies both the manager and assigned developer.

```mermaid
flowchart LR
    User([User]) -->|Clicks Approve| Bot{"Telegram Bot"}
    Bot -->|Retrieves pending state| PendingRedis[("Redis Pending State")]
    Bot -->|Queues creation| Celery[["Celery Worker"]]
    Celery <-->|Creates task| Plane[/"Plane API"/]
    Celery -->|Notifies dev & manager| Bot
```
````
