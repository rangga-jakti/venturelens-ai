# Update register view to redirect to Google
content = open('apps/accounts/views.py', encoding='utf-8').read()
old = """class RegisterView(View):
    \"\"\"User registration with email verification readiness.\"\"\"
    template_name = 'accounts/register.html'
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('dashboard:history')
        return render(request, self.template_name, {'form': RegisterForm()})
    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.is_active = False
            user.save()
            # Send verification email via allauth
            from allauth.account.utils import send_email_confirmation
            send_email_confirmation(request, user, signup=True)
            logger.info(f"New user registered (pending verification): {user.email}")
            return redirect('accounts:verify_email_sent')
        return render(request, self.template_name, {'form': form})"""
new = """class RegisterView(View):
    \"\"\"Redirect to Google OAuth - Google Only login.\"\"\"
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('analysis:input')
        from allauth.socialaccount.providers.google.views import oauth2_login
        return redirect('/accounts/google/login/')
    def post(self, request):
        return redirect('/accounts/google/login/')"""
content = content.replace(old, new)
open('apps/accounts/views.py', 'w', encoding='utf-8').write(content)
print('Done!')