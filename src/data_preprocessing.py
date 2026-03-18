"""
Data preprocessing module for spam email detector
Handles data loading, cleaning, and feature extraction
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
import re
import string
import warnings
warnings.filterwarnings('ignore')

class EmailPreprocessor:
    def __init__(self, test_size=0.2, random_state=42):
        self.test_size = test_size
        self.random_state = random_state
        self.vectorizer = TfidfVectorizer(
            max_features=5000,
            lowercase=True,
            stop_words='english',
            ngram_range=(1, 2),
            min_df=2,
            max_df=0.8
        )
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None
    
    @staticmethod
    def clean_email(email_text):
        """Clean email text by removing special characters and extra whitespace"""
        if not isinstance(email_text, str):
            return ""
        
        # Convert to lowercase
        email_text = email_text.lower()
        
        # Remove URLs
        email_text = re.sub(r'http\S+|www\S+|https\S+', '', email_text, flags=re.MULTILINE)
        
        # Remove email addresses
        email_text = re.sub(r'\S+@\S+', '', email_text)
        
        # Remove special characters and digits
        email_text = re.sub(r'[^a-zA-Z\s]', '', email_text)
        
        # Remove extra whitespace
        email_text = ' '.join(email_text.split())
        
        return email_text
    
    def load_data(self, filepath, label_column='label', text_column='email'):
        """
        Load data from CSV file
        Expected columns: 'email' (text), 'label' (0=ham, 1=spam)
        """
        df = pd.read_csv(filepath)
        return df[text_column].values, df[label_column].values
    
    def preprocess(self, emails, labels=None):
        """Preprocess emails and split into train/test sets"""
        # Clean emails
        cleaned_emails = [self.clean_email(email) for email in emails]
        
        if labels is not None:
            # Split data
            X_train, X_test, y_train, y_test = train_test_split(
                cleaned_emails, labels,
                test_size=self.test_size,
                random_state=self.random_state,
                stratify=labels
            )
            
            # Vectorize
            self.X_train = self.vectorizer.fit_transform(X_train)
            self.X_test = self.vectorizer.transform(X_test)
            self.y_train = y_train
            self.y_test = y_test
            
            return self.X_train, self.X_test, y_train, y_test
        else:
            # Just transform
            X = self.vectorizer.transform(cleaned_emails)
            return X
    
    def get_feature_names(self):
        """Get feature names from vectorizer"""
        return self.vectorizer.get_feature_names_out()

def create_sample_data(filepath, n_samples=500):
    """Create sample email data for demonstration"""
    sample_emails = {
        'email': [
            # Spam examples
            'CLICK HERE NOW!!! WIN $1000 PRIZE MONEY!!!',
            'Congratulations! You have won a FREE IPHONE 15',
            'Urgent: Your account has been compromised. Click link to verify',
            'Do you want to make $5000 from home? Click here now!',
            'FREE PHARMACUTICALS NO PRESCRIPTION',
            'You are the lucky WINNER of a LUXURY VACATION',
            'Click here for FREE MONEY and CASH NOW',
            'Your bank account has been LOCKED. Verify immediately',
            'HOT SINGLES IN YOUR AREA WANT TO MEET YOU',
            'ENLARGE YOUR MANHOOD WITH THIS ONE WEIRD TRICK',
            # Ham examples
            'Hi Sarah, can we schedule a meeting for tomorrow at 3pm?',
            'The quarterly report is attached to this email.',
            'Thanks for your help with the project!',
            'Please find the budget allocation spreadsheet below.',
            'I wanted to follow up on our discussion yesterday.',
            'The conference will be held on March 15th.',
            'Your password reset request has been processed.',
            'Meeting notes from today are attached.',
            'Let me know if you need any additional information.',
            'The new feature is now available in production.',
        ],
        'label': [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    }
    
    # Repeat to reach n_samples
    df = pd.DataFrame(sample_emails)
    while len(df) < n_samples:
        df = pd.concat([df, df], ignore_index=True)
    
    df = df.head(n_samples).reset_index(drop=True)
    df.to_csv(filepath, index=False)
    print(f"Sample data created: {filepath} ({len(df)} samples)")
    return df
