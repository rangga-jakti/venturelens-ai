"""
VentureLens AI - Core Views
Landing page, about, and general pages.
"""

from django.shortcuts import render
from django.views.generic import TemplateView


class LandingView(TemplateView):
    """Premium landing page with hero section and feature highlights."""
    template_name = 'core/landing.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['features'] = [
            {
                'icon': 'brain',
                'title': 'AI-Powered Analysis',
                'description': 'Deep LLM analysis of your startup idea across 7 critical dimensions.',
            },
            {
                'icon': 'chart-bar',
                'title': 'Viability Score',
                'description': 'Proprietary 0–100 scoring engine measuring market readiness.',
            },
            {
                'icon': 'trending-up',
                'title': 'Market Trends',
                'description': 'Real-time Google Trends data visualized with beautiful charts.',
            },
            {
                'icon': 'users',
                'title': 'Competitor Intel',
                'description': 'AI identifies key competitors and market landscape.',
            },
            {
                'icon': 'dollar-sign',
                'title': 'Business Models',
                'description': 'Tailored monetization strategies for your specific idea.',
            },
            {
                'icon': 'shield',
                'title': 'SWOT Analysis',
                'description': 'Comprehensive strengths, weaknesses, opportunities, and threats.',
            },
        ]
        return context
