content = '''{% extends 'base.html' %}
{% block title %}Check Your Email — VentureLens AI{% endblock %}
{% block content %}
<div class="min-h-screen flex items-center justify-center px-6 py-20">
    <div class="w-full max-w-md animate-slide-up text-center">
        <div class="w-16 h-16 bg-gradient-to-br from-brand-500 to-purple-600 rounded-2xl flex items-center justify-center mx-auto mb-6">
            <svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"/>
            </svg>
        </div>
        <h1 class="font-display text-3xl font-700 text-white mb-3">Check your email</h1>
        <p class="text-white/40 mb-8">We sent a verification link to your email address. Click the link to activate your account.</p>
        <div class="glass-card rounded-2xl p-6 border border-white/10 text-left mb-6">
            <p class="text-white/60 text-sm">Didn\'t receive the email? Check your spam folder or</p>
            <a href="{% url 'accounts:register' %}" class="text-brand-400 hover:text-brand-300 text-sm transition-colors">try registering again</a>
        </div>
        <a href="{% url 'accounts:login' %}" class="text-white/30 hover:text-white/50 text-sm transition-colors">
            Back to login
        </a>
    </div>
</div>
{% endblock %}'''

open('templates/accounts/verify_email_sent.html', 'w', encoding='utf-8').write(content)
print('Done!')