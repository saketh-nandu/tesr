"""
Sentinel AI - Text Analyzer
Multi-head classifier for AI detection and scam intent analysis.
Uses mock inference for demonstration - replace with trained model.
"""
import re
import random
from typing import Dict, Tuple


class TextAnalyzer:
    """
    Text analysis model for detecting AI-generated content and scam intent.
    
    In production, this would use a fine-tuned DeBERTa-v3 or RoBERTa model.
    Currently uses pattern-based heuristics for demonstration.
    """
    
    def __init__(self):
        """Initialize the text analyzer."""
        self.loaded = True
        
        # Scam indicator patterns
        self.urgency_patterns = [
            r'\b(urgent|immediately|now|today|hurry|quick|fast|limited time)\b',
            r'\b(act now|don\'t wait|expires|deadline)\b',
            r'!{2,}',  # Multiple exclamation marks
        ]
        
        self.financial_patterns = [
            r'\b(won|winner|prize|lottery|million|money|cash|dollars?)\b',
            r'\b(bank|account|transfer|payment|credit|debit)\b',
            r'\b(invest|profit|earnings|income|rich)\b',
            r'\$[\d,]+',  # Dollar amounts
        ]
        
        self.phishing_patterns = [
            r'\b(verify|confirm|update|validate)\s+your\s+(account|password|information)\b',
            r'\b(click\s+here|click\s+below|click\s+the\s+link)\b',
            r'\b(suspended|locked|compromised|unauthorized)\b',
            r'\b(ssn|social\s+security|password|pin)\b',
        ]
        
        self.impersonation_patterns = [
            r'\b(official|government|irs|fbi|ssa|microsoft|apple|amazon|google)\b',
            r'\b(support|helpdesk|customer\s+service|security\s+team)\b',
            r'\b(dear\s+customer|dear\s+user|dear\s+member)\b',
        ]
        
        self.ai_patterns = [
            r'\b(as an ai|i\'m an ai|language model)\b',
            r'\b(certainly|absolutely|i\'d be happy to)\b',
            r'\b(however|furthermore|additionally|moreover)\b',
        ]
    
    def _count_pattern_matches(self, text: str, patterns: list) -> int:
        """Count pattern matches in text."""
        text_lower = text.lower()
        count = 0
        for pattern in patterns:
            matches = re.findall(pattern, text_lower, re.IGNORECASE)
            count += len(matches)
        return count
    
    def _calculate_ai_likelihood(self, text: str) -> float:
        """
        Estimate likelihood text is AI-generated.
        
        Looks for:
        - Overly formal language
        - Consistent sentence structure
        - AI disclosure patterns
        """
        score = 0.0
        
        # Check for AI disclosure
        ai_matches = self._count_pattern_matches(text, self.ai_patterns)
        score += min(ai_matches * 0.2, 0.6)
        
        # Check sentence consistency (AI tends to be more uniform)
        sentences = re.split(r'[.!?]+', text)
        if len(sentences) > 3:
            lengths = [len(s.split()) for s in sentences if s.strip()]
            if lengths:
                avg_len = sum(lengths) / len(lengths)
                variance = sum((l - avg_len) ** 2 for l in lengths) / len(lengths)
                # Low variance = more AI-like
                if variance < 10:
                    score += 0.2
        
        # Add some randomness for demonstration
        score += random.uniform(-0.1, 0.1)
        
        return max(0.0, min(1.0, score))
    
    def _calculate_scam_intent(self, text: str) -> float:
        """Calculate probability of scam intent."""
        score = 0.0
        
        phishing = self._count_pattern_matches(text, self.phishing_patterns)
        score += min(phishing * 0.15, 0.6)
        
        financial = self._count_pattern_matches(text, self.financial_patterns)
        if phishing > 0:  # Financial terms more suspicious with phishing
            score += min(financial * 0.1, 0.3)
        
        return max(0.0, min(1.0, score))
    
    def _calculate_urgency(self, text: str) -> float:
        """Calculate urgency level."""
        matches = self._count_pattern_matches(text, self.urgency_patterns)
        score = min(matches * 0.15, 0.9)
        return max(0.0, min(1.0, score))
    
    def _calculate_financial_request(self, text: str) -> float:
        """Detect financial requests."""
        matches = self._count_pattern_matches(text, self.financial_patterns)
        score = min(matches * 0.12, 0.8)
        return max(0.0, min(1.0, score))
    
    def _calculate_impersonation(self, text: str) -> float:
        """Detect impersonation attempts."""
        matches = self._count_pattern_matches(text, self.impersonation_patterns)
        score = min(matches * 0.15, 0.8)
        return max(0.0, min(1.0, score))
    
    def analyze(self, text: str) -> Dict[str, float]:
        """
        Analyze text for AI generation and scam indicators.
        
        Args:
            text: Text content to analyze
            
        Returns:
            Dict with classification scores
        """
        return {
            "ai_likelihood": self._calculate_ai_likelihood(text),
            "scam_intent": self._calculate_scam_intent(text),
            "urgency": self._calculate_urgency(text),
            "financial_request": self._calculate_financial_request(text),
            "impersonation": self._calculate_impersonation(text)
        }


# Singleton instance
_analyzer = None


def get_text_analyzer() -> TextAnalyzer:
    """Get or create the text analyzer instance."""
    global _analyzer
    if _analyzer is None:
        _analyzer = TextAnalyzer()
    return _analyzer
