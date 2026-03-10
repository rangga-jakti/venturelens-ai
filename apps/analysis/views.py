"""
VentureLens AI - Analysis Views
"""

import logging
import threading
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views import View
from django.views.generic import FormView
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

from .forms import StartupIdeaForm
from .models import StartupAnalysis
from .services.analysis_orchestrator import orchestrator
from .services.ai_service import AIServiceError

logger = logging.getLogger(__name__)


def run_analysis_in_background(analysis, user):
    """
    Run analysis in a background thread so the user sees the processing page.
    Django's ORM is thread-safe for reads/writes, so this is fine for development.
    """
    try:
        orchestrator.run(analysis)
        user.increment_analysis_count()
    except (AIServiceError, Exception) as e:
        logger.error(f"Background analysis failed: {e}")


class IdeaInputView(LoginRequiredMixin, FormView):
    """Startup idea input — requires login."""
    template_name = 'analysis/input.html'
    form_class = StartupIdeaForm
    login_url = '/accounts/login/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['analysis_features'] = [
            'Viability Score', 'Market Trends',
            'Competitor Intel', 'SWOT Analysis',
            'Business Models', 'Investor View',
        ]
        return context

    def form_valid(self, form):
        user = self.request.user

        # Rate limiting per user
        max_allowed = getattr(settings, 'MAX_ANALYSES_PER_DAY', 10)
        if not user.can_analyze(max_allowed):
            messages.error(
                self.request,
                f'Daily limit of {max_allowed} analyses reached. Resets at midnight UTC.'
            )
            return self.form_invalid(form)

        # Create analysis with PENDING status
        analysis = StartupAnalysis.objects.create(
            user=user,
            startup_idea=form.cleaned_data['startup_idea'],
            status=StartupAnalysis.Status.PENDING,
        )

        # ── Fire analysis in background thread ────────────────────────────
        # This lets Django immediately redirect to the processing page
        # while the orchestrator runs in the background.
        thread = threading.Thread(
            target=run_analysis_in_background,
            args=(analysis, user),
            daemon=True,  # thread dies if server shuts down
        )
        thread.start()

        # Redirect immediately to processing page — don't wait for analysis
        return redirect('analysis:processing', pk=analysis.pk)

    def form_invalid(self, form):
        return render(self.request, self.template_name, self.get_context_data(form=form))


class AnalysisProcessingView(LoginRequiredMixin, View):
    """Show the cinematic processing page while analysis runs in background."""
    login_url = '/accounts/login/'

    def get(self, request, pk):
        analysis = get_object_or_404(StartupAnalysis, pk=pk, user=request.user)

        # If already done (e.g. user refreshes), redirect straight to results
        if analysis.status == StartupAnalysis.Status.COMPLETED:
            return redirect('dashboard:results', pk=pk)
        if analysis.status == StartupAnalysis.Status.FAILED:
            return redirect('dashboard:results', pk=pk)

        return render(request, 'dashboard/processing.html', {'analysis': analysis})


class AnalysisStatusView(View):
    """Polling endpoint — called by processing page every 3 seconds."""
    def get(self, request, pk):
        analysis = get_object_or_404(StartupAnalysis, pk=pk)
        if analysis.status == StartupAnalysis.Status.COMPLETED:
            return JsonResponse({'status': 'completed'})
        elif analysis.status == StartupAnalysis.Status.FAILED:
            return JsonResponse({'status': 'failed', 'error': analysis.error_message})
        return JsonResponse({'status': str(analysis.status)})


class TrendsTimeframeView(LoginRequiredMixin, View):
    """AJAX endpoint — returns fresh trend data for a given timeframe."""
    login_url = '/accounts/login/'

    def get(self, request, pk):
        analysis = get_object_or_404(StartupAnalysis, pk=pk, user=request.user)
        timeframe_key = request.GET.get('tf', '12M')

        from .services.trends_service import trends_service
        keywords = analysis.trend_keywords or [analysis.startup_idea[:50]]
        data = trends_service.fetch_trends(keywords[:3], timeframe_key=timeframe_key)

        return JsonResponse(data)