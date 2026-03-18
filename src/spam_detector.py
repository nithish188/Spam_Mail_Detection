"""
Spam email detector interface
Provides easy-to-use detection and analysis functions
"""

import pickle
from data_preprocessing import EmailPreprocessor

class SpamDetector:
    def __init__(self, model, vectorizer):
        """
        Initialize spam detector
        
        Args:
            model: Trained sklearn model
            vectorizer: TfidfVectorizer used for email preprocessing
        """
        self.model = model
        self.vectorizer = vectorizer
        self.preprocessor = EmailPreprocessor()
        self.preprocessor.vectorizer = vectorizer
    
    def is_spam(self, email_text):
        """
        Check if an email is spam
        
        Args:
            email_text: Email body text
            
        Returns:
            bool: True if spam, False if ham
        """
        cleaned = self.preprocessor.clean_email(email_text)
        vector = self.vectorizer.transform([cleaned])
        prediction = self.model.predict(vector)[0]
        return bool(prediction)
    
    def get_spam_probability(self, email_text):
        """
        Get probability that email is spam
        
        Args:
            email_text: Email body text
            
        Returns:
            float: Probability between 0 and 1
        """
        cleaned = self.preprocessor.clean_email(email_text)
        vector = self.vectorizer.transform([cleaned])
        
        if hasattr(self.model, 'predict_proba'):
            proba = self.model.predict_proba(vector)[0]
            return float(proba[1])  # Probability of spam class
        elif hasattr(self.model, 'decision_function'):
            score = self.model.decision_function(vector)[0]
            # Convert to probability using sigmoid
            prob = 1 / (1 + (-score).__abs__())
            return float(prob)
        else:
            return float(self.model.predict(vector)[0])
    
    def classify_batch(self, emails):
        """
        Classify multiple emails at once
        
        Args:
            emails: List of email texts
            
        Returns:
            list: List of predictions (0=ham, 1=spam)
        """
        cleaned = [self.preprocessor.clean_email(email) for email in emails]
        vectors = self.vectorizer.transform(cleaned)
        predictions = self.model.predict(vectors)
        return list(predictions)
    
    def get_probabilities_batch(self, emails):
        """
        Get spam probabilities for multiple emails
        
        Args:
            emails: List of email texts
            
        Returns:
            list: List of spam probabilities
        """
        cleaned = [self.preprocessor.clean_email(email) for email in emails]
        vectors = self.vectorizer.transform(cleaned)
        
        probabilities = []
        for i, email_vector in enumerate(vectors):
            if hasattr(self.model, 'predict_proba'):
                proba = self.model.predict_proba(email_vector)[0][1]
            elif hasattr(self.model, 'decision_function'):
                score = self.model.decision_function(email_vector)[0]
                proba = 1 / (1 + (-score).__abs__())
            else:
                proba = float(self.model.predict(email_vector)[0])
            probabilities.append(proba)
        
        return probabilities
    
    def analyze_email(self, email_text, threshold=0.5):
        """
        Provide detailed analysis of an email
        
        Args:
            email_text: Email body text
            threshold: Decision threshold for spam classification
            
        Returns:
            dict: Analysis results
        """
        probability = self.get_spam_probability(email_text)
        prediction = probability >= threshold
        
        return {
            'text': email_text[:100] + '...' if len(email_text) > 100 else email_text,
            'spam_probability': round(probability, 4),
            'is_spam': bool(prediction),
            'confidence': round(abs(probability - 0.5) * 2, 4)
        }
    
    @staticmethod
    def save(detector, filepath):
        """Save detector to file"""
        with open(filepath, 'wb') as f:
            pickle.dump(detector, f)
        print(f"Detector saved to {filepath}")
    
    @staticmethod
    def load(filepath):
        """Load detector from file"""
        with open(filepath, 'rb') as f:
            detector = pickle.load(f)
        print(f"Detector loaded from {filepath}")
        return detector
