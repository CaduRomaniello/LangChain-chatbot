import modules.appointment_setting.service as service

from fastapi import APIRouter
from modules.appointment_setting.dto import APPOINTMENTSETTINGDTO
from modules.appointment_setting.entity import AppointmentSettingEntity
from models import CreateAppointmentSettingModel, UpdateAppointmentSettingModel

router = APIRouter(prefix="/appointment_setting")

@router.get("/", response_model=APPOINTMENTSETTINGDTO, description="Get appointment setting by phone number")
async def get_appointment_setting(phone_number: str) -> APPOINTMENTSETTINGDTO:
    return APPOINTMENTSETTINGDTO.from_entity_to_DTO(service.get_appointment_setting_by_phone_number(phone_number))

@router.post("/", response_model=APPOINTMENTSETTINGDTO, description="Create appointment setting")
async def create_appointment_setting(appointment_setting:CreateAppointmentSettingModel) -> APPOINTMENTSETTINGDTO:
    return APPOINTMENTSETTINGDTO.from_entity_to_DTO(service.create_appointment_setting(appointment_setting))

@router.patch("/", response_model=APPOINTMENTSETTINGDTO, description="Update appointment setting")
async def update_appointment_setting(appointment_setting:UpdateAppointmentSettingModel) -> APPOINTMENTSETTINGDTO:
    return APPOINTMENTSETTINGDTO.from_entity_to_DTO(service.update_appointment_setting(appointment_setting))