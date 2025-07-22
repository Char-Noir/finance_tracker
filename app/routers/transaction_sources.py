from flask import Blueprint, jsonify, request, render_template, Response
from app.services.transaction_sources_service import TransactionSourceService
from app.services.transaction_source_category_service import TransactionSourceCategoryService
from app.schemas.transaction_sources import TransactionSourceCreate, TransactionSourceUpdate

# Blueprint for API
api_router = Blueprint('transaction_sources_api', __name__)

# Blueprint for pages
page_router = Blueprint('transaction_sources_pages', __name__)

@page_router.route('/')
async def get_all_page():
    source_service = TransactionSourceService()
    category_service = TransactionSourceCategoryService()
    sources = await source_service.get_all()
    categories_schemas = await category_service.get_all()
    categories = [c.dict() for c in categories_schemas]
    return render_template('transaction_sources.html', sources=sources, categories=categories)

@api_router.route('/', methods=['GET'])
async def get_all_api():
    service = TransactionSourceService()
    # This service method already returns a list of JSON-serializable dicts
    return jsonify(await service.get_all())

@api_router.route('/sh', methods=['GET'])
async def get_all_sh_api():
    service = TransactionSourceService()
    return jsonify(await service.get_all_sh())

@api_router.route('/', methods=['POST'])
async def create_api():
    data = TransactionSourceCreate(**request.json)
    service = TransactionSourceService()
    new_schema = await service.create(data)
    return jsonify(new_schema.dict()), 201

@api_router.route('/<int:source_id>', methods=['PUT'])
async def update_api(source_id: int):
    data = TransactionSourceUpdate(**request.json)
    service = TransactionSourceService()
    updated_schema = await service.update(source_id, data)
    return jsonify(updated_schema.dict())

@api_router.route('/<int:source_id>', methods=['DELETE'])
async def delete_api(source_id: int):
    service = TransactionSourceService()
    await service.delete(source_id)
    return Response(status=204)
