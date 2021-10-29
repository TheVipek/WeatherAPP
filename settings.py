import os
#Static files (CSS ,JS ,Images)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

STATIC_ROOT = os.path.join(BASE_DIR,'static')
STATIC_URL = '/static/'


#Templates (HTML FILES)

TEMPLATE_ROOT = os.path.join(BASE_DIR,'templates')
TEMPLATES_URL = '/templates/'
    