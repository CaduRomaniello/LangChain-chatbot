import modules.chat.service as service

from fastapi import APIRouter
from pydantic import BaseModel
from modules.chat.dto import CHATDTO

router = APIRouter(prefix="/chat")

class ChatParams(BaseModel):
    phone_number: str
    message: str

@router.post("/", response_model=CHATDTO, description="Get response from LLM")
async def get_chat_response(params: ChatParams) -> CHATDTO:
    return CHATDTO.from_entity_to_DTO(service.get_response_from_llm(params))