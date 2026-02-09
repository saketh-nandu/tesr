"""
Sentinel AI - Image Analysis Route
POST /analyze/image endpoint
"""
from fastapi import APIRouter, UploadFile, File, HTTPException, BackgroundTasks

from app.schemas.responses import ImageAnalysisResult, ImageAnalysisDetails, ErrorResponse
from app.models.image_analyzer import get_image_analyzer
from app.utils.file_handler import save_upload, delete_file
from app.utils.explainer import explain_image_analysis, get_verdict


router = APIRouter()


@router.post(
    "/image",
    response_model=ImageAnalysisResult,
    responses={
        400: {"model": ErrorResponse},
        413: {"model": ErrorResponse},
        500: {"model": ErrorResponse}
    },
    summary="Analyze image for AI generation or manipulation",
    description="Analyzes image content to detect if it's AI-generated or manipulated (deepfake)."
)
async def analyze_image(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(..., description="Image file (JPG, PNG)")
):
    """
    Analyze image content for:
    - Real/authentic image
    - AI-generated image
    - Manipulated/edited image
    """
    file_path = None
    
    try:
        # Save uploaded file
        file_path, file_id = await save_upload(file, "image")
        
        # Get analyzer
        analyzer = get_image_analyzer()
        
        # Run analysis
        result = analyzer.analyze(file_path)
        
        # Generate explanations
        risk_score, explanations, action = explain_image_analysis(
            real_probability=result["real_probability"],
            ai_generated=result["ai_generated"],
            manipulated=result["manipulated"]
        )
        
        # Schedule file cleanup
        background_tasks.add_task(delete_file, file_path)
        
        # Build response
        return ImageAnalysisResult(
            risk_score=risk_score,
            verdict=get_verdict(risk_score),
            explanations=explanations,
            action=action,
            content_type="image",
            details=ImageAnalysisDetails(
                real_probability=result["real_probability"],
                ai_generated=result["ai_generated"],
                manipulated=result["manipulated"]
            )
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
