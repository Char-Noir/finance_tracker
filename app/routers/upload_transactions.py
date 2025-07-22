from flask import Blueprint, request, jsonify, render_template
from app.services.upload_transactions_service import UploadTransactionsService
from app.services.data_sources_service import DataSourceService
import pandas as pd

# Blueprint for API
api_router = Blueprint('upload_transactions_api', __name__)

# Blueprint for pages
page_router = Blueprint('upload_transactions_pages', __name__)

@page_router.route('/')
async def upload_page():
    data_source_service = DataSourceService()
    data_sources = await data_source_service.get_all_data_sources()
    return render_template('upload_transactions.html', data_sources=data_sources)

@api_router.route('/', methods=['POST'])
async def upload_transactions_api():
    service = UploadTransactionsService()
    if 'file' not in request.files:
        return jsonify({"detail": "No file part"}), 400

    file = request.files['file']
    data_source_id = request.form.get('data_source_id', type=int)

    if file.filename == '':
        return jsonify({"detail": "No selected file"}), 400

    if not data_source_id:
        return jsonify({"detail": "data_source_id is required"}), 400

    if file and file.content_type == "text/csv":
        try:
            df = pd.read_csv(file, delimiter=",")
            await service.process_csv(data_source_id, df)
            return jsonify({"message": "Завантажено успішно."})
        except Exception as e:
            return jsonify({"detail": str(e)}), 400
    else:
        return jsonify({"detail": "Файл повинен бути csv."}), 400
