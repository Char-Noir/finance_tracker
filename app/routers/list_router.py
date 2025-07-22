from flask import Blueprint, jsonify, request, render_template
from app.services.list_service import ListService
from app.schemas.list import ListCreateRequest, ListUpdateRequest

# Blueprint for API
api_router = Blueprint('list_api', __name__)

# Blueprint for pages
page_router = Blueprint('list_pages', __name__)

@page_router.route('/')
async def get_lists_page():
    service = ListService()
    page = request.args.get('page', 1, type=int)
    size = request.args.get('size', 10, type=int)
    sort_by = request.args.get('sort_by', 'created_at', type=str)
    order = request.args.get('order', 'desc', type=str)
    data = await service.get_all(page, size, sort_by, order)
    return render_template('list.html', data=data)

@api_router.route('/', methods=['GET'])
async def get_lists_api():
    service = ListService()
    page = request.args.get('page', 1, type=int)
    size = request.args.get('size', 10, type=int)
    sort_by = request.args.get('sort_by', 'created_at', type=str)
    order = request.args.get('order', 'desc', type=str)
    return jsonify(await service.get_all(page, size, sort_by, order))

@api_router.route('/<int:list_id>', methods=['GET'])
async def get_list_api(list_id: int):
    service = ListService()
    return jsonify(await service.get_by_id(list_id))

@api_router.route('/', methods=['POST'])
async def create_list_api():
    data = ListCreateRequest(**request.json)
    service = ListService()
    return jsonify(await service.create(data.name, data.author))

@api_router.route('/<int:list_id>', methods=['PUT'])
async def update_list_api(list_id: int):
    data = ListUpdateRequest(**request.json)
    service = ListService()
    updated_list = await service.update(list_id, data.name)
    return jsonify(updated_list)

@api_router.route('/<int:list_id>', methods=['DELETE'])
async def delete_list_api(list_id: int):
    service = ListService()
    return jsonify(await service.delete(list_id))