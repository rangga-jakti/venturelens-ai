content = open('venturelens_project/urls.py', encoding='utf-8').read()
old = "    path('dashboard/', include('apps.dashboard.urls', namespace='dashboard')),\n]"
new = "    path('dashboard/', include('apps.dashboard.urls', namespace='dashboard')),\n    path('accounts/', include('allauth.urls')),\n]"
content = content.replace(old, new)
open('venturelens_project/urls.py', 'w', encoding='utf-8').write(content)
print('Done!')