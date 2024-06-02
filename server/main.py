'''
Server proxy fix for use behind nginx
'''

from werkzeug.middleware.proxy_fix import ProxyFix
from server import create_app

app = create_app()

app.wsgi_app = ProxyFix(
    app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1
)

