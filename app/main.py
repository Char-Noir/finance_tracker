from flask import Flask, jsonify, render_template, redirect, url_for
from app.database import initialize_database
from app.services.data_sources_service import ServiceException
from datetime import datetime
from asgiref.wsgi import WsgiToAsgi

# Import routers
from app.routers.data_sources import api_router as data_sources_api, page_router as data_sources_pages
from app.routers.financial_transactions import api_router as financial_transactions_api, page_router as financial_transactions_pages
from app.routers.list_router import api_router as list_api, page_router as list_pages
from app.routers.transaction_source_categories import api_router as tsc_api, page_router as tsc_pages
from app.routers.transaction_sources import api_router as ts_api, page_router as ts_pages
from app.routers.upload_transactions import api_router as upload_api, page_router as upload_pages

def create_app():
    app = Flask(__name__, template_folder='templates', static_folder='static')

    @app.template_filter('format_date')
    def format_date(value, format='%d.%m.%Y'):
        if isinstance(value, str):
            try:
                value = datetime.fromisoformat(value)
            except ValueError:
                return value # Return original value if parsing fails
        if isinstance(value, datetime):
            return value.strftime(format)
        return value

    @app.errorhandler(ServiceException)
    def handle_service_exception(e):
        return jsonify({"detail": e.message}), e.status_code

    @app.before_request
    async def before_request_func():
        await initialize_database()

    # Register API blueprints
    app.register_blueprint(data_sources_api, url_prefix='/api/data-sources')
    app.register_blueprint(financial_transactions_api, url_prefix='/api/financial-transactions')
    app.register_blueprint(list_api, url_prefix='/api/lists')
    app.register_blueprint(tsc_api, url_prefix='/api/transaction-source-categories')
    app.register_blueprint(ts_api, url_prefix='/api/transaction-sources')
    app.register_blueprint(upload_api, url_prefix='/api/upload-transactions')

    # Register Page blueprints
    app.register_blueprint(data_sources_pages, url_prefix='/data-sources')
    app.register_blueprint(financial_transactions_pages, url_prefix='/financial-transactions')
    app.register_blueprint(list_pages, url_prefix='/list')
    app.register_blueprint(tsc_pages, url_prefix='/transaction-source-category')
    app.register_blueprint(ts_pages, url_prefix='/transaction-sources')
    app.register_blueprint(upload_pages, url_prefix='/upload-transactions')

    @app.route('/')
    def index():
        # Redirect to the main transactions page
        return redirect(url_for('financial_transactions_pages.get_transactions_page'))

    return app

# Create the WSGI app
wsgi_app = create_app()
# Create an ASGI wrapper for the WSGI app
asgi_app = WsgiToAsgi(wsgi_app)

if __name__ == "__main__":
    # Run the original WSGI app for local development
    wsgi_app.run(host="0.0.0.0", port=8000)
