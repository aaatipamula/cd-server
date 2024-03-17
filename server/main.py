'''
Server proxy fix for use behind nginx
'''

from werkzeug.middleware.proxy_fix import ProxyFix
from server.server import app

app.wsgi_app = ProxyFix(
    app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1
)

