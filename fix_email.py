content = open('venturelens_project/settings/base.py', encoding='utf-8').read()
addition = '''
# ── Email (Resend via Anymail) ────────────────────────────────
EMAIL_BACKEND = 'anymail.backends.resend.EmailBackend'
ANYMAIL = {
    'RESEND_API_KEY': os.environ.get('RESEND_API_KEY', ''),
}
DEFAULT_FROM_EMAIL = os.environ.get('EMAIL_FROM', 'onboarding@resend.dev')
SERVER_EMAIL = DEFAULT_FROM_EMAIL

# ── Allauth email verification ────────────────────────────────
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
ACCOUNT_CONFIRM_EMAIL_ON_GET = True
'''
content += addition
open('venturelens_project/settings/base.py', 'w', encoding='utf-8').write(content)
print('Done!')