"""
VentureLens AI - Admin Configuration
"""

from django.contrib import admin
from .models import StartupAnalysis, ViabilityScore


class ViabilityScoreInline(admin.StackedInline):
    model = ViabilityScore
    readonly_fields = ['overall_score', 'calculated_at']
    extra = 0


@admin.register(StartupAnalysis)
class StartupAnalysisAdmin(admin.ModelAdmin):
    list_display = ['truncated_idea', 'industry', 'status', 'get_score', 'created_at', 'processing_time_seconds']
    list_filter = ['status', 'industry', 'created_at']
    search_fields = ['startup_idea', 'industry']
    readonly_fields = ['id', 'created_at', 'updated_at', 'processing_time_seconds']
    inlines = [ViabilityScoreInline]

    def truncated_idea(self, obj):
        return obj.startup_idea[:80] + '...' if len(obj.startup_idea) > 80 else obj.startup_idea
    truncated_idea.short_description = 'Idea'

    def get_score(self, obj):
        return obj.overall_score or '—'
    get_score.short_description = 'Score'


@admin.register(ViabilityScore)
class ViabilityScoreAdmin(admin.ModelAdmin):
    list_display = ['analysis', 'overall_score', 'score_label', 'calculated_at']
    readonly_fields = ['calculated_at']
