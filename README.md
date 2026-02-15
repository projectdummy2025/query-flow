# Query Flow Chat

Chatbot sederhana berbasis OpenRouter API.
Backend dibuat dengan FastAPI (Python) dan frontend sederhana memakai HTML + JavaScript.

## Ringkas

- Streaming response via SSE-style endpoint.
- Riwayat chat disimpan di browser (client-side).
- Konfigurasi mudah lewat environment variable.

## Struktur

- backend/: API server + client OpenRouter.
- frontend/: halaman chat sederhana.
- docs/: dokumentasi dan tutorial.

## Mulai Cepat

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements.txt
export OPENROUTER_API_KEY=your_api_key_here
uvicorn backend.main:app --reload --port 8000
```

Buka `http://localhost:8000`.

## Dokumentasi

- Lihat [docs/docs.md](docs/docs.md)
- Tutorial singkat di [docs/tutorial.md](docs/tutorial.md)
