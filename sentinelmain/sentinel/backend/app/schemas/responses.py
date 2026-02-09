"""
Sentinel AI - Response Schemas
Pydantic models for API responses.
"""
from pydantic import BaseModel, Field
from typing import List, Literal
from enum import Enum


class Verdict(str, Enum):
    """Possible verdicts for content analysis."""
    SAFE = "Safe"
    POSSIBLY_AI = "Possibly AI"
    HIGH_RISK = "High Risk"


class AnalysisResult(BaseModel):
    """Standard analysis result returned by all endpoints."""
    
    risk_score: int = Field(
        ..., 
        ge=0, 
        le=100, 
        description="Risk score from 0 (safe) to 100 (high risk)"
    )
    verdict: Verdict = Field(
        ..., 
        description="Human-readable verdict"
    )
    explanations: List[str] = Field(
        ..., 
        min_length=1,
        max_length=3,
        description="2-3 simple explanations for the verdict"
    )
    action: str = Field(
        ..., 
        description="Single clear action recommendation"
    )
    content_type: Literal["text", "audio", "image", "video"] = Field(
        ..., 
        description="Type of content analyzed"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "risk_score": 75,
                "verdict": "Possibly AI",
                "explanations": [
                    "The text uses urgent language asking for immediate action",
                    "Contains requests for personal financial information",
                    "Writing style appears computer-generated"
                ],
                "action": "Do not click any links or share personal information",
                "content_type": "text"
            }
        }


class TextAnalysisRequest(BaseModel):
    """Request body for text analysis."""
    text: str = Field(
        ..., 
        min_length=1, 
        max_length=10000,
        description="Text content to analyze"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "text": "Congratulations! You've won $1,000,000. Click here to claim your prize now!"
            }
        }


class TextAnalysisDetails(BaseModel):
    """Detailed classification results for text analysis."""
    ai_likelihood: float = Field(..., ge=0, le=1, description="Probability text is AI-generated")
    scam_intent: float = Field(..., ge=0, le=1, description="Probability of scam intent")
    urgency_level: float = Field(..., ge=0, le=1, description="Level of artificial urgency")
    financial_request: float = Field(..., ge=0, le=1, description="Presence of financial requests")
    impersonation: float = Field(..., ge=0, le=1, description="Signs of impersonation")


class TextAnalysisResult(AnalysisResult):
    """Extended result for text analysis with detailed scores."""
    details: TextAnalysisDetails


class AudioAnalysisDetails(BaseModel):
    """Detailed classification results for audio analysis."""
    human_voice: float = Field(..., ge=0, le=1, description="Probability of real human voice")
    tts_likelihood: float = Field(..., ge=0, le=1, description="Probability of text-to-speech")
    voice_cloning: float = Field(..., ge=0, le=1, description="Probability of voice cloning")


class AudioAnalysisResult(AnalysisResult):
    """Extended result for audio analysis with detailed scores."""
    details: AudioAnalysisDetails
    duration_seconds: float = Field(..., description="Duration of analyzed audio")


class ImageAnalysisDetails(BaseModel):
    """Detailed classification results for image analysis."""
    real_probability: float = Field(..., ge=0, le=1, description="Probability image is authentic")
    ai_generated: float = Field(..., ge=0, le=1, description="Probability image is AI-generated")
    manipulated: float = Field(..., ge=0, le=1, description="Probability image is manipulated")


class ImageAnalysisResult(AnalysisResult):
    """Extended result for image analysis with detailed scores."""
    details: ImageAnalysisDetails


class VideoAnalysisDetails(BaseModel):
    """Detailed classification results for video analysis."""
    real_probability: float = Field(..., ge=0, le=1, description="Probability video is authentic")
    deepfake_likelihood: float = Field(..., ge=0, le=1, description="Probability of deepfake")
    frames_analyzed: int = Field(..., description="Number of frames analyzed")


class VideoAnalysisResult(AnalysisResult):
    """Extended result for video analysis with detailed scores."""
    details: VideoAnalysisDetails
    duration_seconds: float = Field(..., description="Duration of analyzed video")


class ErrorResponse(BaseModel):
    """Error response model."""
    error: str = Field(..., description="Error message")
    detail: str = Field(None, description="Additional error details")
