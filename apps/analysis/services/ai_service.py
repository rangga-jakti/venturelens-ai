"""
VentureLens AI - AI Service
LLM integration layer supporting Groq and OpenAI.
Clean interface for all AI-powered analysis tasks.
"""

import json
import logging
from typing import Any
from django.conf import settings

logger = logging.getLogger(__name__)


def detect_language(text: str) -> str:
    """
    Detect language of the input text.
    Returns 'id' for Indonesian, 'en' for everything else.
    Falls back to 'en' if detection fails.
    """
    try:
        from langdetect import detect
        lang = detect(text)
        return 'id' if lang == 'id' else 'en'
    except Exception:
        return 'en'


def get_language_instruction(lang: str) -> str:
    """Return language instruction to inject into AI prompts."""
    if lang == 'id':
        return (
            "\n\nIMPORTANT LANGUAGE RULE: The user wrote in Bahasa Indonesia. "
            "You MUST respond with all text values in Bahasa Indonesia. "
            "Only keep these fields in English: field names/keys, "
            "technical terms like 'pre-seed/seed/Series A', verdict values like "
            "'likely/neutral/unlikely', revenue_potential values like "
            "'low/medium/high/very-high', and implementation_difficulty values. "
            "All descriptive text, analysis, and explanations must be in Bahasa Indonesia."
        )
    return ""


class AIServiceError(Exception):
    """Raised when AI API call fails."""
    pass


class AIService:
    """
    Unified AI service supporting Groq (primary) and OpenAI (fallback).
    Uses structured prompts to extract analysis data as JSON.
    """

    def __init__(self):
        self.provider = getattr(settings, 'LLM_PROVIDER', 'groq')
        self._client = None

    def _get_client(self):
        """Lazy-initialize the LLM client."""
        if self._client is not None:
            return self._client

        if self.provider == 'groq':
            try:
                from groq import Groq
                self._client = Groq(api_key=settings.GROQ_API_KEY)
                return self._client
            except ImportError:
                logger.warning("Groq not installed, falling back to OpenAI")
                self.provider = 'openai'

        # OpenAI fallback
        from openai import OpenAI
        self._client = OpenAI(api_key=settings.OPENAI_API_KEY)
        return self._client

    def _get_model(self) -> str:
        if self.provider == 'groq':
            return getattr(settings, 'GROQ_MODEL', 'llama-3.3-70b-versatile')
        return getattr(settings, 'OPENAI_MODEL', 'gpt-4o-mini')

    def _chat(self, system_prompt: str, user_prompt: str, max_tokens: int = 2000) -> str:
        """Core chat completion call."""
        client = self._get_client()
        model = self._get_model()

        try:
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                max_tokens=max_tokens,
                temperature=0.7,
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"AI API error: {e}")
            raise AIServiceError(f"AI service unavailable: {str(e)}")

    def _chat_json(self, system_prompt: str, user_prompt: str, max_tokens: int = 3000) -> dict:
        """Chat that expects JSON response."""
        system = system_prompt + "\n\nIMPORTANT: Respond ONLY with valid JSON. No markdown, no explanation, just the JSON object."
        raw = self._chat(system, user_prompt, max_tokens)

        # Strip possible markdown code fences
        raw = raw.strip()
        if raw.startswith("```"):
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]
        raw = raw.strip()

        try:
            return json.loads(raw)
        except json.JSONDecodeError as e:
            logger.error(f"JSON parse error: {e}\nRaw: {raw[:500]}")
            # Try to repair truncated JSON
            try:
                import re
                # Find last complete key-value and close the JSON
                fixed = raw
                if not fixed.endswith('}'):
                    # Remove last incomplete field and close
                    fixed = re.sub(r',?\s*"[^"]*"\s*:\s*[^,}]*$', '', fixed)
                    fixed = fixed.rstrip(',') + '}'
                return json.loads(fixed)
            except Exception:
                raise AIServiceError(f"Invalid JSON from AI: {e}")

    # ─── Analysis Methods ──────────────────────────────────────────────────────

    def analyze_core(self, startup_idea: str, lang: str = 'en') -> dict[str, Any]:
        """
        Core startup analysis: problem, solution, market, value prop, scalability.
        Returns structured JSON.
        """
        lang_instruction = get_language_instruction(lang)

        system = """You are a senior startup analyst and venture capitalist with 20+ years of experience.
Analyze startup ideas with depth, nuance, and actionable insights.
Be specific, honest, and constructive. Avoid generic advice.""" + lang_instruction

        prompt = f"""Analyze this startup idea and return a JSON object with these exact keys:

Startup idea: "{startup_idea}"

Return JSON with:
{{
  "industry": "detected industry/sector (1-3 words)",
  "target_market": "specific target audience",
  "problem_statement": "problem in 1-2 sentences (max 40 words)",
  "solution_summary": "solution in 1-2 sentences (max 40 words)",
  "target_market_analysis": "market analysis (max 60 words)",
  "value_proposition": "unique value (max 50 words)",
  "scalability_analysis": "scaling potential (max 50 words)",
  "trend_keywords": ["keyword1", "keyword2", "keyword3"]
}}"""

        return self._chat_json(system, prompt, max_tokens=4000)

    def analyze_competitors(self, startup_idea: str, industry: str, lang: str = 'en') -> list[dict]:
        """
        Identify real and potential competitors in the market.
        Returns list of competitor objects.
        """
        system = "You are a competitive intelligence expert. Identify real companies and potential competitors." + get_language_instruction(lang)

        prompt = f"""For this startup idea, identify 5-7 key competitors (existing companies or close analogies).

Startup: "{startup_idea}"
Industry: "{industry}"

Return JSON array:
[
  {{
    "name": "Company Name",
    "description": "1-2 sentence description of what they do",
    "similarity": "how they compete with this idea (direct/indirect)",
    "strength": "their main competitive advantage",
    "weakness": "their main gap or weakness",
    "stage": "startup/growth/public"
  }}
]"""

        result = self._chat_json(system, prompt, max_tokens=2000)
        return result if isinstance(result, list) else result.get('competitors', [])

    def generate_business_models(self, startup_idea: str, target_market: str, lang: str = 'en') -> list[dict]:
        """Generate monetization strategies."""
        system = "You are a business model expert and revenue strategy consultant." + get_language_instruction(lang)

        prompt = f"""Suggest 5 monetization strategies for this startup.

Startup: "{startup_idea}"
Target market: "{target_market}"

Return JSON array:
[
  {{
    "model": "Model name (e.g., SaaS Subscription)",
    "description": "How this monetization works (2 sentences)",
    "revenue_potential": "low/medium/high/very-high",
    "implementation_difficulty": "easy/moderate/complex",
    "example": "Real company using this model"
  }}
]"""

        result = self._chat_json(system, prompt, max_tokens=1000)
        return result if isinstance(result, list) else result.get('models', [])

    def analyze_investor_perspective(self, startup_idea: str, score: int, lang: str = 'en') -> dict:
        """Evaluate from an investor's perspective."""
        system = "You are a venture capitalist evaluating startup investments. Be honest and direct." + get_language_instruction(lang)

        prompt = f"""Evaluate this startup idea from an investor's perspective.

Startup: "{startup_idea}"
Viability Score: {score}/100

Return JSON:
{{
  "verdict": "likely|neutral|unlikely",
  "perspective": "3-4 sentence investor evaluation (honest, direct)",
  "funding_stage": "pre-seed/seed/Series A (most appropriate)",
  "key_concern": "single biggest investor concern",
  "key_opportunity": "single biggest investment opportunity",
  "comparable_investments": ["Company1", "Company2"]
}}"""

        return self._chat_json(system, prompt, max_tokens=800)

    def generate_swot(self, startup_idea: str, industry: str, lang: str = 'en') -> dict:
        """Generate SWOT analysis."""
        system = "You are a strategic business analyst specializing in startup evaluation." + get_language_instruction(lang)

        prompt = f"""Generate a comprehensive SWOT analysis for this startup.

Startup: "{startup_idea}"
Industry: "{industry}"

Return JSON:
{{
  "strengths": ["strength 1", "strength 2", "strength 3", "strength 4"],
  "weaknesses": ["weakness 1", "weakness 2", "weakness 3", "weakness 4"],
  "opportunities": ["opportunity 1", "opportunity 2", "opportunity 3", "opportunity 4"],
  "threats": ["threat 1", "threat 2", "threat 3", "threat 4"]
}}"""

        return self._chat_json(system, prompt, max_tokens=800)

    def calculate_scores(self, startup_idea: str, core_analysis: dict, lang: str = 'en') -> dict:
        """
        AI-driven viability scoring across 7 dimensions.
        Returns scores 0-100 per dimension.
        """
        system = "You are a quantitative startup analyst. Score startups objectively based on evidence." + get_language_instruction(lang)

        prompt = f"""Score this startup across 7 dimensions (0-100 each).

Startup: "{startup_idea}"
Industry: {core_analysis.get('industry', 'unknown')}
Market: {core_analysis.get('target_market', 'unknown')}

Scoring criteria:
- market_demand: Size and urgency of the problem (0=no market, 100=massive urgent need)
- competition_level: Market openness (0=saturated, 100=blue ocean)
- scalability: Growth potential (0=local only, 100=global scale)
- innovation: Novelty and differentiation (0=copycat, 100=revolutionary)
- monetization_potential: Revenue clarity (0=unclear, 100=multiple clear streams)
- execution_complexity: Ease of building (0=impossible, 100=simple to execute)
- market_timing: Is now the right time? (0=too early/late, 100=perfect timing)

Return JSON:
{{
  "market_demand": 72,
  "competition_level": 58,
  "scalability": 85,
  "innovation": 67,
  "monetization_potential": 76,
  "execution_complexity": 61,
  "market_timing": 80,
  "rationale": "2-3 sentence explanation of the overall scores",
  "recommendation": "Actionable next step for the founder (2-3 sentences)"
}}"""

        return self._chat_json(system, prompt, max_tokens=600)


# Singleton instance
ai_service = AIService()
