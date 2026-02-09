"""
Sentinel AI - Video Analysis Route
POST /analyze/video endpoint
"""
from fastapi import APIRouter, UploadFile, File, HTTPException, BackgroundTasks

from app.schemas.responses import VideoAnalysisResult, VideoAnalysisDetails, ErrorResponse
from app.models.video_analyzer import get_video_analyzer
from app.utils.file_handler import save_upload, delete_file
from app.utils.explainer import explain_video_analysis, get_verdict
from app.config import settings


router = APIRouter()


@router.post(
    "/video",
    response_model=VideoAnalysisResult,
    responses={
        400: {"model": ErrorResponse},
        413: {"model": ErrorResponse},
        500: {"model": ErrorResponse}
    },
    summary="Analyze video for deepfake content",
    description="Analyzes video content to detect deepfakes by sampling frames and analyzing temporal patterns."
)
async def analyze_video(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(..., description="Video file (MP4, MOV, ≤8 seconds)")
):
    """
    Analyze video content for:
    - Real/authentic video
    - Deepfake detection
    - Frame-by-frame analysis
    """
    file_path = None
    
    try:
        # Save uploaded file
        file_path, file_id = await save_upload(file, "video")
        
        # Get analyzer
        analyzer = get_video_analyzer()
        
        # Run analysis
        result = analyzer.analyze(file_path)
        
        # Check duration limit
        if result["duration_seconds"] > settings.max_video_duration_seconds:
            raise HTTPException(
                status_code=400,
                detail=f"Video too long. Maximum duration: {settings.max_video_duration_seconds} seconds"
            )
        
        # Generate explanations
        risk_score, explanations, action = explain_video_analysis(
            real_probability=result["real_probability"],
            deepfake_likelihood=result["deepfake_likelihood"]
        )
        
        # Schedule file cleanup
        background_tasks.add_task(delete_file, file_path)
        
        # Build response
        return VideoAnalysisResult(
            risk_score=risk_score,
            verdict=get_verdict(risk_score),
            explanations=explanations,
            action=action,
            content_type="video",
            details=VideoAnalysisDetails(
                real_probability=result["real_probability"],
                deepfake_likelihood=result["deepfake_likelihood"],
                frames_analyzed=result["frames_analyzed"]
            ),
            duration_seconds=result["duration_seconds"]
        )
        
    except HTTPException:
        if file_path:
            delete_file(file_path)
        raise
    except Exception as e:
        if file_path:
            delete_file(file_path)
        raise HTTPException(
            status_code=500,
            detail=f"Analysis failed: {str(e)}"
        )
