"""
Sentinel AI - Video Analyzer
Deepfake video detection with frame sampling.
Uses mock inference for demonstration - replace with trained model.
"""
import random
from pathlib import Path
from typing import Dict, List, Optional


class VideoAnalyzer:
    """
    Video analysis model for detecting deepfake videos.
    
    In production, this would use CNN + temporal pooling.
    Samples 1 frame per second, max 8 frames.
    """
    
    def __init__(self):
        """Initialize the video analyzer."""
        self.loaded = True
        self.target_size = (224, 224)
        self.max_frames = 8
        self.fps_sample = 1  # Sample 1 frame per second
    
    def _get_video_info(self, file_path: Path) -> Dict:
        """
        Get video metadata.
        
        Returns:
            Dict with duration, fps, frame_count
        """
        try:
            import cv2
            
            cap = cv2.VideoCapture(str(file_path))
            fps = cap.get(cv2.CAP_PROP_FPS)
            frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            duration = frame_count / fps if fps > 0 else 0
            cap.release()
            
            return {
                "duration": duration,
                "fps": fps,
                "frame_count": frame_count
            }
        except Exception as e:
            print(f"Video info extraction failed: {e}")
            return {"duration": 0, "fps": 30, "frame_count": 0}
    
    def _sample_frames(self, file_path: Path) -> List:
        """
        Sample frames from video at 1 fps.
        
        Returns:
            List of frame arrays
        """
        try:
            import cv2
            import numpy as np
            
            cap = cv2.VideoCapture(str(file_path))
            fps = cap.get(cv2.CAP_PROP_FPS)
            
            frames = []
            frame_interval = int(fps) if fps > 0 else 30  # Frames per second
            
            current_frame = 0
            while len(frames) < self.max_frames:
                cap.set(cv2.CAP_PROP_POS_FRAMES, current_frame)
                ret, frame = cap.read()
                
                if not ret:
                    break
                
                # Resize and convert
                frame = cv2.resize(frame, self.target_size)
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame = frame / 255.0
                
                frames.append(frame)
                current_frame += frame_interval
            
            cap.release()
            return frames
        except Exception as e:
            print(f"Frame sampling failed: {e}")
            return []
    
    def _analyze_frame(self, frame) -> Dict:
        """
        Analyze a single frame.
        
        Returns:
            Dict with frame analysis scores
        """
        import numpy as np
        
        # Placeholder analysis
        return {
            "real_score": 0.7 + random.uniform(-0.2, 0.2),
            "fake_score": 0.3 + random.uniform(-0.2, 0.2)
        }
    
    def analyze(self, file_path: Path) -> Dict:
        """
        Analyze video for deepfake content.
        
        Args:
            file_path: Path to video file
            
        Returns:
            Dict with analysis results
        """
        video_info = self._get_video_info(file_path)
        frames = self._sample_frames(file_path)
        
        if not frames:
            # Return uncertain results on error
            return {
                "real_probability": 0.5,
                "deepfake_likelihood": 0.5,
                "frames_analyzed": 0,
                "duration_seconds": video_info.get("duration", 0)
            }
        
        # Analyze each frame
        frame_results = [self._analyze_frame(f) for f in frames]
        
        # Aggregate results (temporal pooling - mean for now)
        avg_real = sum(r["real_score"] for r in frame_results) / len(frame_results)
        avg_fake = sum(r["fake_score"] for r in frame_results) / len(frame_results)
        
        # Normalize
        total = avg_real + avg_fake
        
        return {
            "real_probability": avg_real / total,
            "deepfake_likelihood": avg_fake / total,
            "frames_analyzed": len(frames),
            "duration_seconds": video_info.get("duration", 0)
        }


# Singleton instance
_analyzer = None


def get_video_analyzer() -> VideoAnalyzer:
    """Get or create the video analyzer instance."""
    global _analyzer
    if _analyzer is None:
        _analyzer = VideoAnalyzer()
    return _analyzer
