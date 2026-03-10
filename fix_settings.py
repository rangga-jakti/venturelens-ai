content = open('venturelens_project/settings/base.py', encoding='utf-8').read()
old = "    'django_htmx.middleware.HtmxMiddleware',\n]"
new = "    'django_htmx.middleware.HtmxMiddleware',\n    'allauth.account.middleware.AccountMiddleware',\n]"
content = content.replace(old, new)
open('venturelens_project/settings/base.py', 'w', encoding='utf-8').write(content)
print('Done!')