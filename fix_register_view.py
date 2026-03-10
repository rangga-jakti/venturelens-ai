content = open('apps/accounts/views.py', encoding='utf-8').read()
old = """    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            messages.success(request, f'Welcome to VentureLens, {user.display_name}! ðŸš€')
            logger.info(f"New user registered: {user.email}")
            return redirect('analysis:input')
        return render(request, self.template_name, {'form': form})"""
new = """    def post(self, request):
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
content = content.replace(old, new)
open('apps/accounts/views.py', 'w', encoding='utf-8').write(content)
print('Done!')