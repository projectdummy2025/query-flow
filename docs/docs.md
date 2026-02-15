# Query Flow Chat

Query Flow Chat adalah proyek chatbot sederhana yang memakai OpenRouter API.
Backend dibuat dengan FastAPI (Python) dan frontend sederhana memakai HTML + JavaScript.
Target utama proyek ini adalah demonstrasi alur chat streaming dari model LLM.

## Fitur

- Backend FastAPI dengan endpoint streaming.
- Frontend HTML/JS sederhana tanpa build step.
- Riwayat chat disimpan di browser (client-side).
- Konfigurasi mudah lewat environment variable.

## Struktur

- backend/: API server + client OpenRouter.
- frontend/: halaman chat sederhana.
- docs/: dokumentasi dan tutorial.

## Catatan

- API key OpenRouter harus disimpan di server (env var).
- Default model: meta-llama/llama-3-8b-instruct.
- Streaming menggunakan SSE-style di response `text/event-stream`.
