"""
Sentinel AI - Image Analyzer
Deepfake and AI-generated image detection.
Uses mock inference for demonstration - replace with trained model.
"""
import random
from pathlib import Path
from typing import Dict, Optional, Tuple


class ImageAnalyzer:
    """
    Image analysis model for detecting AI-generated and manipulated images.
    
    In production, this would use EfficientNet-B0 or Xception as backbone.
    Currently uses placeholder logic for demonstration.
    """
    
    def __init__(self):
        """Initialize the image analyzer."""
        self.loaded = True
        self.target_size = (224, 224)  # EfficientNet-B0 input size
    
    def _load_image(self, file_path: Path) -> Optional[Tuple]:
        """
        Load and preprocess image.
        
        Returns:
            Tuple of (image_array, original_size) or None
        """
        try:
            from PIL import Image
            import numpy as np
            
            img = Image.open(file_path)
            original_size = img.size
            
            # Convert to RGB if needed
            if img.mode != "RGB":
                img = img.convert("RGB")
            
            # Resize for model
            img_resized = img.resize(self.target_size)
            img_array = np.array(img_resized) / 255.0
            
            return img_array, original_size
        except Exception as e:
            print(f"Image loading failed: {e}")
            return None
    
    def _extract_features(self, img_array) -> Dict:
        """
        Extract basic image features.
        
        In production, this would use the CNN backbone.
        """
        import numpy as np
        
        # Basic statistics
        return {
            "mean_brightness": float(np.mean(img_array)),
            "std_brightness": float(np.std(img_array)),
            "color_distribution": [float(np.mean(img_array[:, :, i])) for i in range(3)]
        }
    
    def analyze(self, file_path: Path) -> Dict:
        """
        Analyze image for AI generation or manipulation.
        
        Args:
            file_path: Path to image file
            
        Returns:
            Dict with analysis results
        """
        result = self._load_image(file_path)
        
        if result is None:
            # Return uncertain results on error
            return {
                "real_probability": 0.5,
                "ai_generated": 0.25,
                "manipulated": 0.25
            }
        
        img_array, original_size = result
        features = self._extract_features(img_array)
        
        # Mock inference with controlled variation
        # In production, this would be replaced with actual model inference
        base_real = 0.7
        base_ai = 0.2
        base_manip = 0.1
        
        # Adjust based on basic heuristics (placeholder logic)
        if features["std_brightness"] < 0.1:
            # Very uniform images are slightly more suspicious
            base_real -= 0.1
            base_ai += 0.05
            base_manip += 0.05
        
        # Add controlled randomness for demonstration
        noise = random.uniform(-0.15, 0.15)
        base_real = max(0.1, min(0.95, base_real + noise))
        
        # Normalize probabilities
        total = base_real + base_ai + base_manip
        
        return {
            "real_probability": base_real / total,
            "ai_generated": base_ai / total + random.uniform(0, 0.1),
            "manipulated": base_manip / total + random.uniform(0, 0.05)
        }


# Singleton instance
_analyzer = None


def get_image_analyzer() -> ImageAnalyzer:
    """Get or create the image analyzer instance."""
    global _analyzer
    if _analyzer is None:
        _analyzer = ImageAnalyzer()
    return _analyzer
