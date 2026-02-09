"""
Sentinel AI - Explanation Generator
Creates human-friendly, jargon-free explanations for analysis results.
Target audience: 6th grade reading level (non-technical users).
"""
from typing import List, Tuple
from app.schemas.responses import Verdict


def get_verdict(risk_score: int) -> Verdict:
    """
    Convert a risk score to a verdict.
    
    Args:
        risk_score: Score from 0-100
        
    Returns:
        Verdict enum value
    """
    if risk_score < 30:
        return Verdict.SAFE
    elif risk_score < 70:
        return Verdict.POSSIBLY_AI
    else:
        return Verdict.HIGH_RISK


# =============================================================================
# Text Explanations
# =============================================================================

TEXT_EXPLANATIONS = {
    "ai_generated": {
        "high": "This text looks like it was written by a computer, not a real person.",
        "medium": "Some parts of this text might have been written by AI.",
        "low": "This text appears to be written by a real person."
    },
    "scam_intent": {
        "high": "This message is trying to trick you into doing something risky.",
        "medium": "This message has some warning signs of a scam.",
        "low": "This message doesn't show obvious scam patterns."
    },
    "urgency": {
        "high": "The message is pushing you to act fast without thinking.",
        "medium": "There's some pressure to respond quickly.",
        "low": None
    },
    "financial": {
        "high": "This asks for money or financial information.",
        "medium": "This mentions money or payments.",
        "low": None
    },
    "impersonation": {
        "high": "This pretends to be from someone important (like a bank or government).",
        "medium": "This might be pretending to be from an official source.",
        "low": None
    }
}

TEXT_ACTIONS = {
    Verdict.SAFE: "This looks okay, but always be careful with personal information.",
    Verdict.POSSIBLY_AI: "Be careful! Don't click any links or share personal details.",
    Verdict.HIGH_RISK: "Don't respond to this message. Delete it and don't click anything."
}


def explain_text_analysis(
    ai_likelihood: float,
    scam_intent: float,
    urgency: float,
    financial: float,
    impersonation: float
) -> Tuple[int, List[str], str]:
    """
    Generate explanations for text analysis.
    
    Returns:
        Tuple of (risk_score, explanations, action)
    """
    explanations = []
    
    def get_level(score: float) -> str:
        if score > 0.7:
            return "high"
        elif score > 0.4:
            return "medium"
        return "low"
    
    def add_explanation(category: str, score: float):
        level = get_level(score)
        text = TEXT_EXPLANATIONS[category].get(level)
        if text:
            explanations.append(text)
    
    # Calculate risk score (weighted average)
    risk_score = int(
        scam_intent * 40 +
        ai_likelihood * 20 +
        urgency * 15 +
        financial * 15 +
        impersonation * 10
    )
    risk_score = min(100, max(0, risk_score))
    
    # Add relevant explanations (max 3)
    add_explanation("scam_intent", scam_intent)
    add_explanation("ai_generated", ai_likelihood)
    add_explanation("urgency", urgency)
    add_explanation("financial", financial)
    add_explanation("impersonation", impersonation)
    
    # Limit to 3 explanations
    explanations = explanations[:3]
    
    # Ensure at least one explanation
    if not explanations:
        explanations = ["This text looks safe based on our checks."]
    
    # Get action
    verdict = get_verdict(risk_score)
    action = TEXT_ACTIONS[verdict]
    
    return risk_score, explanations, action


# =============================================================================
# Audio Explanations
# =============================================================================

AUDIO_EXPLANATIONS = {
    "tts": {
        "high": "This voice sounds like it was made by a computer.",
        "medium": "This voice has some digital qualities.",
        "low": "This sounds like a real human voice."
    },
    "voice_cloning": {
        "high": "This voice might be copied from someone else's voice.",
        "medium": "There are signs this voice might be manipulated.",
        "low": None
    }
}

AUDIO_ACTIONS = {
    Verdict.SAFE: "This audio seems genuine, but stay alert for requests.",
    Verdict.POSSIBLY_AI: "Be careful! This voice might not be real. Verify the caller's identity.",
    Verdict.HIGH_RISK: "Don't trust this voice. Hang up and call the person directly."
}


def explain_audio_analysis(
    human_voice: float,
    tts_likelihood: float,
    voice_cloning: float
) -> Tuple[int, List[str], str]:
    """
    Generate explanations for audio analysis.
    
    Returns:
        Tuple of (risk_score, explanations, action)
    """
    explanations = []
    
    def get_level(score: float) -> str:
        if score > 0.7:
            return "high"
        elif score > 0.4:
            return "medium"
        return "low"
    
    # Calculate risk score
    fake_likelihood = max(tts_likelihood, voice_cloning)
    risk_score = int(fake_likelihood * 100)
    risk_score = min(100, max(0, risk_score))
    
    # Add explanations
    tts_level = get_level(tts_likelihood)
    if AUDIO_EXPLANATIONS["tts"].get(tts_level):
        explanations.append(AUDIO_EXPLANATIONS["tts"][tts_level])
    
    clone_level = get_level(voice_cloning)
    if AUDIO_EXPLANATIONS["voice_cloning"].get(clone_level):
        explanations.append(AUDIO_EXPLANATIONS["voice_cloning"][clone_level])
    
    # Ensure at least one explanation
    if not explanations:
        explanations = ["This audio sounds natural and authentic."]
    
    explanations = explanations[:3]
    
    # Get action
    verdict = get_verdict(risk_score)
    action = AUDIO_ACTIONS[verdict]
    
    return risk_score, explanations, action


# =============================================================================
# Image Explanations
# =============================================================================

IMAGE_EXPLANATIONS = {
    "ai_generated": {
        "high": "This image was likely created by AI, not a real camera.",
        "medium": "Parts of this image might be AI-generated.",
        "low": "This image appears to be from a real camera."
    },
    "manipulated": {
        "high": "This image has been edited or changed significantly.",
        "medium": "There are some signs this image was altered.",
        "low": None
    }
}

IMAGE_ACTIONS = {
    Verdict.SAFE: "This image looks authentic, but photos can still be misleading.",
    Verdict.POSSIBLY_AI: "Be cautious! This image might not be what it seems.",
    Verdict.HIGH_RISK: "Don't trust this image. It's likely fake or heavily edited."
}


def explain_image_analysis(
    real_probability: float,
    ai_generated: float,
    manipulated: float
) -> Tuple[int, List[str], str]:
    """
    Generate explanations for image analysis.
    
    Returns:
        Tuple of (risk_score, explanations, action)
    """
    explanations = []
    
    def get_level(score: float) -> str:
        if score > 0.7:
            return "high"
        elif score > 0.4:
            return "medium"
        return "low"
    
    # Calculate risk score
    fake_likelihood = max(ai_generated, manipulated)
    risk_score = int(fake_likelihood * 100)
    risk_score = min(100, max(0, risk_score))
    
    # Add explanations
    ai_level = get_level(ai_generated)
    if IMAGE_EXPLANATIONS["ai_generated"].get(ai_level):
        explanations.append(IMAGE_EXPLANATIONS["ai_generated"][ai_level])
    
    manip_level = get_level(manipulated)
    if IMAGE_EXPLANATIONS["manipulated"].get(manip_level):
        explanations.append(IMAGE_EXPLANATIONS["manipulated"][manip_level])
    
    if not explanations:
        explanations = ["This image looks like it's from a real camera."]
    
    explanations = explanations[:3]
    
    verdict = get_verdict(risk_score)
    action = IMAGE_ACTIONS[verdict]
    
    return risk_score, explanations, action


# =============================================================================
# Video Explanations
# =============================================================================

VIDEO_EXPLANATIONS = {
    "deepfake": {
        "high": "This video is likely a deepfake - the face or voice might be fake.",
        "medium": "Some parts of this video might be manipulated.",
        "low": "This video appears to be genuine."
    }
}

VIDEO_ACTIONS = {
    Verdict.SAFE: "This video seems real, but stay alert for misinformation.",
    Verdict.POSSIBLY_AI: "Be careful! Parts of this video might not be real.",
    Verdict.HIGH_RISK: "Don't trust this video. It's likely a deepfake."
}


def explain_video_analysis(
    real_probability: float,
    deepfake_likelihood: float
) -> Tuple[int, List[str], str]:
    """
    Generate explanations for video analysis.
    
    Returns:
        Tuple of (risk_score, explanations, action)
    """
    explanations = []
    
    def get_level(score: float) -> str:
        if score > 0.7:
            return "high"
        elif score > 0.4:
            return "medium"
        return "low"
    
    # Calculate risk score
    risk_score = int(deepfake_likelihood * 100)
    risk_score = min(100, max(0, risk_score))
    
    # Add explanations
    df_level = get_level(deepfake_likelihood)
    if VIDEO_EXPLANATIONS["deepfake"].get(df_level):
        explanations.append(VIDEO_EXPLANATIONS["deepfake"][df_level])
    
    if not explanations:
        explanations = ["This video looks authentic based on our analysis."]
    
    explanations = explanations[:3]
    
    verdict = get_verdict(risk_score)
    action = VIDEO_ACTIONS[verdict]
    
    return risk_score, explanations, action
