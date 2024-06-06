from typing import List
from dataclasses import dataclass
from modules.appointment_setting.entity import AppointmentSettingEntity, ConversationHistory

@dataclass
class APPOINTMENTSETTINGDTO:
    phone_number: str
    name: str
    email: str    
    conversation_history: List[ConversationHistory]

    @staticmethod
    def from_entity_to_DTO(appointment_setting: AppointmentSettingEntity):
        return APPOINTMENTSETTINGDTO(
            phone_number = appointment_setting.phone_number,
            name = appointment_setting.name,
            email = appointment_setting.email,
            conversation_history = [ConversationHistory(**x) for x in appointment_setting.conversation_history] if appointment_setting.conversation_history else []
        )