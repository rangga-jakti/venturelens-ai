content = open('apps/accounts/views.py', encoding='utf-8').read()
addition = '''
class VerifyEmailSentView(View):
    """Show after registration - ask user to check email."""
    def get(self, request):
        return render(request, 'accounts/verify_email_sent.html')
'''
content += addition
open('apps/accounts/views.py', 'w', encoding='utf-8').write(content)
print('Done!')