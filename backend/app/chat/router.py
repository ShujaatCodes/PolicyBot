from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse

from app.auth.dependencies import get_current_user
from app.chat.schemas import ChatRequest, ChatResponse
from app.chat.service import generate_stream, get_rag_response
from app.models import User

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("/", response_model=ChatResponse)
async def chat(
    body: ChatRequest,
    _: User = Depends(get_current_user),
):
    result = await get_rag_response(body.question)
    return ChatResponse(**result)


@router.post("/stream")
async def chat_stream(
    body: ChatRequest,
    _: User = Depends(get_current_user),
):
    return StreamingResponse(
        generate_stream(body.question),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
            "Connection": "keep-alive",
        },
    )
