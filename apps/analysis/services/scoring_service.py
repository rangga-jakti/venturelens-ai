"""
VentureLens AI - Scoring Service
Computes the final viability score from AI dimension scores.
Uses weighted average with business-logic adjustments.
"""

import logging

logger = logging.getLogger(__name__)

# Dimension weights (must sum to 1.0)
SCORE_WEIGHTS = {
    'market_demand': 0.22,
    'competition_level': 0.15,
    'scalability': 0.18,
    'innovation': 0.15,
    'monetization_potential': 0.15,
    'execution_complexity': 0.08,
    'market_timing': 0.07,
}


class ScoringService:
    """
    Computes the VentureLens Viability Score (VVS).
    
    The VVS is a weighted composite of 7 dimensions,
    each scored 0–100 by the AI service.
    """

    def compute_overall_score(self, dimension_scores: dict) -> int:
        """
        Compute weighted overall score from dimension scores.
        
        Args:
            dimension_scores: Dict of dimension_name -> score (0-100)
        
        Returns:
            Integer overall score 0-100
        """
        weighted_sum = 0.0
        total_weight = 0.0

        for dimension, weight in SCORE_WEIGHTS.items():
            score = dimension_scores.get(dimension, 50)
            # Clamp to 0-100
            score = max(0, min(100, int(score)))
            weighted_sum += score * weight
            total_weight += weight

        if total_weight == 0:
            return 50

        overall = round(weighted_sum / total_weight)
        return max(0, min(100, overall))

    def build_score_object(self, analysis, ai_scores: dict) -> dict:
        """
        Build the complete score object ready for database storage.
        
        Args:
            analysis: StartupAnalysis instance
            ai_scores: Raw scores from AI service
        
        Returns:
            Dict ready to create ViabilityScore model
        """
        overall = self.compute_overall_score(ai_scores)

        return {
            'analysis': analysis,
            'market_demand': max(0, min(100, int(ai_scores.get('market_demand', 50)))),
            'competition_level': max(0, min(100, int(ai_scores.get('competition_level', 50)))),
            'scalability': max(0, min(100, int(ai_scores.get('scalability', 50)))),
            'innovation': max(0, min(100, int(ai_scores.get('innovation', 50)))),
            'monetization_potential': max(0, min(100, int(ai_scores.get('monetization_potential', 50)))),
            'execution_complexity': max(0, min(100, int(ai_scores.get('execution_complexity', 50)))),
            'market_timing': max(0, min(100, int(ai_scores.get('market_timing', 50)))),
            'overall_score': overall,
            'score_rationale': ai_scores.get('rationale', ''),
            'recommendation': ai_scores.get('recommendation', ''),
        }


scoring_service = ScoringService()
