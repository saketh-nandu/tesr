"""
Sentinel AI - Text Analysis Route
POST /analyze/text endpoint
"""
from fastapi import APIRouter, HTTPException

from app.schemas.responses import (
    TextAnalysisRequest,
    TextAnalysisResult,
    TextAnalysisDetails,
    ErrorResponse
)
from app.models.text_analyzer import get_text_analyzer
from app.utils.explainer import explain_text_analysis, get_verdict


router = APIRouter()


@router.post(
    "/text",
    response_model=TextAnalysisResult,
    responses={
        400: {"model": ErrorResponse},
        500: {"model": ErrorResponse}
    },
    summary="Analyze text for AI generation and scam intent",
    description="Analyzes text content to detect if it's AI-generated and check for scam/fraud indicators."
)
async def analyze_text(request: TextAnalysisRequest):
    """
    Analyze text content for:
    - AI-generated content
    - Scam/phishing intent
    - Urgency manipulation
    - Financial requests
    - Impersonation attempts
    """
    try:
        # Get analyzer
        analyzer = get_text_analyzer()
        
        # Run analysis
        scores = analyzer.analyze(request.text)
        
        # Generate explanations
        risk_score, explanations, action = explain_text_analysis(
            ai_likelihood=scores["ai_likelihood"],
            scam_intent=scores["scam_intent"],
            urgency=scores["urgency"],
            financial=scores["financial_request"],
            impersonation=scores["impersonation"]
        )
        
        # Build response
        return TextAnalysisResult(
            risk_score=risk_score,
            verdict=get_verdict(risk_score),
            explanations=explanations,
            action=action,
            content_type="text",
            details=TextAnalysisDetails(
                ai_likelihood=scores["ai_likelihood"],
                scam_intent=scores["scam_intent"],
                urgency_level=scores["urgency"],
                financial_request=scores["financial_request"],
                impersonation=scores["impersonation"]
            )
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Analysis failed: {str(e)}"
        )
