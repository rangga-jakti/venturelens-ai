"""
VentureLens AI - Accounts Views
Authentication views: register, login, logout, profile.
"""

import logging
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views import View
from django.utils.decorators import method_decorator

from .forms import RegisterForm, LoginForm, ProfileForm
from apps.analysis.models import StartupAnalysis

logger = logging.getLogger(__name__)


class RegisterView(View):
    """User registration with email verification readiness."""
    template_name = 'accounts/register.html'

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('dashboard:history')
        return render(request, self.template_name, {'form': RegisterForm()})

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            messages.success(request, f'Welcome to VentureLens, {user.display_name}! 🚀')
            logger.info(f"New user registered: {user.email}")
            return redirect('analysis:input')
        return render(request, self.template_name, {'form': form})


class LoginView(View):
    """Secure login with brute-force protection awareness."""
    template_name = 'accounts/login.html'

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('analysis:input')
        next_url = request.GET.get('next', '')
        return render(request, self.template_name, {
            'form': LoginForm(),
            'next': next_url,
        })

    def post(self, request):
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            logger.info(f"User logged in: {user.email}")
            next_url = request.POST.get('next') or request.GET.get('next', '')
            if next_url and next_url.startswith('/'):
                return redirect(next_url)
            return redirect('analysis:input')

        # Don't reveal whether email exists
        return render(request, self.template_name, {
            'form': form,
            'next': request.POST.get('next', ''),
        })


class LogoutView(View):
    """Secure logout — POST only to prevent CSRF logout attacks."""

    def post(self, request):
        logout(request)
        messages.info(request, 'You have been logged out.')
        return redirect('core:landing')

    def get(self, request):
        # Redirect GET requests to home
        return redirect('core:landing')


@method_decorator(login_required, name='dispatch')
class ProfileView(View):
    """User profile — view stats and update preferences."""
    template_name = 'accounts/profile.html'

    def get(self, request):
        recent_analyses = StartupAnalysis.objects.filter(
            user=request.user,
            status=StartupAnalysis.Status.COMPLETED,
        ).select_related('viability_score').order_by('-created_at')[:5]

        return render(request, self.template_name, {
            'form': ProfileForm(instance=request.user),
            'recent_analyses': recent_analyses,
        })

    def post(self, request):
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('accounts:profile')

        recent_analyses = StartupAnalysis.objects.filter(
            user=request.user,
            status=StartupAnalysis.Status.COMPLETED,
        ).order_by('-created_at')[:5]

        return render(request, self.template_name, {
            'form': form,
            'recent_analyses': recent_analyses,
        })

class VerifyEmailSentView(View):
    """Show after registration - ask user to check email."""
    def get(self, request):
        return render(request, 'accounts/verify_email_sent.html')
