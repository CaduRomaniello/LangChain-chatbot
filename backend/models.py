from typing import List
from pydantic import BaseModel

from modules.appointment_setting.entity import ConversationHistory

class CreateAppointmentSettingModel(BaseModel):
    phone_number: str
    name: str = None
    email: str = None
    conversation_history: List[ConversationHistory] = None

class UpdateAppointmentSettingModel(BaseModel):
    phone_number: str
    name: str = None
    email: str = None
    conversation_history: List[ConversationHistory] = None