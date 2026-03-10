content = open('venturelens_project/settings/base.py', encoding='utf-8').read()
old = """        'APP_DIRS': False,
        'loaders': [
            'django.template.loaders.filesystem.Loader',
            'django.template.loaders.app_directories.Loader',
        ],"""
new = """        'APP_DIRS': False,"""
content = content.replace(old, new)

# Add loaders inside OPTIONS
old2 = "            'context_processors': ["
new2 = """            'loaders': [
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
            ],
            'context_processors': ["""
content = content.replace(old2, new2)
open('venturelens_project/settings/base.py', 'w', encoding='utf-8').write(content)
print('Done!')