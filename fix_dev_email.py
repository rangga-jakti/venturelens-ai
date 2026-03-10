content = open('venturelens_project/settings/development.py', encoding='utf-8').read()
old = "EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'"
new = "# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'  # disabled: using Resend"
content = content.replace(old, new)
open('venturelens_project/settings/development.py', 'w', encoding='utf-8').write(content)
print('Done!')