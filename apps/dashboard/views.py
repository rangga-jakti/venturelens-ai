"""
VentureLens AI - Dashboard Views
"""

import json
import logging
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from apps.analysis.models import StartupAnalysis

logger = logging.getLogger(__name__)


class ResultsDashboardView(LoginRequiredMixin, DetailView):
    model = StartupAnalysis
    template_name = 'dashboard/results.html'
    context_object_name = 'analysis'
    login_url = '/accounts/login/'

    def get_queryset(self):
        # Users can only see their own analyses
        return StartupAnalysis.objects.filter(user=self.request.user)

    def get(self, request, *args, **kwargs):
        analysis = self.get_object()
        if analysis.status in [StartupAnalysis.Status.PENDING, StartupAnalysis.Status.PROCESSING]:
            return redirect('dashboard:processing', pk=analysis.pk)
        if analysis.status == StartupAnalysis.Status.FAILED:
            return render(request, 'dashboard/failed.html', {'analysis': analysis})
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        analysis = self.object
        try:
            score = analysis.viability_score
            context['score'] = score
            context['score_dimensions_json'] = json.dumps(score.get_dimensions())
        except Exception:
            context['score'] = None
            context['score_dimensions_json'] = '{}'

        context['trend_data_json'] = json.dumps(analysis.trend_data or {})
        verdict_styles = {
            'likely': {'color': 'emerald', 'label': 'Likely to Fund'},
            'neutral': {'color': 'yellow', 'label': 'Neutral'},
            'unlikely': {'color': 'red', 'label': 'Unlikely to Fund'},
        }
        context['investor_style'] = verdict_styles.get(analysis.investor_verdict, verdict_styles['neutral'])
        context['swot'] = {
            'strengths': analysis.swot_strengths,
            'weaknesses': analysis.swot_weaknesses,
            'opportunities': analysis.swot_opportunities,
            'threats': analysis.swot_threats,
        }
        return context


class ProcessingView(LoginRequiredMixin, DetailView):
    model = StartupAnalysis
    template_name = 'dashboard/processing.html'
    context_object_name = 'analysis'
    login_url = '/accounts/login/'

    def get_queryset(self):
        return StartupAnalysis.objects.filter(user=self.request.user)


@method_decorator(login_required(login_url='/accounts/login/'), name='dispatch')
class HistoryView(DetailView):
    template_name = 'dashboard/history.html'

    def get(self, request, *args, **kwargs):
        analyses = StartupAnalysis.objects.filter(
            user=request.user,
            status=StartupAnalysis.Status.COMPLETED
        ).select_related('viability_score').order_by('-created_at')[:20]
        return render(request, self.template_name, {'analyses': analyses})

class DeleteAnalysisView(LoginRequiredMixin, View):
    login_url = '/accounts/login/'

    def post(self, request, pk):
        analysis = get_object_or_404(StartupAnalysis, pk=pk, user=request.user)
        analysis.delete()
        return JsonResponse({'status': 'ok'})


import uuid as _uuid

class GenerateShareLinkView(LoginRequiredMixin, View):
    login_url = "/accounts/login/"

    def post(self, request, pk):
        analysis = get_object_or_404(StartupAnalysis, pk=pk, user=request.user)
        if not analysis.share_token:
            analysis.share_token = _uuid.uuid4()
            analysis.is_public = True
            analysis.save(update_fields=["share_token", "is_public"])
        share_url = request.build_absolute_uri(f"/dashboard/shared/{analysis.share_token}/")
        return JsonResponse({"status": "ok", "url": share_url})


class SharedResultsView(DetailView):
    model = StartupAnalysis
    template_name = "dashboard/results.html"
    context_object_name = "analysis"

    def get_object(self):
        return get_object_or_404(StartupAnalysis, share_token=self.kwargs["token"], is_public=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        analysis = self.object
        context["is_shared_view"] = True
        try:
            score = analysis.viability_score
            context["score"] = score
            context["score_dimensions_json"] = json.dumps(score.get_dimensions())
        except Exception:
            context["score"] = None
            context["score_dimensions_json"] = "{}"
        context["trend_data_json"] = json.dumps(analysis.trend_data or {})
        verdict_styles = {
            "likely": {"color": "emerald", "label": "Likely to Fund"},
            "neutral": {"color": "yellow", "label": "Neutral"},
            "unlikely": {"color": "red", "label": "Unlikely to Fund"},
        }
        context["investor_style"] = verdict_styles.get(analysis.investor_verdict, verdict_styles["neutral"])
        context["swot"] = {
            "strengths": analysis.swot_strengths,
            "weaknesses": analysis.swot_weaknesses,
            "opportunities": analysis.swot_opportunities,
            "threats": analysis.swot_threats,
        }
        return context
