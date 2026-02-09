"""
Sentinel AI - Audio Analysis Route
POST /analyze/audio endpoint
"""
from fastapi import APIRouter, UploadFile, File, HTTPException, BackgroundTasks

from app.schemas.responses import AudioAnalysisResult, AudioAnalysisDetails, ErrorResponse
from app.models.audio_analyzer import get_audio_analyzer
from app.utils.file_handler import save_upload, delete_file
from app.utils.explainer import explain_audio_analysis, get_verdict
from app.config import settings


router = APIRouter()


@router.post(
    "/audio",
    response_model=AudioAnalysisResult,
    responses={
        400: {"model": ErrorResponse},
        413: {"model": ErrorResponse},
        500: {"model": ErrorResponse}
    },
    summary="Analyze audio for voice spoofing",
    description="Analyzes audio content to detect TTS, voice cloning, or other voice spoofing."
)
async def analyze_audio(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(..., description="Audio file (MP3, WAV, ≤30 seconds)")
):
    """
    Analyze audio content for:
    - Real human voice
    - Text-to-speech (TTS)
    - Voice cloning/conversion
    - Spoofed audio
    """
    file_path = None
    
    try:
        # Save uploaded file
        file_path, file_id = await save_upload(file, "audio")
        
        # Get analyzer
        analyzer = get_audio_analyzer()
        
        # Run analysis
        result = analyzer.analyze(file_path)
        
        # Check duration limit
        if result["duration_seconds"] > settings.max_audio_duration_seconds:
            raise HTTPException(
                status_code=400,
                detail=f"Audio too long. Maximum duration: {settings.max_audio_duration_seconds} seconds"
            )
        
        # Generate explanations
        risk_score, explanations, action = explain_audio_analysis(
            human_voice=result["human_voice"],
            tts_likelihood=result["tts_likelihood"],
            voice_cloning=result["voice_cloning"]
        )
        
        # Schedule file cleanup
        background_tasks.add_task(delete_file, file_path)
        
        # Build response
        return AudioAnalysisResult(
            risk_score=risk_score,
            verdict=get_verdict(risk_score),
            explanations=explanations,
            action=action,
            content_type="audio",
            details=AudioAnalysisDetails(
                human_voice=result["human_voice"],
                tts_likelihood=result["tts_likelihood"],
                voice_cloning=result["voice_cloning"]
            ),
            duration_seconds=result["duration_seconds"]
        )
        
    except HTTPException:
        # Re-raise HTTP exceptions
        if file_path:
            delete_file(file_path)
        raise
    except Exception as e:
        # Clean up on error
        if file_path:
            delete_file(file_path)
        raise HTTPException(
            status_code=500,
            detail=f"Analysis failed: {str(e)}"
        )
