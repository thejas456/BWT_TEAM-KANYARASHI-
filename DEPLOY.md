# Deployment

## Streamlit Community Cloud (Recommended)
1. Push this repo to GitHub.
2. Go to https://share.streamlit.io/ and sign in.
3. Create new app:
   - Repository: your GitHub repo
   - Branch: main
   - File: app.py
4. Advanced settings:
   - Python version: 3.10
   - Dependencies: requirements.txt (auto)
5. Deploy.

## Render (Docker)
1. Ensure `Dockerfile` and `render.yaml` are committed and pushed.
2. In Render:
   - New Web Service → From repo
   - Select this repo
   - It will detect `render.yaml`
3. Deploy. The service exposes port 8501 by default.

## Docker (Local)
```bash
docker build -t credpulse-ai .
docker run -p 8501:8501 credpulse-ai
```
Open http://localhost:8501

## Notes
- Large local files are ignored via `.dockerignore` and `.gitignore`.
- For secrets, use `.streamlit/secrets.toml` locally and Render environment variables in the dashboard.
