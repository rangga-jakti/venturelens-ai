content = open('venturelens_project/settings/base.py', encoding='utf-8').read()
old = """ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = 'email'"""
new = """ACCOUNT_LOGIN_METHODS = {'email'}
ACCOUNT_SIGNUP_FIELDS = ['email*', 'password1*', 'password2*']"""
content = content.replace(old, new)
open('venturelens_project/settings/base.py', 'w', encoding='utf-8').write(content)
print('Done!')