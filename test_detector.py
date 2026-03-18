"""
Test script for spam detector
Quick testing and demonstration
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.spam_detector import SpamDetector
from src.model import SpamDetectorModel
from src.data_preprocessing import EmailPreprocessor, create_sample_data
import pickle

def test_detector():
    """Test the detector with example emails"""
    
    print("="*70)
    print("SPAM EMAIL DETECTOR - TEST AND DEMONSTRATION")
    print("="*70)
    
    # Check if models exist
    model_path = 'models/best_model_naive_bayes.pkl'
    vectorizer_path = 'models/vectorizer.pkl'
    
    if not os.path.exists(model_path):
        print("\n⚠️  Model not found. Running main pipeline first...")
        import main
        main.main()
    
    # Load model and vectorizer
    print("\n[Loading] Model and vectorizer...")
    with open(model_path, 'rb') as f:
        model = pickle.load(f)
    
    with open(vectorizer_path, 'rb') as f:
        vectorizer = pickle.load(f)
    
    # Create detector
    detector = SpamDetector(model, vectorizer)
    print("✓ Detector loaded successfully!")
    
    # Define test emails
    test_cases = [
        {
            "email": "Hi Sarah, I hope this email finds you well. Can we schedule a meeting to discuss the Q2 budget?",
            "expected": "HAM"
        },
        {
            "email": "CLICK HERE NOW!!! WIN FREE IPHONE 15 PRIZE MONEY!!!",
            "expected": "SPAM"
        },
        {
            "email": "Please review the attached quarterly report when you have a chance.",
            "expected": "HAM"
        },
        {
            "email": "Congratulations! You have been selected as our special customer. Claim your reward NOW!!!",
            "expected": "SPAM"
        },
        {
            "email": "The project deadline has been moved to next Friday.",
            "expected": "HAM"
        },
        {
            "email": "YOU WON! Claim your prize! Click here for FREE MONEY!!!",
            "expected": "SPAM"
        },
        {
            "email": "Thank you for your help on the presentation yesterday.",
            "expected": "HAM"
        },
        {
            "email": "URGENT: Your account will be closed! Verify now or lose access!",
            "expected": "SPAM"
        }
    ]
    
    # Run tests
    print("\n" + "="*70)
    print("TEST RESULTS")
    print("="*70)
    
    correct = 0
    total = len(test_cases)
    
    for i, test in enumerate(test_cases, 1):
        email = test['email']
        expected = test['expected']
        
        # Get prediction
        is_spam = detector.is_spam(email)
        probability = detector.get_spam_probability(email)
        prediction = "SPAM" if is_spam else "HAM"
        
        # Check correctness
        correct_pred = prediction == expected
        correct += correct_pred
        
        status = "✓ PASS" if correct_pred else "✗ FAIL"
        
        print(f"\nTest {i}: {status}")
        print(f"  Email: {email[:60]}...")
        print(f"  Expected: {expected}, Got: {prediction}")
        print(f"  Spam Probability: {probability:.4f}")
        print(f"  Confidence: {abs(probability - 0.5) * 2:.4f}")
    
    # Summary
    accuracy = (correct / total) * 100
    print("\n" + "="*70)
    print(f"SUMMARY: {correct}/{total} tests passed ({accuracy:.1f}% accuracy)")
    print("="*70)
    
    # Interactive mode
    print("\n" + "="*70)
    print("INTERACTIVE MODE")
    print("="*70)
    print("Enter emails to classify (type 'quit' to exit)")
    print()
    
    while True:
        user_email = input("Enter email text: ").strip()
        
        if user_email.lower() == 'quit':
            print("Exiting...")
            break
        
        if not user_email:
            continue
        
        analysis = detector.analyze_email(user_email)
        status = "SPAM ⚠️" if analysis['is_spam'] else "LEGITIMATE ✓"
        
        print(f"\n  Status: {status}")
        print(f"  Spam Probability: {analysis['spam_probability']:.4f}")
        print(f"  Confidence: {analysis['confidence']:.4f}")
        print()

if __name__ == "__main__":
    test_detector()
