# app.py
from flask import Flask
from backend.routes import auth_bp, product_bp, receipt_bp
from extensions import mysql
import os
import socket


def create_app():
    app = Flask(__name__, static_folder='frontend/static', template_folder='frontend/templates')
    # Secret key for sessions/flash (env override supported)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-change-me')

    # MySQL config (env-overridable). Force TCP (localhost -> 127.0.0.1) on Windows.
    _host = os.getenv('MYSQL_HOST', '127.0.0.1')
    if _host.lower() in ('localhost', '::1'):
        _host = '127.0.0.1'
    app.config['MYSQL_HOST'] = _host
    # Determine port: env override, else probe 3306 then 3307
    _port_env = os.getenv('MYSQL_PORT')
    if _port_env is not None and str(_port_env).strip() != '':
        try:
            _port = int(str(_port_env).strip())
        except (ValueError, TypeError):
            _port = 3306
    else:
        def _port_open(host, port, timeout=0.5):
            try:
                with socket.create_connection((host, port), timeout=timeout):
                    return True
            except OSError:
                return False
        _port = 3306 if _port_open('127.0.0.1', 3306) else (3307 if _port_open('127.0.0.1', 3307) else 3306)
    app.config['MYSQL_PORT'] = _port
    app.config['MYSQL_USER'] = os.getenv('MYSQL_USER', 'root')
    app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD', '')
    app.config['MYSQL_DB'] = os.getenv('MYSQL_DB', 'product')

    # Log effective DB config (no secrets) for troubleshooting
    print(f"[DB] host={app.config['MYSQL_HOST']} port={app.config['MYSQL_PORT']} user={app.config['MYSQL_USER']} db={app.config['MYSQL_DB']}")
    mysql.init_app(app)

    # Ensure template changes reload and static files aren't cached in dev
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.jinja_env.auto_reload = True
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(product_bp)
    app.register_blueprint(receipt_bp)

    # Make mysql available to models/routes
    app.mysql = mysql

    return app
    
# Only for debugging
if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)


    
    
    