"""
VentureLens AI - Analysis Models
"""

from django.db import models
from django.utils import timezone
from django.conf import settings
import uuid


class StartupAnalysis(models.Model):
    class Status(models.TextChoices):
        PENDING = 'pending', 'Pending'
        PROCESSING = 'processing', 'Processing'
        COMPLETED = 'completed', 'Completed'
        FAILED = 'failed', 'Failed'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='analyses',
        null=True, blank=True,
    )
    session_key = models.CharField(max_length=40, db_index=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    startup_idea = models.TextField()
    industry = models.CharField(max_length=100, blank=True)
    target_market = models.CharField(max_length=200, blank=True)

    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    processing_time_seconds = models.FloatField(null=True, blank=True)
    error_message = models.TextField(blank=True)
    feedback = models.CharField(max_length=10, blank=True, choices=[('up', 'Up'), ('down', 'Down')])
	
    problem_statement = models.TextField(blank=True)
    solution_summary = models.TextField(blank=True)
    target_market_analysis = models.TextField(blank=True)
    value_proposition = models.TextField(blank=True)
    scalability_analysis = models.TextField(blank=True)
    business_models = models.JSONField(default=list, blank=True)
    competitors = models.JSONField(default=list, blank=True)
    investor_perspective = models.TextField(blank=True)
    investor_verdict = models.CharField(max_length=20, blank=True)
    swot_strengths = models.JSONField(default=list, blank=True)
    swot_weaknesses = models.JSONField(default=list, blank=True)
    swot_opportunities = models.JSONField(default=list, blank=True)
    swot_threats = models.JSONField(default=list, blank=True)
    trend_data = models.JSONField(default=dict, blank=True)
    trend_keywords = models.JSONField(default=list, blank=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'created_at']),
            models.Index(fields=['status']),
        ]

    def __str__(self):
        return f"{self.startup_idea[:60]}... ({self.status})"

    @property
    def is_completed(self):
        return self.status == self.Status.COMPLETED

    @property
    def overall_score(self):
        try:
            return self.viability_score.overall_score
        except Exception:
            return None


class ViabilityScore(models.Model):
    analysis = models.OneToOneField(StartupAnalysis, on_delete=models.CASCADE, related_name='viability_score')
    market_demand = models.IntegerField(default=0)
    competition_level = models.IntegerField(default=0)
    scalability = models.IntegerField(default=0)
    innovation = models.IntegerField(default=0)
    monetization_potential = models.IntegerField(default=0)
    execution_complexity = models.IntegerField(default=0)
    market_timing = models.IntegerField(default=0)
    overall_score = models.IntegerField(default=0)
    score_rationale = models.TextField(blank=True)
    recommendation = models.TextField(blank=True)
    calculated_at = models.DateTimeField(auto_now_add=True)

    @property
    def score_label(self):
        if self.overall_score >= 80: return 'Exceptional'
        elif self.overall_score >= 65: return 'Strong'
        elif self.overall_score >= 50: return 'Promising'
        elif self.overall_score >= 35: return 'Needs Work'
        else: return 'High Risk'

    @property
    def score_color(self):
        if self.overall_score >= 80: return 'emerald'
        elif self.overall_score >= 65: return 'blue'
        elif self.overall_score >= 50: return 'yellow'
        elif self.overall_score >= 35: return 'orange'
        else: return 'red'

    def get_dimensions(self):
        return {
            'Market Demand': self.market_demand,
            'Competition': self.competition_level,
            'Scalability': self.scalability,
            'Innovation': self.innovation,
            'Monetization': self.monetization_potential,
            'Execution': self.execution_complexity,
            'Timing': self.market_timing,
        }
