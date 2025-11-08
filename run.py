import os
from flask import Flask, send_from_directory
from config import Config
from extensions import mysql
from backend.routes import auth_bp, product_bp, receipt_bp

def create_app():
    # create app and load config
    app = Flask(__name__, static_folder='static', template_folder='templates')
    app.config.from_object(Config)

    # init extensions
    mysql.init_app(app)

    # register all blueprints (routes)
    app.register_blueprint(auth_bp)
    app.register_blueprint(product_bp)
    app.register_blueprint(receipt_bp)

    # optional compatibility route — serves files from static/img
    @app.route('/img/<path:filename>')
    def serve_img(filename):
        img_dir = os.path.join(app.root_path, 'static', 'img')
        return send_from_directory(img_dir, filename)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)