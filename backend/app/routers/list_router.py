from fastapi import APIRouter, Query, Depends, WebSocket, WebSocketDisconnect
from app.services.list_service import ListService
from app.schemas.list import ListCreateRequest, ListUpdateRequest
from typing import Dict, List

router = APIRouter(prefix="/lists", tags=["Lists"])

active_connections: Dict[int, List[WebSocket]] = {}

@router.get("/")
async def get_lists(
    page: int = Query(1),
    size: int = Query(10),
    sort_by: str = Query("created_at"),
    order: str = Query("desc"),
    service: ListService = Depends(ListService)
):
    return await service.get_all(page, size, sort_by, order)

@router.get("/{list_id}")
async def get_list(list_id: int, service: ListService = Depends(ListService)):
    return await service.get_by_id(list_id)

@router.post("/")
async def create_list(data: ListCreateRequest, service: ListService = Depends(ListService)):
    return await service.create(data.name, data.author)

@router.put("/{list_id}")
async def update_list(list_id: int, data: ListUpdateRequest, service: ListService = Depends(ListService)):
    updated_list = await service.update(list_id, data.name)
    
    if list_id in active_connections:
        for connection in active_connections[list_id]:
            await connection.send_json({"list_id": list_id, "new_name": data.name})
    
    return updated_list

@router.websocket("/ws/{list_id}")
async def websocket_endpoint(websocket: WebSocket, list_id: int):
    await websocket.accept()
    
    if list_id not in active_connections:
        active_connections[list_id] = []
    active_connections[list_id].append(websocket)
    
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        active_connections[list_id].remove(websocket)
        if not active_connections[list_id]:
            del active_connections[list_id]

@router.delete("/{list_id}")
async def delete_list(list_id: int, service: ListService = Depends(ListService)):
    return await service.delete(list_id)