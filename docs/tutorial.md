# Tutorial Cepat

Berikut langkah paling singkat untuk menjalankan proyek ini secara lokal.

## 1) Siapkan environment

Buat virtual env dan install dependency:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements.txt
```

## 2) Set API key OpenRouter

Set variable env di terminal:

```bash
export OPENROUTER_API_KEY=your_api_key_here
```

Opsional: kamu bisa menyalin `.env.example` menjadi `.env` dan isi nilainya, lalu jalankan server di bawah.

## 3) Jalankan server

```bash
uvicorn backend.main:app --reload --port 8000
```

## 4) Buka frontend

Buka browser ke:

```
http://localhost:8000
```

## 5) Uji streaming

Ketik pesan di UI, lalu lihat balasan muncul bertahap.

## Troubleshooting

- Jika error 401/403, periksa `OPENROUTER_API_KEY`.
- Jika respons kosong, cek model di `OPENROUTER_MODEL`.
- Jika ingin host frontend terpisah, set `APP_ORIGIN`.
