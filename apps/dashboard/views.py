class GenerateShareLinkView(LoginRequiredMixin, View):
    login_url = '/accounts/login/'

    def post(self, request, pk):
        analysis = get_object_or_404(StartupAnalysis, pk=pk, user=request.user)
        if not analysis.share_token:
            analysis.share_token = uuid.uuid4()
            analysis.is_public = True
            analysis.save(update_fields=['share_token', 'is_public'])
        share_url = request.build_absolute_uri(f'/dashboard/shared/{analysis.share_token}/')
        return JsonResponse({'status': 'ok', 'url': share_url})


class SharedResultsView(DetailView):
    model = StartupAnalysis
    template_name = 'dashboard/results.html'
    context_object_name = 'analysis'

    def get_object(self):
        return get_object_or_404(StartupAnalysis, share_token=self.kwargs['token'], is_public=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        analysis = self.object
        context['is_shared_view'] = True
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
        return contextimport uuid as _uuid
class GenerateShareLinkView(LoginRequiredMixin, View):
    login_url = '/accounts/login/'
    def post(self, request, pk):
        analysis = get_object_or_404(StartupAnalysis, pk=pk, user=request.user)
        if not analysis.share_token:
            analysis.share_token = _uuid.uuid4()
            analysis.is_public = True
            analysis.save(update_fields=['share_token', 'is_public'])
        share_url = request.build_absolute_uri(f'/dashboard/shared/{analysis.share_token}/')
        return JsonResponse({'status': 'ok', 'url': share_url})
class SharedResultsView(DetailView):
    model = StartupAnalysis
    template_name = 'dashboard/results.html'
    context_object_name = 'analysis'
    def get_object(self):
        return get_object_or_404(StartupAnalysis, share_token=self.kwargs['token'], is_public=True)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        analysis = self.object
        context['is_shared_view'] = True
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
import uuid as _uuid
class GenerateShareLinkView(LoginRequiredMixin, View):
    login_url = '/accounts/login/'
    def post(self, request, pk):
        analysis = get_object_or_404(StartupAnalysis, pk=pk, user=request.user)
        if not analysis.share_token:
            analysis.share_token = _uuid.uuid4()
            analysis.is_public = True
            analysis.save(update_fields=['share_token', 'is_public'])
        share_url = request.build_absolute_uri(f'/dashboard/shared/{analysis.share_token}/')
        return JsonResponse({'status': 'ok', 'url': share_url})
class SharedResultsView(DetailView):
    model = StartupAnalysis
    template_name = 'dashboard/results.html'
    context_object_name = 'analysis'
    def get_object(self):
        return get_object_or_404(StartupAnalysis, share_token=self.kwargs['token'], is_public=True)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        analysis = self.object
        context['is_shared_view'] = True
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
