# routes/__init__.py
from flask import Blueprint

# ── Blueprints ─────────────────────────────────────
auth_bp    = Blueprint('auth',    __name__, url_prefix='')
product_bp = Blueprint('product', __name__, url_prefix='/product')
receipt_bp = Blueprint('receipt', __name__, url_prefix='/receipt')

# ── Import the route modules (so decorators are executed) ──
from . import auth_routes, product_routes, receipt_routes   # noqa: F401,E402