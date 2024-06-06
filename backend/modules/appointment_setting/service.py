import modules.appointment_setting.repository as repository

from modules.appointment_setting.entity import AppointmentSettingEntity

def get_appointment_setting_by_phone_number(phone_number: str) -> AppointmentSettingEntity:
    return repository.get_appointment_setting_by_phone_number(phone_number)

def create_appointment_setting(appointment_setting: dict) -> AppointmentSettingEntity:
    return repository.create_appointment_setting(appointment_setting)

def update_appointment_setting(appointment_setting: dict) -> AppointmentSettingEntity:
    return repository.update_appointment_setting(appointment_setting)