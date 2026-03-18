# 🚀 Quick Start Guide

## No Virtual Environment Needed!

This is a **Streamlit web application** that works directly without virtual environments.

### Windows Users

**Option 1: Double-click (Easiest)**
```
Double-click: run.bat
```

**Option 2: Command Line**
```cmd
pip install -r requirements.txt
streamlit run app.py
```

### Mac/Linux Users

**Option 1: Run script**
```bash
chmod +x run.sh
./run.sh
```

**Option 2: Manual command**
```bash
pip install -r requirements.txt
streamlit run app.py
```

---

## What Happens When You Run It

1. **Dependencies Install** - All required packages download automatically
2. **Streamlit Starts** - A local web server starts
3. **Browser Opens** - Your default browser opens to `http://localhost:8501`
4. **App Ready** - You can now use the spam detector!

---

## Using the App

### 📧 **Detector Tab** (Default)
- Paste any email text
- Click "Analyze"
- Get instant spam/ham classification with confidence score

### 🚀 **Train Model Tab**
- Click "Train Model" to create a ML model from sample data
- See performance metrics (Accuracy, Precision, etc.)
- Automatically saved for future use

### 📊 **Batch Testing Tab**
- Paste multiple emails separated by blank lines
- Analyze all at once
- Get summary statistics

### 📖 **About Tab**
- Learn how the system works
- See example emails
- View model details

---

## First Time Usage

1. Run the app using the command above
2. Go to **Train Model** tab
3. Click **Train Model** button
4. Wait for training to complete (~30 seconds)
5. Go to **Detector** tab
6. Paste an email and click **Analyze**

---

## System Requirements

- **Python 3.8+** (check with `python --version`)
- **Internet connection** (for first run to download packages)
- **Any modern browser** (Chrome, Firefox, Safari, Edge)

---

## Example Emails to Test

### ✓ Legitimate (Ham)
```
Can we schedule a meeting tomorrow at 3pm?
Please find the quarterly report attached.
Thanks for your help with the project!
```

### 🚨 Spam
```
CONGRATULATIONS YOU WON A PRIZE!!! CLICK HERE NOW!!!
Click here for FREE MONEY and CASH!!!
Your account has been compromised. Verify immediately!
```

---

## Deployment

Want to share your app online? See [DEPLOYMENT.md](DEPLOYMENT.md) for:
- Deploy to **Streamlit Cloud** (Free, easy)
- Deploy to **AWS, Azure, Heroku** (Paid options)
- Deploy with **Docker** (Advanced)

---

## Troubleshooting

### ❌ "Python not found"
- Install Python from https://www.python.org/
- Make sure to check "Add Python to PATH" during installation

### ❌ "Port 8501 already in use"
```cmd
streamlit run app.py --server.port 8502
```

### ❌ "Module not found"
```cmd
pip install scikit-learn pandas numpy streamlit
```

### ❌ App won't train
- Make sure you have at least 500MB free disk space
- Check that `data/` and `models/` folders can be created

---

## Files Overview

| File | Purpose |
|------|---------|
| `app.py` | Main Streamlit web app |
| `src/spam_detector.py` | Detection logic |
| `src/data_preprocessing.py` | Email cleaning/processing |
| `src/model.py` | ML model training |
| `requirements.txt` | All dependencies |
| `.streamlit/config.toml` | Streamlit settings |

---

## Keyboard Shortcuts

| Key | Action |
|-----|--------|
| `Ctrl+C` | Stop the app |
| `R` | Rerun app |
| `Cmd+Enter` | Run code component |

---

## Next Steps

1. ✓ Run the app
2. ✓ Train the model
3. ✓ Test with emails
4. ✓ (Optional) Deploy online

**Happy spam detecting! 📧**
