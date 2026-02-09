# Sentinel AI

**Check if content is AI-generated or a scam.**

Sentinel AI is an upload-only AI analysis system that helps non-technical users identify:
- AI-generated or manipulated content (deepfakes)
- Scam, phishing, and social engineering attempts

## Supported Content Types

| Type | Formats | Limits |
|------|---------|--------|
| Image | JPG, PNG | 50MB max |
| Video | MP4, MOV, WebM | 8 seconds max |
| Audio | MP3, WAV, M4A | 30 seconds max |
| Text | Plain text | 10,000 characters max |

## Quick Start

### Prerequisites
- [Docker](https://www.docker.com/get-started) installed
- [Docker Compose](https://docs.docker.com/compose/install/) installed

### 1. Clone and Configure

```bash
cd sentinel

# Copy environment template
cp .env.example .env

# Edit .env with your API keys (optional)
```

### 2. Start the Application

```bash
# Build and start all services
docker compose up --build

# Or run in background
docker compose up --build -d
```

### 3. Access the Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

## Architecture

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│    Frontend     │────▶│    Backend      │────▶│     Redis       │
│  (nginx:3000)   │     │ (FastAPI:8000)  │     │    (6379)       │
└─────────────────┘     └─────────────────┘     └─────────────────┘
                              │
                              ▼
                        ┌─────────────────┐
                        │  Celery Worker  │
                        │  (async tasks)  │
                        └─────────────────┘
```

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/analyze/text` | POST | Analyze text for AI/scam detection |
| `/analyze/image` | POST | Analyze image for deepfakes |
| `/analyze/audio` | POST | Analyze audio for voice spoofing |
| `/analyze/video` | POST | Analyze video for deepfakes |
| `/health` | GET | Health check |

### Example: Text Analysis

```bash
curl -X POST http://localhost:8000/analyze/text \
  -H "Content-Type: application/json" \
  -d '{"text": "You won $1000! Click here now!"}'
```

Response:
```json
{
  "risk_score": 75,
  "verdict": "Possibly AI",
  "explanations": [
    "This message is trying to trick you into doing something risky.",
    "The message is pushing you to act fast without thinking.",
    "This asks for money or financial information."
  ],
  "action": "Be careful! Don't click any links or share personal details.",
  "content_type": "text"
}
```

## Project Structure

```
sentinel/
├── docker-compose.yml      # Service orchestration
├── .env.example            # Environment template
│
├── backend/
│   ├── Dockerfile
│   ├── requirements.txt
│   └── app/
│       ├── main.py         # FastAPI app
│       ├── config.py       # Settings
│       ├── api/routes/     # API endpoints
│       ├── models/         # ML analyzers
│       ├── utils/          # Helpers
│       └── workers/        # Celery tasks
│
└── frontend/
    ├── Dockerfile
    ├── index.html
    ├── css/styles.css
    └── js/
        ├── main.js
        ├── api.js
        ├── ui.js
        └── validators.js
```

## Development

### Run Backend Only

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Run Frontend Only

Open `frontend/index.html` in a browser (note: API calls will fail without backend).

### View Logs

```bash
# All services
docker compose logs -f

# Specific service
docker compose logs -f backend
```

### Stop Services

```bash
docker compose down
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `GEMINI_API_KEY` | Gemini API key (optional) | - |
| `API_SECRET_KEY` | API secret key | - |
| `REDIS_URL` | Redis connection URL | `redis://redis:6379/0` |
| `MAX_UPLOAD_SIZE_MB` | Max upload size | `50` |
| `FILE_RETENTION_SECONDS` | Auto-delete after | `300` |

## Model Integration

The current implementation uses pattern-based mock inference. To integrate trained models:

1. Export your model to ONNX format
2. Place model files in `backend/models/`
3. Update the analyzer classes in `backend/app/models/`

### Model Targets

| Model | Framework | Target Size |
|-------|-----------|-------------|
| Text | DeBERTa-v3 / RoBERTa | ≤20MB (INT8) |
| Audio | wav2vec2 + CNN | ≤25MB |
| Image | EfficientNet-B0 | ≤15MB |
| Video | CNN + temporal pooling | Cloud-only |

## Notes

⚠️ **Disclaimer**: This tool provides estimates only and cannot guarantee 100% accuracy. Always verify important information through trusted sources.

## License

MIT
