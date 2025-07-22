from flask import Blueprint, jsonify, request, render_template, Response
from app.services.data_sources_service import DataSourceService
from app.schemas.data_sources import DataSourceCreate, DataSourceUpdate

# Blueprint for API
api_router = Blueprint('data_sources_api', __name__)

# Blueprint for pages
page_router = Blueprint('data_sources_pages', __name__)

@page_router.route('/')
async def get_all_data_sources_page():
    service = DataSourceService()
    sources = await service.get_all_data_sources()
    return render_template('data-sources.html', sources=sources)

@api_router.route('/', methods=['GET'])
async def get_all_data_sources_api():
    service = DataSourceService()
    schemas = await service.get_all_data_sources()
    return jsonify([s.dict() for s in schemas])

@api_router.route('/sh', methods=['GET'])
async def get_all_data_sources_sh_api():
    service = DataSourceService()
    return jsonify(await service.get_all_data_sources_sh())

@api_router.route('/', methods=['POST'])
async def create_data_source_api():
    data = DataSourceCreate(**request.json)
    service = DataSourceService()
    new_source_schema = await service.create_data_source(data)
    return jsonify(new_source_schema.dict()), 201

@api_router.route('/<int:data_source_id>', methods=['PUT'])
async def update_data_source_api(data_source_id: int):
    data = DataSourceUpdate(**request.json)
    service = DataSourceService()
    updated_source_schema = await service.update_data_source(data_source_id, data)
    return jsonify(updated_source_schema.dict())

@api_router.route('/<int:data_source_id>', methods=['DELETE'])
async def delete_data_source_api(data_source_id: int):
    service = DataSourceService()
    await service.delete_data_source(data_source_id)
    return Response(status=204)