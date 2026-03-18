"""
Spam email detector model module
Trains and evaluates various ML models
"""

import pickle
import numpy as np
import warnings
warnings.filterwarnings('ignore')
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import LinearSVC
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    confusion_matrix, classification_report, roc_auc_score
)

class SpamDetectorModel:
    def __init__(self, model_type='naive_bayes'):
        """
        Initialize spam detector model
        
        Args:
            model_type: 'naive_bayes', 'logistic_regression', 'random_forest', or 'svm'
        """
        self.model_type = model_type
        self.model = self._create_model(model_type)
        self.metrics = {}
    
    def _create_model(self, model_type):
        """Create the specified model"""
        if model_type == 'naive_bayes':
            return MultinomialNB(alpha=1.0)
        elif model_type == 'logistic_regression':
            return LogisticRegression(max_iter=1000, random_state=42)
        elif model_type == 'random_forest':
            return RandomForestClassifier(n_estimators=100, random_state=42)
        elif model_type == 'svm':
            return LinearSVC(random_state=42, max_iter=2000)
        else:
            raise ValueError(f"Unknown model type: {model_type}")
    
    def train(self, X_train, y_train):
        """Train the model"""
        print(f"Training {self.model_type} model...")
        self.model.fit(X_train, y_train)
        print("Model training completed!")
    
    def predict(self, X):
        """Make predictions"""
        return self.model.predict(X)
    
    def predict_proba(self, X):
        """Get prediction probabilities (if available)"""
        if hasattr(self.model, 'predict_proba'):
            return self.model.predict_proba(X)
        elif hasattr(self.model, 'decision_function'):
            # Convert decision function to probabilities
            scores = self.model.decision_function(X)
            return np.column_stack([1 - 1/(1 + np.exp(-scores)), 1/(1 + np.exp(-scores))])
        else:
            return None
    
    def evaluate(self, X_test, y_test):
        """Evaluate model on test set"""
        y_pred = self.predict(X_test)
        
        self.metrics = {
            'accuracy': accuracy_score(y_test, y_pred),
            'precision': precision_score(y_test, y_pred, zero_division=0),
            'recall': recall_score(y_test, y_pred, zero_division=0),
            'f1': f1_score(y_test, y_pred, zero_division=0),
            'confusion_matrix': confusion_matrix(y_test, y_pred)
        }
        
        # Add ROC-AUC if probabilities are available
        try:
            y_proba = self.predict_proba(X_test)
            if y_proba is not None:
                self.metrics['roc_auc'] = roc_auc_score(y_test, y_proba[:, 1])
        except:
            pass
        
        return self.metrics
    
    def print_evaluation(self):
        """Print evaluation metrics"""
        if not self.metrics:
            print("No evaluation metrics available. Run evaluate() first.")
            return
        
        print("\n" + "="*50)
        print(f"Model: {self.model_type.upper()}")
        print("="*50)
        print(f"Accuracy:  {self.metrics['accuracy']:.4f}")
        print(f"Precision: {self.metrics['precision']:.4f}")
        print(f"Recall:    {self.metrics['recall']:.4f}")
        print(f"F1-Score:  {self.metrics['f1']:.4f}")
        if 'roc_auc' in self.metrics:
            print(f"ROC-AUC:   {self.metrics['roc_auc']:.4f}")
        
        cm = self.metrics['confusion_matrix']
        print(f"\nConfusion Matrix:")
        print(f"  True Negatives:  {cm[0, 0]}")
        print(f"  False Positives: {cm[0, 1]}")
        print(f"  False Negatives: {cm[1, 0]}")
        print(f"  True Positives:  {cm[1, 1]}")
        print("="*50)
    
    def save(self, filepath):
        """Save model to file"""
        with open(filepath, 'wb') as f:
            pickle.dump(self.model, f)
        print(f"Model saved to {filepath}")
    
    def load(self, filepath):
        """Load model from file"""
        with open(filepath, 'rb') as f:
            self.model = pickle.load(f)
        print(f"Model loaded from {filepath}")
