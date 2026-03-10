"""
VentureLens AI - Analysis Orchestrator
Coordinates all analysis services into a complete startup analysis.
This is the main entry point for the analysis pipeline.
"""

import logging
import time
from django.db import transaction

from .ai_service import ai_service, AIServiceError, detect_language
from .scoring_service import scoring_service
from .trends_service import trends_service
from ..models import StartupAnalysis, ViabilityScore

logger = logging.getLogger(__name__)


class AnalysisOrchestrator:
    """
    Orchestrates the full analysis pipeline:
    1. Core AI analysis (problem, market, value prop)
    2. AI scoring (7 dimensions)
    3. Viability score computation
    4. Competitor detection
    5. Business model generation
    6. Investor perspective
    7. SWOT analysis
    8. Google Trends data
    """

    def run(self, analysis: StartupAnalysis) -> StartupAnalysis:
        """
        Execute the full analysis pipeline for a StartupAnalysis instance.
        Updates the instance in-place and saves to DB.

        Args:
            analysis: StartupAnalysis with status=PENDING

        Returns:
            Updated StartupAnalysis with status=COMPLETED or FAILED
        """
        start_time = time.time()

        try:
            # Mark as processing
            analysis.status = StartupAnalysis.Status.PROCESSING
            analysis.save(update_fields=['status'])

            startup_idea = analysis.startup_idea

            # ── Detect language once ───────────────────────────────────────
            lang = detect_language(startup_idea)
            logger.info(f"[{analysis.id}] Detected language: {lang}")

            # ── Step 1: Core Analysis ──────────────────────────────────────
            logger.info(f"[{analysis.id}] Step 1: Core analysis")
            core = ai_service.analyze_core(startup_idea, lang=lang)

            analysis.industry = core.get('industry', '')
            analysis.target_market = core.get('target_market', '')
            analysis.problem_statement = core.get('problem_statement', '')
            analysis.solution_summary = core.get('solution_summary', '')
            analysis.target_market_analysis = core.get('target_market_analysis', '')
            analysis.value_proposition = core.get('value_proposition', '')
            analysis.scalability_analysis = core.get('scalability_analysis', '')
            analysis.trend_keywords = core.get('trend_keywords', [startup_idea[:50]])

            # ── Step 2: AI Scoring ─────────────────────────────────────────
            logger.info(f"[{analysis.id}] Step 2: Scoring")
            ai_scores = ai_service.calculate_scores(startup_idea, core, lang=lang)

            # ── Step 3: Viability Score ────────────────────────────────────
            score_data = scoring_service.build_score_object(analysis, ai_scores)
            overall_score = score_data['overall_score']

            # ── Step 4: Competitors ────────────────────────────────────────
            logger.info(f"[{analysis.id}] Step 4: Competitors")
            analysis.competitors = ai_service.analyze_competitors(
                startup_idea, analysis.industry, lang=lang
            )

            # ── Step 5: Business Models ────────────────────────────────────
            logger.info(f"[{analysis.id}] Step 5: Business models")
            analysis.business_models = ai_service.generate_business_models(
                startup_idea, analysis.target_market, lang=lang
            )

            # ── Step 6: Investor Perspective ───────────────────────────────
            logger.info(f"[{analysis.id}] Step 6: Investor perspective")
            investor = ai_service.analyze_investor_perspective(startup_idea, overall_score, lang=lang)
            analysis.investor_perspective = investor.get('perspective', '')
            analysis.investor_verdict = investor.get('verdict', 'neutral')

            # Attach extra investor data to business models context
            analysis.business_models = analysis.business_models or []

            # ── Step 7: SWOT Analysis ──────────────────────────────────────
            logger.info(f"[{analysis.id}] Step 7: SWOT")
            swot = ai_service.generate_swot(startup_idea, analysis.industry, lang=lang)
            analysis.swot_strengths = swot.get('strengths', [])
            analysis.swot_weaknesses = swot.get('weaknesses', [])
            analysis.swot_opportunities = swot.get('opportunities', [])
            analysis.swot_threats = swot.get('threats', [])

            # ── Step 8: Google Trends ──────────────────────────────────────
            logger.info(f"[{analysis.id}] Step 8: Trends")
            keywords = analysis.trend_keywords or [startup_idea[:50]]
            analysis.trend_data = trends_service.fetch_trends(keywords[:3])

            # ── Save everything atomically ─────────────────────────────────
            with transaction.atomic():
                analysis.status = StartupAnalysis.Status.COMPLETED
                analysis.processing_time_seconds = time.time() - start_time
                analysis.save()

                # Save viability score
                ViabilityScore.objects.update_or_create(
                    analysis=analysis,
                    defaults={k: v for k, v in score_data.items() if k != 'analysis'}
                )

            logger.info(f"[{analysis.id}] Analysis complete in {analysis.processing_time_seconds:.1f}s")
            return analysis

        except AIServiceError as e:
            logger.error(f"[{analysis.id}] AI service error: {e}")
            analysis.status = StartupAnalysis.Status.FAILED
            analysis.error_message = str(e)
            analysis.processing_time_seconds = time.time() - start_time
            analysis.save(update_fields=['status', 'error_message', 'processing_time_seconds'])
            raise

        except Exception as e:
            logger.exception(f"[{analysis.id}] Unexpected error: {e}")
            analysis.status = StartupAnalysis.Status.FAILED
            analysis.error_message = f"Unexpected error: {str(e)}"
            analysis.processing_time_seconds = time.time() - start_time
            analysis.save(update_fields=['status', 'error_message', 'processing_time_seconds'])
            raise


orchestrator = AnalysisOrchestrator()
