from flask import Blueprint, jsonify, request, render_template, Response
from app.services.financial_transactions_service import FinancialTransactionService
from app.schemas.financial_transaction import FinancialTransactionCreate, FinancialTransactionUpdate

# Blueprint for API
api_router = Blueprint('financial_transactions_api', __name__)

# Blueprint for pages
page_router = Blueprint('financial_transactions_pages', __name__)

@page_router.route('/')
async def get_transactions_page():
    service = FinancialTransactionService()
    page = request.args.get('page', 1, type=int)
    sort = request.args.get('sort', 'date', type=str)
    order = request.args.get('order', 'asc', type=str)
    start_date = request.args.get('start_date', type=str)
    end_date = request.args.get('end_date', type=str)
    source = request.args.get('source', type=str)
    category = request.args.get('category', type=str)
    bank = request.args.get('bank', type=str)
    min_amount = request.args.get('min_amount', type=float)
    max_amount = request.args.get('max_amount', type=float)
    data = await service.get_all(page, sort, order, start_date, end_date, source, category, bank, min_amount, max_amount)
    return render_template('financial_transactions.html', data=data)

@api_router.route('/', methods=['GET'])
async def get_transactions_api():
    service = FinancialTransactionService()
    page = request.args.get('page', 1, type=int)
    sort = request.args.get('sort', 'date', type=str)
    order = request.args.get('order', 'asc', type=str)
    start_date = request.args.get('start_date', type=str)
    end_date = request.args.get('end_date', type=str)
    source = request.args.get('source', type=str)
    category = request.args.get('category', type=str)
    bank = request.args.get('bank', type=str)
    min_amount = request.args.get('min_amount', type=float)
    max_amount = request.args.get('max_amount', type=float)
    # This service method already returns a JSON-serializable dict
    return jsonify(await service.get_all(page, sort, order, start_date, end_date, source, category, bank, min_amount, max_amount))

@api_router.route('/', methods=['POST'])
async def create_api():
    data = FinancialTransactionCreate(**request.json)
    service = FinancialTransactionService()
    new_transaction_schema = await service.create(data)
    return jsonify(new_transaction_schema.dict()), 201

@api_router.route('/<int:transaction_id>', methods=['PUT'])
async def update_api(transaction_id: int):
    data = FinancialTransactionUpdate(**request.json)
    service = FinancialTransactionService()
    updated_transaction_schema = await service.update(transaction_id, data)
    return jsonify(updated_transaction_schema.dict())

@api_router.route('/<int:transaction_id>', methods=['DELETE'])
async def delete_api(transaction_id: int):
    service = FinancialTransactionService()
    await service.delete(transaction_id)
    return Response(status=204)