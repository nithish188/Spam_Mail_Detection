"""
Main script for spam email detector
Trains models and provides detection interface
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.data_preprocessing import EmailPreprocessor, create_sample_data
from src.model import SpamDetectorModel
from src.spam_detector import SpamDetector
import pickle

def main():
    print("="*60)
    print("SPAM EMAIL DETECTOR - MAIN PIPELINE")
    print("="*60)
    
    # Paths
    data_path = 'data/emails.csv'
    model_dir = 'models'
    
    # Create sample data if it doesn't exist
    if not os.path.exists(data_path):
        print("\n[Step 1] Creating sample email data...")
        create_sample_data(data_path, n_samples=500)
    else:
        print(f"\n[Step 1] Using existing data from {data_path}")
    
    # Load and preprocess data
    print("\n[Step 2] Loading and preprocessing data...")
    preprocessor = EmailPreprocessor(test_size=0.2, random_state=42)
    emails, labels = preprocessor.load_data(data_path)
    X_train, X_test, y_train, y_test = preprocessor.preprocess(emails, labels)
    print(f"  Training samples: {X_train.shape[0]}")
    print(f"  Test samples: {X_test.shape[0]}")
    print(f"  Features: {X_train.shape[1]}")
    
    # Train models
    print("\n[Step 3] Training multiple models...")
    models_to_train = ['naive_bayes', 'logistic_regression']
    best_model = None
    best_f1 = 0
    
    for model_type in models_to_train:
        print(f"\n  Training {model_type}...")
        model = SpamDetectorModel(model_type)
        model.train(X_train, y_train)
        metrics = model.evaluate(X_test, y_test)
        model.print_evaluation()
        
        # Track best model
        if metrics['f1'] > best_f1:
            best_f1 = metrics['f1']
            best_model = model
    
    # Save best model
    print("\n[Step 4] Saving best model...")
    os.makedirs(model_dir, exist_ok=True)
    best_model_path = os.path.join(model_dir, f"best_model_{best_model.model_type}.pkl")
    best_model.save(best_model_path)
    
    # Save vectorizer
    vectorizer_path = os.path.join(model_dir, "vectorizer.pkl")
    with open(vectorizer_path, 'wb') as f:
        pickle.dump(preprocessor.vectorizer, f)
    print(f"Vectorizer saved to {vectorizer_path}")
    
    # Create and test detector
    print("\n[Step 5] Creating spam detector...")
    detector = SpamDetector(best_model.model, preprocessor.vectorizer)
    
    # Test with sample emails
    print("\n[Step 6] Testing detector with sample emails...")
    test_emails = [
        "Hi John, can we schedule a meeting tomorrow?",
        "CONGRATULATIONS YOU WON A PRIZE!!! CLICK HERE NOW!!!",
        "The project report is ready for your review.",
        "You have been selected for a special offer! Act now!"
    ]
    
    for email in test_emails:
        analysis = detector.analyze_email(email)
        status = "SPAM" if analysis['is_spam'] else "HAM"
        print(f"\n  [{status}] Probability: {analysis['spam_probability']}")
        print(f"         Text: {analysis['text']}")
    
    print("\n" + "="*60)
    print("PIPELINE COMPLETED SUCCESSFULLY!")
    print(f"Best model: {best_model.model_type} (F1: {best_f1:.4f})")
    print(f"Detector ready for use!")
    print("="*60)
    
    return detector, best_model

if __name__ == "__main__":
    detector, model = main()
