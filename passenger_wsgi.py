# -*- coding: utf-8 -*-
import os, sys
sys.path.insert(0, '/var/www/u1991005/data/www/ardulove.ru/ardulove')
sys.path.insert(1, '/var/www/u1991005/data/www/ardulove.ru/venv/lib/python3.8/site-packages')
os.environ['DJANGO_SETTINGS_MODULE'] = 'ardulove.settings'
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()