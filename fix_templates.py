content = open('venturelens_project/settings/base.py', encoding='utf-8').read()
old = "        'APP_DIRS': True,"
new = """        'APP_DIRS': False,
        'loaders': [
            'django.template.loaders.filesystem.Loader',
            'django.template.loaders.app_directories.Loader',
        ],"""
content = content.replace(old, new)
open('venturelens_project/settings/base.py', 'w', encoding='utf-8').write(content)
print('Done!')