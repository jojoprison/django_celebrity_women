import os
import sys

# здесь изначально забыл путь к папке с хостом типа .beget.tech и тд
sys.path.insert(0, '/home/j/jojoskate/jojoskate.beget.tech')
# здесь указываем путь к либам именного того окружения, которое засунем в .htaccess
sys.path.insert(1, '/home/j/jojoskate/jojoskate.beget.tech/djangoenv/lib/python3.9/site-packages')
os.environ['DJANGO_SETTINGS_MODULE'] = 'sqsite.settings'

from django.core.wsgi import get_wsgi_application

# вызываем функция не как из гайда на бегете, но так пашет - мб альтернатива)
application = get_wsgi_application()
