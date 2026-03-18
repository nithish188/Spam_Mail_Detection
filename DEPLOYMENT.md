# Deployment Guide

## Quick Start (Local)

```bash
pip install -r requirements.txt
streamlit run app.py
```

The app will open at `http://localhost:8501`

## Deploy to Streamlit Cloud (Free)

### Step 1: Prepare Your Project
Ensure your project is on GitHub with:
- `app.py` (main entry point)
- `requirements.txt` (all dependencies)
- `.streamlit/config.toml` (Streamlit config)
- `src/` directory with modules
- `data/` and `models/` directories

### Step 2: Create Streamlit Cloud Account
1. Go to https://share.streamlit.io
2. Sign in with GitHub

### Step 3: Deploy
1. Click "New app"
2. Select your GitHub repository
3. Select main branch
4. Set main file to `app.py`
5. Click "Deploy"

### Step 4: Access Your App
Your app will be live at: `https://your-username-app-name.streamlit.app`

## Environment Variables (Optional)

For Streamlit Cloud deployment, you can set secrets in:
Settings → Secrets → Add to `~/.streamlit/secrets.toml`

Example:
```toml
[database]
url = "https://example.com"
```

## Docker Deployment

Create `Dockerfile`:
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["streamlit", "run", "app.py"]
```

Build and run:
```bash
docker build -t spam-detector .
docker run -p 8501:8501 spam-detector
```

## Performance Optimization

For faster loading in Streamlit Cloud:
1. Use `@st.cache_data` for expensive operations (already in data loading)
2. Reduce dataset size for training
3. Pre-train models locally and commit them

## Troubleshooting

### Port Already in Use
```bash
streamlit run app.py --server.port 8502
```

### Memory Issues
Reduce sample data size in `data_preprocessing.py`:
```python
create_sample_data(data_path, n_samples=200)  # Instead of 500
```

### Model File Size
Keep model files under 100MB for cloud deployment.
