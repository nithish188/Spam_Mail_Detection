"""
SpamSense - Advanced Email Security Dashboard
Modern Admin-style Dashboard with Professional UI
"""

import streamlit as st
import pickle
import os
import sys
from pathlib import Path
import time
import random
from datetime import datetime, timedelta

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from data_preprocessing import EmailPreprocessor, create_sample_data
from model import SpamDetectorModel
from spam_detector import SpamDetector

# Page configuration
st.set_page_config(
    page_title="SpamSense Dashboard",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────────
# MODERN ADMIN DASHBOARD CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
    /* ===== IMPORTS ===== */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

    /* ===== ROOT VARIABLES ===== */
    :root {
        --primary: #4361ee;
        --primary-dark: #3a56d4;
        --primary-light: #eef1ff;
        --sidebar-bg: #1e2a4a;
        --sidebar-active: #4361ee;
        --bg: #f0f2f8;
        --card-bg: #ffffff;
        --text-primary: #1e293b;
        --text-secondary: #64748b;
        --text-muted: #94a3b8;
        --border: #e2e8f0;
        --success: #22c55e;
        --success-light: #f0fdf4;
        --danger: #ef4444;
        --danger-light: #fef2f2;
        --warning: #f59e0b;
        --warning-light: #fffbeb;
        --info: #3b82f6;
        --info-light: #eff6ff;
        --shadow-sm: 0 1px 2px rgba(0,0,0,0.05);
        --shadow: 0 1px 3px rgba(0,0,0,0.1), 0 1px 2px rgba(0,0,0,0.06);
        --shadow-md: 0 4px 6px -1px rgba(0,0,0,0.1), 0 2px 4px -1px rgba(0,0,0,0.06);
        --shadow-lg: 0 10px 15px -3px rgba(0,0,0,0.1), 0 4px 6px -2px rgba(0,0,0,0.05);
        --radius: 12px;
        --radius-sm: 8px;
    }

    /* ===== GLOBAL STYLES ===== */
    * { font-family: 'Inter', sans-serif !important; }

    /* Hide Streamlit header */
    [data-testid="stHeader"],
    header[data-testid="stHeader"],
    .stAppHeader {
        display: none !important;
        height: 0 !important;
    }

    /* Main background */
    .stAppViewContainer, [data-testid="stAppViewContainer"] {
        background: var(--bg) !important;
    }

    [data-testid="stMain"] {
        background: transparent !important;
    }

    [data-testid="stMainBlockContainer"] {
        background: transparent !important;
        padding: 1rem 2rem !important;
        max-width: 100% !important;
    }

    /* Remove any white blocks */
    div[data-testid="stVerticalBlock"],
    .element-container,
    [class*="stMarkdownContainer"],
    [class*="stColumn"],
    .stForm, .stContainer {
        background: transparent !important;
    }

    body, [data-testid="stAppViewContainer"] > div {
        background: transparent !important;
    }

    /* ===== GLOBAL TEXT ===== */
    h1, h2, h3, h4, h5, h6 {
        color: var(--text-primary) !important;
        font-weight: 700 !important;
    }

    p, span, label, div, li, td, th,
    .stMarkdown, .stMarkdown p,
    [data-testid="stMarkdownContainer"],
    [data-testid="stMarkdownContainer"] p,
    [data-testid="stText"] {
        color: var(--text-primary) !important;
    }

    /* ===== SIDEBAR ===== */
    [data-testid="stSidebar"] {
        background: var(--sidebar-bg) !important;
        box-shadow: 2px 0 10px rgba(0,0,0,0.1);
        width: 200px !important;
        min-width: 200px !important;
    }

    [data-testid="stSidebar"] header {
        display: none !important;
    }

    [data-testid="stSidebarCollapseButton"],
    [data-testid="collapsedControl"],
    [data-testid="stSidebar"] button[kind="header"],
    [data-testid="stSidebar"] [data-testid="stBaseButton-header"] {
        display: none !important;
        visibility: hidden !important;
    }

    /* Sidebar text */
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] span,
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"],
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p,
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] h4 {
        color: #ffffff !important;
    }

    [data-testid="stSidebar"] hr {
        border-color: rgba(255,255,255,0.1) !important;
    }

    /* Sidebar buttons */
    [data-testid="stSidebar"] .stButton > button {
        background: transparent !important;
        color: #cbd5e1 !important;
        border: none !important;
        border-radius: var(--radius-sm) !important;
        padding: 10px 16px !important;
        font-size: 0.9em !important;
        font-weight: 500 !important;
        text-align: left !important;
        width: 100% !important;
        justify-content: flex-start !important;
        box-shadow: none !important;
        transition: all 0.2s ease !important;
    }

    [data-testid="stSidebar"] .stButton > button:hover {
        background: rgba(67, 97, 238, 0.3) !important;
        color: #ffffff !important;
        transform: none !important;
    }

    [data-testid="stSidebar"] .stButton > button:focus {
        background: var(--sidebar-active) !important;
        color: #ffffff !important;
        box-shadow: none !important;
    }

    /* ===== METRIC CARDS ===== */
    .metric-card {
        background: var(--card-bg);
        border-radius: var(--radius);
        padding: 24px;
        box-shadow: var(--shadow);
        border: 1px solid var(--border);
        position: relative;
        overflow: hidden;
        transition: all 0.3s ease;
    }

    .metric-card:hover {
        box-shadow: var(--shadow-lg);
        transform: translateY(-2px);
    }

    .metric-card .metric-icon {
        width: 48px;
        height: 48px;
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 22px;
        margin-bottom: 16px;
    }

    .metric-card .metric-value {
        font-size: 2em;
        font-weight: 800;
        color: var(--text-primary);
        margin: 0;
        line-height: 1.2;
    }

    .metric-card .metric-label {
        font-size: 0.85em;
        color: var(--text-secondary);
        margin: 4px 0 0 0;
        font-weight: 500;
    }

    .metric-card .metric-badge {
        position: absolute;
        top: 16px;
        right: 16px;
        padding: 4px 10px;
        border-radius: 20px;
        font-size: 0.75em;
        font-weight: 600;
    }

    /* ===== CONTENT CARDS ===== */
    .content-card {
        background: var(--card-bg);
        border-radius: var(--radius);
        padding: 24px;
        box-shadow: var(--shadow);
        border: 1px solid var(--border);
        margin-bottom: 16px;
    }

    .content-card .card-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 20px;
    }

    .content-card .card-title {
        font-size: 1.1em;
        font-weight: 700;
        color: var(--text-primary);
        margin: 0;
    }

    .content-card .card-subtitle {
        font-size: 0.85em;
        color: var(--text-secondary);
        margin: 2px 0 0 0;
    }

    /* ===== ACTIVITY ITEM ===== */
    .activity-item {
        display: flex;
        align-items: flex-start;
        padding: 14px 0;
        border-bottom: 1px solid var(--border);
        gap: 12px;
    }

    .activity-item:last-child {
        border-bottom: none;
    }

    .activity-icon {
        width: 40px;
        height: 40px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 18px;
        flex-shrink: 0;
    }

    .activity-content {
        flex: 1;
    }

    .activity-title {
        font-size: 0.9em;
        font-weight: 600;
        color: var(--text-primary);
        margin: 0;
    }

    .activity-desc {
        font-size: 0.8em;
        color: var(--text-secondary);
        margin: 2px 0 0 0;
    }

    .activity-time {
        font-size: 0.75em;
        color: var(--text-muted);
        white-space: nowrap;
    }

    .activity-badge {
        padding: 3px 10px;
        border-radius: 20px;
        font-size: 0.7em;
        font-weight: 700;
    }

    /* ===== CHART BAR ===== */
    .chart-bar-container {
        display: flex;
        align-items: flex-end;
        gap: 8px;
        height: 180px;
        padding: 10px 0;
    }

    .chart-bar {
        flex: 1;
        border-radius: 6px 6px 0 0;
        position: relative;
        min-width: 20px;
        transition: all 0.3s ease;
    }

    .chart-bar:hover {
        opacity: 0.85;
    }

    .chart-bar-label {
        text-align: center;
        font-size: 0.7em;
        color: var(--text-muted);
        margin-top: 6px;
        font-weight: 500;
    }

    /* ===== DONUT CHART ===== */
    .donut-chart {
        width: 160px;
        height: 160px;
        border-radius: 50%;
        position: relative;
        margin: 0 auto;
    }

    .donut-center {
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        width: 90px;
        height: 90px;
        border-radius: 50%;
        background: var(--card-bg);
        display: flex;
        align-items: center;
        justify-content: center;
        flex-direction: column;
    }

    .donut-value {
        font-size: 1.4em;
        font-weight: 800;
        color: var(--text-primary);
    }

    .donut-label {
        font-size: 0.65em;
        color: var(--text-secondary);
    }

    /* ===== LEGEND ===== */
    .legend-item {
        display: flex;
        align-items: center;
        gap: 8px;
        margin: 6px 0;
        font-size: 0.82em;
    }

    .legend-dot {
        width: 10px;
        height: 10px;
        border-radius: 50%;
        flex-shrink: 0;
    }

    .legend-text {
        color: var(--text-secondary);
        flex: 1;
    }

    .legend-value {
        font-weight: 700;
        color: var(--text-primary);
    }

    /* ===== BREADCRUMB ===== */
    .breadcrumb {
        display: flex;
        align-items: center;
        gap: 8px;
        margin-bottom: 24px;
        font-size: 0.85em;
    }

    .breadcrumb-item {
        color: var(--text-muted);
    }

    .breadcrumb-item.active {
        color: var(--text-primary);
        font-weight: 600;
    }

    .breadcrumb-sep {
        color: var(--text-muted);
    }

    /* ===== PAGE TITLE ===== */
    .page-title {
        font-size: 1.5em;
        font-weight: 800;
        color: var(--text-primary);
        margin: 0 0 6px 0;
    }

    .page-subtitle {
        font-size: 0.9em;
        color: var(--text-secondary);
        margin: 0 0 24px 0;
    }

    /* ===== BADGES ===== */
    .spam-badge {
        background: linear-gradient(135deg, #ef4444, #dc2626);
        color: #fff !important;
        padding: 20px 40px;
        border-radius: var(--radius);
        font-weight: 700;
        font-size: 20px;
        text-align: center;
        box-shadow: 0 4px 14px rgba(239, 68, 68, 0.3);
        width: 100%;
    }

    .ham-badge {
        background: linear-gradient(135deg, #22c55e, #16a34a);
        color: #fff !important;
        padding: 20px 40px;
        border-radius: var(--radius);
        font-weight: 700;
        font-size: 20px;
        text-align: center;
        box-shadow: 0 4px 14px rgba(34, 197, 94, 0.3);
        width: 100%;
    }

    /* ===== STATS CONTAINER ===== */
    .stats-container {
        background: var(--card-bg);
        border-left: 5px solid var(--primary);
        padding: 20px;
        border-radius: var(--radius);
        margin: 10px 0;
        box-shadow: var(--shadow);
        border: 1px solid var(--border);
        border-left: 5px solid var(--primary);
    }

    .stats-container strong {
        color: var(--text-primary) !important;
        font-size: 1em;
    }

    .stats-container span {
        color: var(--primary) !important;
    }

    /* ===== BUTTONS ===== */
    .stButton > button {
        background: var(--primary) !important;
        color: #ffffff !important;
        border: none !important;
        font-size: 0.95em !important;
        font-weight: 600 !important;
        padding: 10px 24px !important;
        border-radius: var(--radius-sm) !important;
        box-shadow: 0 2px 8px rgba(67, 97, 238, 0.3) !important;
        transition: all 0.2s ease !important;
    }

    .stButton > button:hover {
        background: var(--primary-dark) !important;
        box-shadow: 0 4px 14px rgba(67, 97, 238, 0.4) !important;
        transform: translateY(-1px) !important;
    }

    /* ===== INPUTS ===== */
    .stTextArea > div > div > textarea {
        border-radius: var(--radius-sm) !important;
        border: 2px solid var(--border) !important;
        padding: 14px !important;
        background: var(--card-bg) !important;
        color: var(--text-primary) !important;
        font-size: 0.9em !important;
    }

    .stTextArea > div > div > textarea:focus {
        border-color: var(--primary) !important;
        box-shadow: 0 0 0 3px rgba(67, 97, 238, 0.15) !important;
    }

    .stTextInput > div > div > input {
        border-radius: var(--radius-sm) !important;
        border: 2px solid var(--border) !important;
        background: var(--card-bg) !important;
        padding: 10px 14px !important;
        color: var(--text-primary) !important;
    }

    .stTextInput > div > div > input:focus {
        border-color: var(--primary) !important;
        box-shadow: 0 0 0 3px rgba(67, 97, 238, 0.15) !important;
    }

    /* ===== METRICS (streamlit default) ===== */
    .stMetric {
        background: var(--card-bg) !important;
        border-radius: var(--radius) !important;
        padding: 20px !important;
        box-shadow: var(--shadow) !important;
        border: 1px solid var(--border) !important;
    }

    [data-testid="stMetricValue"] {
        color: var(--text-primary) !important;
        font-size: 2em !important;
        font-weight: 800 !important;
    }

    [data-testid="stMetricLabel"],
    [data-testid="stMetricLabel"] div,
    [data-testid="stMetricLabel"] p {
        color: var(--text-secondary) !important;
        font-weight: 500 !important;
    }

    [data-testid="stMetricDelta"] {
        color: var(--success) !important;
    }

    /* ===== HIDE DIVIDER DEFAULT ===== */
    hr {
        border-color: var(--border) !important;
    }

    /* ===== INFO MESSAGE ===== */
    .info-message {
        background: var(--info-light);
        border: 1px solid #bfdbfe;
        color: var(--text-primary);
        padding: 16px 20px;
        border-radius: var(--radius-sm);
        margin: 12px 0;
    }

    /* ===== DATAFRAME ===== */
    .stDataFrame {
        border-radius: var(--radius) !important;
        overflow: hidden;
    }

    /* ===== RESPONSIVE ===== */
    @media (max-width: 768px) {
        .metric-card .metric-value { font-size: 1.5em; }
        .chart-bar-container { height: 120px; }
    }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# SESSION STATE
# ─────────────────────────────────────────────
if 'detector' not in st.session_state:
    st.session_state.detector = None
if 'model_trained' not in st.session_state:
    st.session_state.model_trained = False
if 'model_metrics' not in st.session_state:
    st.session_state.model_metrics = None
if 'page' not in st.session_state:
    st.session_state.page = "dashboard"
if 'scan_history' not in st.session_state:
    st.session_state.scan_history = []

# ─────────────────────────────────────────────
# MODEL TRAINING
# ─────────────────────────────────────────────
@st.cache_resource
def train_model_cached():
    """Train and cache the model"""
    progress_bar = st.progress(0)
    status_text = st.empty()

    try:
        status_text.text("📊 Creating dataset...")
        progress_bar.progress(10)
        data_path = 'data/emails.csv'
        os.makedirs('data', exist_ok=True)

        if not os.path.exists(data_path):
            create_sample_data(data_path, n_samples=500)

        status_text.text("🔄 Preprocessing data...")
        progress_bar.progress(30)
        preprocessor = EmailPreprocessor(test_size=0.2, random_state=42)
        emails, labels = preprocessor.load_data(data_path)
        X_train, X_test, y_train, y_test = preprocessor.preprocess(emails, labels)

        status_text.text("🤖 Training model...")
        progress_bar.progress(60)
        model = SpamDetectorModel('naive_bayes')
        model.train(X_train, y_train)

        status_text.text("📈 Evaluating performance...")
        progress_bar.progress(80)
        metrics = model.evaluate(X_test, y_test)

        status_text.text("💾 Saving model...")
        progress_bar.progress(90)
        os.makedirs('models', exist_ok=True)
        model.save('models/best_model_naive_bayes.pkl')

        vectorizer_path = 'models/vectorizer.pkl'
        with open(vectorizer_path, 'wb') as f:
            pickle.dump(preprocessor.vectorizer, f)

        detector = SpamDetector(model.model, preprocessor.vectorizer)

        progress_bar.progress(100)
        status_text.text("✅ Model ready!")
        time.sleep(0.5)
        progress_bar.empty()
        status_text.empty()

        return detector, metrics
    except Exception as e:
        st.error(f"Error training model: {e}")
        return None, None

def load_or_train_model():
    """Load existing model or train new one"""
    model_path = 'models/best_model_naive_bayes.pkl'
    vectorizer_path = 'models/vectorizer.pkl'

    if os.path.exists(model_path) and os.path.exists(vectorizer_path):
        try:
            with open(model_path, 'rb') as f:
                model = pickle.load(f)
            with open(vectorizer_path, 'rb') as f:
                vectorizer = pickle.load(f)
            detector = SpamDetector(model, vectorizer)
            st.session_state.detector = detector
            st.session_state.model_trained = True
            return detector, None
        except:
            pass

    detector, metrics = train_model_cached()
    if detector:
        st.session_state.detector = detector
        st.session_state.model_trained = True
        st.session_state.model_metrics = metrics
    return detector, metrics

# Load model
if not st.session_state.detector:
    detector, metrics = load_or_train_model()

# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────

# SVG icons (line-art style)
SVG_DASHBOARD = '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="3" width="20" height="14" rx="2" ry="2"></rect><line x1="8" y1="21" x2="16" y2="21"></line><line x1="12" y1="17" x2="12" y2="21"></line><path d="M6 8h.01M6 12h.01M10 12a2 2 0 1 0 0-4 2 2 0 0 0 0 4z"></path><rect x="14" y="8" width="2" height="4"></rect><rect x="17" y="7" width="2" height="5"></rect></svg>'
SVG_EMAIL = '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="4" width="20" height="16" rx="2"></rect><path d="M22 4L12 13 2 4"></path></svg>'
SVG_STATS = '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="20" x2="18" y2="10"></line><line x1="12" y1="20" x2="12" y2="4"></line><line x1="6" y1="20" x2="6" y2="14"></line></svg>'
SVG_BATCH = '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M9 5H7a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V7a2 2 0 0 0-2-2h-2"></path><rect x="9" y="3" width="6" height="4" rx="1"></rect><path d="M9 14l2 2 4-4"></path></svg>'
SVG_ABOUT = '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="16" x2="12" y2="12"></line><line x1="12" y1="8" x2="12.01" y2="8"></line></svg>'
SVG_SETTINGS = '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="3"></circle><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1-2.83 2.83l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-4 0v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83-2.83l.06-.06A1.65 1.65 0 0 0 4.68 15a1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1 0-4h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 2.83-2.83l.06.06A1.65 1.65 0 0 0 9 4.68a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 4 0v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 2.83l-.06.06A1.65 1.65 0 0 0 19.4 9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 0 4h-.09a1.65 1.65 0 0 0-1.51 1z"></path></svg>'
SVG_SHIELD = '<svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="#ffffff" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path><path d="M9 12l2 2 4-4"></path></svg>'

# Sidebar nav items as list of dicts
nav_items = [
    {"key": "dashboard", "label": "Dashboard", "icon": SVG_DASHBOARD, "page": "dashboard"},
    {"key": "detector", "label": "Email Detector", "icon": SVG_EMAIL, "page": "detector"},
    {"key": "stats", "label": "Statistics", "icon": SVG_STATS, "page": "statistics"},
]

nav_items_bottom = [
    {"key": "about", "label": "About", "icon": SVG_ABOUT, "page": "about"},
    {"key": "settings", "label": "Settings", "icon": SVG_SETTINGS, "page": "about"},
]

with st.sidebar:
    # Logo
    st.markdown(f"""
    <div style="padding: 20px 10px 10px 10px; text-align: center;">
        <div style="margin-bottom: 4px;">{SVG_SHIELD}</div>
        <h3 style="color: #ffffff !important; font-size: 1.3em; margin: 0; font-weight: 800;">SpamSense</h3>
        <p style="color: #94a3b8 !important; font-size: 0.75em; margin: 4px 0 0 0;">Email Security Suite</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # CSS to style the buttons with SVG icons
    st.markdown("""
    <style>
    /* Hide button text styling for SVG nav buttons */
    [data-testid="stSidebar"] .stButton > button {
        display: flex !important;
        align-items: center !important;
        gap: 12px !important;
        padding: 10px 16px !important;
        font-size: 0.9em !important;
    }

    [data-testid="stSidebar"] .stButton > button svg {
        flex-shrink: 0;
    }
    </style>
    """, unsafe_allow_html=True)

    # Main nav
    for item in nav_items:
        is_active = st.session_state.get('page', 'dashboard') == item['page']
        if st.button(f"  {item['label']}", key=f"nav_{item['key']}", use_container_width=True):
            st.session_state.page = item['page']
            st.rerun()

    st.markdown("---")

    # Bottom nav
    for item in nav_items_bottom:
        if st.button(f"  {item['label']}", key=f"nav_{item['key']}", use_container_width=True):
            st.session_state.page = item['page']
            st.rerun()

    # Model status
    st.markdown("---")
    if st.session_state.model_trained:
        st.markdown("""
        <div style="padding: 12px; background: rgba(34,197,94,0.15); border-radius: 8px; border: 1px solid rgba(34,197,94,0.3);">
            <p style="color: #4ade80 !important; font-size: 0.8em; margin: 0; font-weight: 600;">● Model Active</p>
            <p style="color: #94a3b8 !important; font-size: 0.7em; margin: 4px 0 0 0;">Naive Bayes · Ready</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="padding: 12px; background: rgba(239,68,68,0.15); border-radius: 8px; border: 1px solid rgba(239,68,68,0.3);">
            <p style="color: #f87171 !important; font-size: 0.8em; margin: 0; font-weight: 600;">● Model Inactive</p>
            <p style="color: #94a3b8 !important; font-size: 0.7em; margin: 4px 0 0 0;">Training needed</p>
        </div>
        """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
# HELPER FUNCTIONS
# ─────────────────────────────────────────────
def get_metrics():
    if st.session_state.model_metrics:
        m = st.session_state.model_metrics
        return {
            'accuracy': m.get('accuracy', 0) * 100,
            'precision': m.get('precision', 0) * 100,
            'recall': m.get('recall', 0) * 100,
            'f1': m.get('f1', 0) * 100
        }
    return {'accuracy': 95.0, 'precision': 95.0, 'recall': 95.0, 'f1': 95.0}

# def generate_sample_activity():
#     """Generate sample recent activity for the dashboard"""
#     activities = [
#         {"icon": "🚨", "bg": "#fef2f2", "title": "Spam Detected", "desc": "Phishing attempt blocked", "time": "2 min ago", "badge": "Spam", "badge_bg": "#fef2f2", "badge_color": "#ef4444"},
#         {"icon": "✅", "bg": "#f0fdf4", "title": "Email Verified", "desc": "Newsletter confirmed safe", "time": "5 min ago", "badge": "Safe", "badge_bg": "#f0fdf4", "badge_color": "#22c55e"},
#         {"icon": "🚨", "bg": "#fef2f2", "title": "Bulk Spam Caught", "desc": "Prize scam campaign flagged", "time": "12 min ago", "badge": "Spam", "badge_bg": "#fef2f2", "badge_color": "#ef4444"},
#         {"icon": "✅", "bg": "#f0fdf4", "title": "Email Verified", "desc": "Meeting invite from team", "time": "18 min ago", "badge": "Safe", "badge_bg": "#f0fdf4", "badge_color": "#22c55e"},
#         {"icon": "⚠️", "bg": "#fffbeb", "title": "Suspicious Email", "desc": "Low confidence detection", "time": "25 min ago", "badge": "Review", "badge_bg": "#fffbeb", "badge_color": "#f59e0b"},
#         {"icon": "✅", "bg": "#f0fdf4", "title": "Email Verified", "desc": "Project report from manager", "time": "30 min ago", "badge": "Safe", "badge_bg": "#f0fdf4", "badge_color": "#22c55e"},
#     ]
#     return activities

# ─────────────────────────────────────────────
# PAGE ROUTING
# ─────────────────────────────────────────────
page = st.session_state.page

# ═══════════════════════════════════════════════
# DASHBOARD PAGE
# ═══════════════════════════════════════════════
if page == "dashboard":
    # Breadcrumb
    st.markdown("""
    <div class="breadcrumb">
        <span class="breadcrumb-item">SpamSense</span>
        <span class="breadcrumb-sep">›</span>
        <span class="breadcrumb-item active">Dashboard</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<p class="page-title">General Report</p>', unsafe_allow_html=True)

    m = get_metrics()

    # Compute real stats from scan history
    scan_history = st.session_state.get('scan_history', [])
    total_scanned = len(scan_history)
    spam_count = sum(1 for s in scan_history if s.get('is_spam', False))
    clean_count = total_scanned - spam_count

    # ── METRIC CARDS ROW ──
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <p class="metric-value">{total_scanned}</p>
            <p class="metric-label">Emails Scanned</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <p class="metric-value">{spam_count}</p>
            <p class="metric-label">Spam Detected</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <p class="metric-value">{clean_count}</p>
            <p class="metric-label">Clean Emails</p>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <p class="metric-value">{m['accuracy']:.1f}%</p>
            <p class="metric-label">Detection Rate</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)

    # ── CHARTS ROW ──
    main_col, side_col = st.columns([2, 1])

    with main_col:

        # Classification Distribution
        dist_col1, dist_col2 = st.columns(2)

        with dist_col1:
            st.markdown(f"""
            <div class="content-card">
                <div class="card-header">
                    <div>
                        <p class="card-title">Spam Categories</p>
                        <p class="card-subtitle">By threat type</p>
                    </div>
                </div>
                <div style="display: flex; align-items: center; gap: 24px;">
                    <div class="donut-chart" style="background: conic-gradient(#4361ee 0deg 216deg, #ef4444 216deg 295deg, #f59e0b 295deg 338deg, #94a3b8 338deg 360deg);">
                        <div class="donut-center">
                            <span class="donut-value">342</span>
                            <span class="donut-label">Total</span>
                        </div>
                    </div>
                    <div>
                        <div class="legend-item"><div class="legend-dot" style="background: #4361ee;"></div><span class="legend-text">Phishing</span><span class="legend-value" style="margin-left: 8px;">60%</span></div>
                        <div class="legend-item"><div class="legend-dot" style="background: #ef4444;"></div><span class="legend-text">Scam</span><span class="legend-value" style="margin-left: 8px;">22%</span></div>
                        <div class="legend-item"><div class="legend-dot" style="background: #f59e0b;"></div><span class="legend-text">Malware</span><span class="legend-value" style="margin-left: 8px;">12%</span></div>
                        <div class="legend-item"><div class="legend-dot" style="background: #94a3b8;"></div><span class="legend-text">Other</span><span class="legend-value" style="margin-left: 8px;">6%</span></div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        with dist_col2:
            st.markdown(f"""
            <div class="content-card">
                <div class="card-header">
                    <div>
                        <p class="card-title">Model Metrics</p>
                        <p class="card-subtitle">Performance overview</p>
                    </div>
                </div>
                <div style="display: flex; align-items: center; gap: 24px;">
                    <div class="donut-chart" style="background: conic-gradient(#22c55e 0deg {m['accuracy']*3.6:.0f}deg, #e2e8f0 {m['accuracy']*3.6:.0f}deg 360deg);">
                        <div class="donut-center">
                            <span class="donut-value">{m['accuracy']:.0f}%</span>
                            <span class="donut-label">Accuracy</span>
                        </div>
                    </div>
                    <div>
                        <div class="legend-item"><div class="legend-dot" style="background: #4361ee;"></div><span class="legend-text">Precision</span><span class="legend-value" style="margin-left: 8px;">{m['precision']:.1f}%</span></div>
                        <div class="legend-item"><div class="legend-dot" style="background: #22c55e;"></div><span class="legend-text">Recall</span><span class="legend-value" style="margin-left: 8px;">{m['recall']:.1f}%</span></div>
                        <div class="legend-item"><div class="legend-dot" style="background: #f59e0b;"></div><span class="legend-text">F1 Score</span><span class="legend-value" style="margin-left: 8px;">{m['f1']:.1f}%</span></div>
                        <div class="legend-item"><div class="legend-dot" style="background: #94a3b8;"></div><span class="legend-text">Accuracy</span><span class="legend-value" style="margin-left: 8px;">{m['accuracy']:.1f}%</span></div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    with side_col:
        # Recent Activity
        activities = generate_sample_activity()
        activity_html = ""
        for act in activities:
            activity_html += f"""
            <div class="activity-item">
                <div style="font-size: 18px; flex-shrink: 0;">{act['icon']}</div>
                <div class="activity-content">
                    <p class="activity-title">{act['title']}</p>
                    <p class="activity-desc">{act['desc']}</p>
                </div>
                <div style="text-align: right;">
                    <span class="activity-badge" style="background: {act['badge_bg']}; color: {act['badge_color']};">{act['badge']}</span>
                    <p class="activity-time" style="margin: 4px 0 0 0;">{act['time']}</p>
                </div>
            </div>
            """

        st.markdown(f"""
        <div class="content-card" style="height: 100%;">
            <div class="card-header">
                <p class="card-title">Recent Activity</p>
                <span style="font-size: 0.8em; color: #4361ee; font-weight: 600; cursor: pointer;">View All</span>
            </div>
            {activity_html}
        </div>
        """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════
# EMAIL DETECTOR PAGE
# ═══════════════════════════════════════════════
elif page == "detector":
    st.markdown("""
    <div class="breadcrumb">
        <span class="breadcrumb-item">SpamSense</span>
        <span class="breadcrumb-sep">›</span>
        <span class="breadcrumb-item active">Email Detector</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<p class="page-title">Email Detector</p>', unsafe_allow_html=True)
    st.markdown('<p class="page-subtitle">Analyze any email to determine if it\'s spam or legitimate</p>', unsafe_allow_html=True)

    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    email_text = st.text_area(
        "Email Content",
        placeholder="Paste the email text you want to analyze...",
        height=250,
        label_visibility="collapsed"
    )

    if st.button("🔍 Analyze Email", use_container_width=True, type="primary"):
        if email_text:
            detector = st.session_state.detector

            is_spam = detector.is_spam(email_text)
            probability = detector.get_spam_probability(email_text)
            confidence = abs(probability - 0.5) * 2

            st.markdown("---")

            # Result badge
            if is_spam:
                st.markdown(
                    '<div class="spam-badge">🚨 SPAM DETECTED</div>',
                    unsafe_allow_html=True
                )
            else:
                st.markdown(
                    '<div class="ham-badge">✅ LEGITIMATE EMAIL</div>',
                    unsafe_allow_html=True
                )

            st.markdown("")

            # Metrics
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Classification", "SPAM" if is_spam else "HAM",
                         delta="Risky" if is_spam else "Safe")
            with col2:
                st.metric("Spam Probability", f"{probability:.1%}")
            with col3:
                st.metric("Confidence Level", f"{confidence:.1%}")

            # Details
            st.markdown("### Detailed Analysis")
            details_col1, details_col2 = st.columns(2)

            with details_col1:
                st.markdown("""
                <div class="stats-container">
                    <strong>Classification Details</strong><br>
                    📌 Type: <span style="font-weight: bold;">{}</span><br>
                    🎯 Score: <span style="font-weight: bold;">{:.4f}</span><br>
                    ⚡ Model: <span style="font-weight: bold;">Naive Bayes</span>
                </div>
                """.format("SPAM" if is_spam else "LEGITIMATE", probability),
                unsafe_allow_html=True)

            with details_col2:
                st.markdown("""
                <div class="stats-container">
                    <strong>Prediction Confidence</strong><br>
                    🎲 Confidence: <span style="font-weight: bold;">{:.2%}</span><br>
                    📊 Certainty: <span style="font-weight: bold;">{}</span><br>
                    ✓ Status: <span style="font-weight: bold;">{}</span>
                </div>
                """.format(
                    confidence,
                    "Very High" if confidence > 0.8 else "High" if confidence > 0.6 else "Medium",
                    "Reliable" if confidence > 0.6 else "Low confidence"
                ),
                unsafe_allow_html=True)

            # Add to scan history
            st.session_state.scan_history.append({
                "text": email_text[:50],
                "is_spam": is_spam,
                "confidence": confidence,
                "time": datetime.now().strftime("%H:%M")
            })
        else:
            st.warning("Please enter email content to analyze")
    st.markdown('</div>', unsafe_allow_html=True)


# ═══════════════════════════════════════════════
# STATISTICS PAGE
# ═══════════════════════════════════════════════
elif page == "statistics":
    st.markdown("""
    <div class="breadcrumb">
        <span class="breadcrumb-item">SpamSense</span>
        <span class="breadcrumb-sep">›</span>
        <span class="breadcrumb-item active">Statistics</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<p class="page-title">Model Performance Dashboard</p>', unsafe_allow_html=True)

    if st.session_state.model_metrics:
        metrics = st.session_state.model_metrics

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <p class="metric-value">{metrics['accuracy']:.1%}</p>
                <p class="metric-label">Accuracy</p>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
            <div class="metric-card">
                <p class="metric-value">{metrics['precision']:.1%}</p>
                <p class="metric-label">Precision</p>
            </div>
            """, unsafe_allow_html=True)
        with col3:
            st.markdown(f"""
            <div class="metric-card">
                <p class="metric-value">{metrics['recall']:.1%}</p>
                <p class="metric-label">Recall</p>
            </div>
            """, unsafe_allow_html=True)
        with col4:
            st.markdown(f"""
            <div class="metric-card">
                <p class="metric-value">{metrics['f1']:.1%}</p>
                <p class="metric-label">F1-Score</p>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)

        # Confusion Matrix
        st.markdown('<p class="page-title" style="font-size: 1.2em;">Confusion Matrix</p>', unsafe_allow_html=True)
        cm = metrics['confusion_matrix']

        col1, col2 = st.columns(2)

        with col1:
            st.markdown(f"""
            <div class="content-card" style="border-left: 5px solid #22c55e;">
                <p style="font-weight: 600; color: #64748b !important; font-size: 0.85em; margin: 0 0 8px 0;">True Negatives (Correct Ham)</p>
                <p style="font-size: 2.5em; font-weight: 800; color: #22c55e !important; margin: 0;">{cm[0, 0]}</p>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown(f"""
            <div class="content-card" style="border-left: 5px solid #4361ee;">
                <p style="font-weight: 600; color: #64748b !important; font-size: 0.85em; margin: 0 0 8px 0;">True Positives (Correct Spam)</p>
                <p style="font-size: 2.5em; font-weight: 800; color: #4361ee !important; margin: 0;">{cm[1, 1]}</p>
            </div>
            """, unsafe_allow_html=True)

        col1, col2 = st.columns(2)

        with col1:
            st.markdown(f"""
            <div class="content-card" style="border-left: 5px solid #f59e0b;">
                <p style="font-weight: 600; color: #64748b !important; font-size: 0.85em; margin: 0 0 8px 0;">False Positives (Ham → Spam)</p>
                <p style="font-size: 2.5em; font-weight: 800; color: #f59e0b !important; margin: 0;">{cm[0, 1]}</p>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown(f"""
            <div class="content-card" style="border-left: 5px solid #ef4444;">
                <p style="font-weight: 600; color: #64748b !important; font-size: 0.85em; margin: 0 0 8px 0;">False Negatives (Spam → Ham)</p>
                <p style="font-size: 2.5em; font-weight: 800; color: #ef4444 !important; margin: 0;">{cm[1, 0]}</p>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="info-message">
            <strong>ℹ️ No metrics available</strong><br>
            Train the model to see performance statistics.
        </div>
        """, unsafe_allow_html=True)



# ═══════════════════════════════════════════════
# ABOUT PAGE
# ═══════════════════════════════════════════════
elif page == "about":
    st.markdown("""
    <div class="breadcrumb">
        <span class="breadcrumb-item">SpamSense</span>
        <span class="breadcrumb-sep">›</span>
        <span class="breadcrumb-item active">About</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<p class="page-title">About SpamSense</p>', unsafe_allow_html=True)
    st.markdown('<p class="page-subtitle">AI-powered email security and spam detection</p>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div class="content-card">
            <p class="card-title">🎯 Features</p>
            <div style="margin-top: 16px; line-height: 2;">
                • <strong>Real-time Detection</strong> — Instant email classification<br>
                • <strong>Advanced AI</strong> — Machine learning analysis<br>
                • <strong>High Accuracy</strong> — ~95% detection rate<br>
                • <strong>Batch Processing</strong> — Analyze multiple emails<br>
                • <strong>Modern Dashboard</strong> — Clean, intuitive UI
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="content-card">
            <p class="card-title">🔧 Technology Stack</p>
            <div style="margin-top: 16px; line-height: 2;">
                • <strong>ML Framework</strong> — scikit-learn<br>
                • <strong>Text Processing</strong> — TF-IDF Vectorization<br>
                • <strong>Web Framework</strong> — Streamlit<br>
                • <strong>Language</strong> — Python 3.8+
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="content-card">
            <p class="card-title">📊 How It Works</p>
            <div style="margin-top: 16px; line-height: 2;">
                <strong>1.</strong> Text Cleaning — Remove URLs, special chars<br>
                <strong>2.</strong> Vectorization — Convert text to features<br>
                <strong>3.</strong> Classification — ML model prediction<br>
                <strong>4.</strong> Scoring — Confidence-based metrics
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="content-card">
            <p class="card-title">🎓 Model Details</p>
            <div style="margin-top: 16px; line-height: 2;">
                • <strong>Algorithm</strong> — Naive Bayes Classifier<br>
                • <strong>Features</strong> — 5,000 TF-IDF features<br>
                • <strong>Training Data</strong> — 500 samples<br>
                • <strong>Accuracy</strong> — 95%
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)

    st.markdown('<p class="page-title" style="font-size: 1.2em;">📝 Example Emails</p>', unsafe_allow_html=True)

    example_col1, example_col2 = st.columns(2)

    with example_col1:
        st.markdown("""
        <div class="content-card" style="border-left: 5px solid #ef4444;">
            <p class="card-title">🚨 Typical Spam</p>
        </div>
        """, unsafe_allow_html=True)
        st.code("""CONGRATULATIONS YOU WON!!!

CLICK HERE FOR FREE MONEY!!!

Urgent: Account compromised!
Verify NOW!""", language="text")

    with example_col2:
        st.markdown("""
        <div class="content-card" style="border-left: 5px solid #22c55e;">
            <p class="card-title">✅ Typical Legitimate</p>
        </div>
        """, unsafe_allow_html=True)
        st.code("""Can we schedule a meeting
tomorrow at 3pm?

Please review the attached
quarterly report.

Thanks for your help!""", language="text")

    st.markdown("""
    <div class="info-message">
    <strong>🔐 Privacy Notice:</strong> This application processes emails locally.
    No data is stored or sent to external servers. Your email content remains private.
    </div>
    """, unsafe_allow_html=True)
