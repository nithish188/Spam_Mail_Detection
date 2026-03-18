# Spam Email Detector

A machine learning-based spam email detection system using scikit-learn with a **Streamlit web interface**. Features accurate classification of emails as spam or legitimate (ham) using ML models.

## Features

✅ **Web-Based Interface** - Interactive Streamlit app (no terminal needed)
✅ **Real-time Detection** - Instant email classification
✅ **Multiple ML Models** - Naive Bayes, Logistic Regression, Random Forest, SVM
✅ **Advanced Text Processing** - TF-IDF, N-grams, stop word removal
✅ **Batch Testing** - Analyze multiple emails at once
✅ **Comprehensive Metrics** - Accuracy, Precision, Recall, F1-Score
✅ **Easy Deployment** - Deploy to Streamlit Cloud with one click

## Project Structure

```
AIML_Project/
├── app.py                      # Streamlit web application
├── main.py                     # Training pipeline (legacy)
├── test_detector.py            # Testing script
├── requirements.txt            # Python dependencies
├── .gitignore
├── .streamlit/
│   └── config.toml            # Streamlit configuration
├── data/
│   └── emails.csv             # Sample email dataset
├── models/
│   ├── best_model_naive_bayes.pkl
│   └── vectorizer.pkl
└── src/
    ├── data_preprocessing.py
    ├── model.py
    └── spam_detector.py
```

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the Streamlit App
```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## Usage Modes

### 📧 Detector Tab
- Paste email content
- Get instant spam/ham classification
- See spam probability and confidence score

### 🚀 Train Model Tab
- Train a new model with sample data
- View performance metrics
- Automatically saves the trained model

### 📊 Batch Testing Tab
- Test multiple emails at once
- Get summary statistics
- See spam vs legitimate counts

### 📖 About Tab
- Learn how the system works
- See example emails
- View model performance metrics

## Deployment

### Deploy to Streamlit Cloud (Free)

1. Push your project to GitHub
2. Go to [Streamlit Cloud](https://share.streamlit.io)
3. Deploy by connecting your GitHub repository
4. Your app is live!

### Local Deployment
```bash
streamlit run app.py --logger.level=warning
```

## Python Code Usage (Advanced)

```python
from src.spam_detector import SpamDetector
import pickle

# Load trained model
with open('models/best_model_naive_bayes.pkl', 'rb') as f:
    model = pickle.load(f)
with open('models/vectorizer.pkl', 'rb') as f:
    vectorizer = pickle.load(f)

detector = SpamDetector(model, vectorizer)

# Single email classification
is_spam = detector.is_spam("CLICK HERE FOR FREE MONEY!!!")  # True
probability = detector.get_spam_probability("Hi, can we meet?")  # ~0.05

# Detailed analysis
analysis = detector.analyze_email("Some email text")
print(analysis)
# Output:
# {
#     'text': 'Some email text...',
#     'spam_probability': 0.1234,
#     'is_spam': False,
#     'confidence': 0.7532
# }

# Batch processing
emails = ["Email 1", "Email 2", "Email 3"]
predictions = detector.classify_batch(emails)
probabilities = detector.get_probabilities_batch(emails)
```

## Training the Model

```bash
# Train from scratch
python main.py

# This will:
# 1. Create sample email data
# 2. Preprocess and vectorize emails
# 3. Train multiple models
# 4. Evaluate and save the best model
# 5. Display performance metrics
```

## Dataset Format

Create your own `data/emails.csv`:

```csv
email,label
"Hello, can we schedule a meeting?",0
"CONGRATULATIONS YOU WON A PRIZE!!!",1
"Project report attached",0
"Click here for FREE MONEY!!!",1
```

Columns:
- `email`: Email text content
- `label`: 0 = legitimate (ham), 1 = spam

## Model Performance

Expected metrics:
- **Accuracy**: ~95%
- **Precision**: ~94%
- **Recall**: ~96%
- **F1-Score**: ~95%

## Text Processing Pipeline

1. **URL Removal** - Strip HTTP/HTTPS links
2. **Email Removal** - Remove email addresses
3. **Lowercasing** - Normalize case
4. **Special Character Removal** - Clean text
5. **Stop Word Removal** - Filter common words
6. **TF-IDF Vectorization** - Convert to numerical features
7. **N-gram Features** - Capture word patterns

## Key Classes

### SpamDetector
Main detection interface:
```python
detector.is_spam(email_text)                    # bool
detector.get_spam_probability(email_text)      # float 0-1
detector.classify_batch(emails)                 # list
detector.get_probabilities_batch(emails)       # list
detector.analyze_email(email_text)             # dict
```

### EmailPreprocessor
Data preprocessing and vectorization:
```python
preprocessor = EmailPreprocessor()
X_train, X_test, y_train, y_test = preprocessor.preprocess(emails, labels)
```

### SpamDetectorModel
ML model training:
```python
model = SpamDetectorModel('naive_bayes')
model.train(X_train, y_train)
metrics = model.evaluate(X_test, y_test)
model.save('path/to/model.pkl')
```

## Requirements

- Python 3.8+
- numpy >= 1.24.0
- pandas >= 2.0.0
- scikit-learn >= 1.3.0
- streamlit >= 1.28.0
- matplotlib >= 3.7.0
- seaborn >= 0.12.0

## Troubleshooting

**"ModuleNotFoundError: No module named 'sklearn'"**
```bash
pip install scikit-learn
```

**Streamlit not found**
```bash
pip install streamlit
```

**Model not loading**
- Ensure `models/` directory exists
- Run the Train Model tab first to create the model

## Performance Tips

- Train with 500+ emails for better accuracy
- Use balanced datasets (similar spam/ham counts)
- Include diverse email types in training data
- Retrain periodically with new data

## Future Improvements

- Deep learning models (LSTM, Transformers)
- Custom model upload
- Email attachment scanning
- Real-time spam database integration
- Multi-language support
- API endpoint deployment

## License

Open source project for educational purposes.

## Author

Created as an AI/ML learning project.
