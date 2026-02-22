Deployment guide

1) API (FastAPI) -> Render or Docker
- Build a Docker image using `api/Dockerfile` and push to a registry.
- On Render: create a Web Service, connect to GitHub repo, set Docker option and configure port 8000.
- Add environment variable `GOOGLE_API_KEY` in Render settings.

2) Frontend (React/Vite) -> Vercel
- In Vercel, import the `frontend` project from this repo (select folder `frontend`).
- Build command: `npm run build`
- Output dir: `dist`
- Set env var `VITE_API_BASE` or update the fetch URL in `App.jsx` to your API endpoint.

3) Streamlit App -> Streamlit Community Cloud (optional)
- Your Streamlit app (`ui/app.py`) can remain on Streamlit Cloud. Add `GOOGLE_API_KEY` in Secrets.

Notes
- For local development, run the API:

```bash
python -m pip install -r requirements.txt
uvicorn api.app:app --reload --port 8000
```

- Run frontend locally (from `frontend` folder):

```bash
npm install
npm run dev
```

- The React frontend captures with `facingMode: environment` when supported; browsers vary.
