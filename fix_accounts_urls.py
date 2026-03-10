content = open('apps/accounts/urls.py', encoding='utf-8').read()
old = "    path('profile/', views.ProfileView.as_view(), name='profile'),\n]"
new = "    path('profile/', views.ProfileView.as_view(), name='profile'),\n    path('verify-email-sent/', views.VerifyEmailSentView.as_view(), name='verify_email_sent'),\n]"
content = content.replace(old, new)
open('apps/accounts/urls.py', 'w', encoding='utf-8').write(content)
print('Done!')