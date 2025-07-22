from flask import Blueprint, jsonify, request, render_template, Response
from app.services.transaction_source_category_service import TransactionSourceCategoryService
from app.schemas.transaction_source_category import TransactionSourceCategoryCreate, TransactionSourceCategoryUpdate

# Blueprint for API
api_router = Blueprint('transaction_source_categories_api', __name__)

# Blueprint for pages
page_router = Blueprint('transaction_source_categories_pages', __name__)

@page_router.route('/')
async def get_all_page():
    service = TransactionSourceCategoryService()
    categories = await service.get_all()
    return render_template('transaction_source_category.html', categories=categories)

@api_router.route('/', methods=['GET'])
async def get_all_api():
    service = TransactionSourceCategoryService()
    schemas = await service.get_all()
    return jsonify([s.dict() for s in schemas])

@api_router.route('/sh', methods=['GET'])
async def get_all_sh_api():
    service = TransactionSourceCategoryService()
    return jsonify(await service.get_all_sh())

@api_router.route('/', methods=['POST'])
async def create_api():
    data = TransactionSourceCategoryCreate(**request.json)
    service = TransactionSourceCategoryService()
    new_schema = await service.create(data)
    return jsonify(new_schema.dict()), 201

@api_router.route('/<int:category_id>', methods=['PUT'])
async def update_api(category_id: int):
    data = TransactionSourceCategoryUpdate(**request.json)
    service = TransactionSourceCategoryService()
    updated_schema = await service.update(category_id, data)
    return jsonify(updated_schema.dict())

@api_router.route('/<int:category_id>', methods=['DELETE'])
async def delete_api(category_id: int):
    service = TransactionSourceCategoryService()
    await service.delete(category_id)
    return Response(status=204)