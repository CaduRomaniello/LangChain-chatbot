import json
import traceback

from database import get_db
from sqlalchemy import text
from modules.appointment_setting.entity import AppointmentSettingEntity
from models import CreateAppointmentSettingModel, UpdateAppointmentSettingModel

def get_appointment_setting_by_phone_number(phone_number: str) -> AppointmentSettingEntity:
    try:
        query = text(
            "SELECT * FROM public.appointment_setting WHERE phone_number = :phone_number"
        ).bindparams(phone_number=phone_number)

        return get_db().execute(query).first()

    except Exception as e:
        print(e, traceback.print_exc())
        get_db().rollback()
        return None
    
def create_appointment_setting(appointment_setting: CreateAppointmentSettingModel) -> AppointmentSettingEntity:
    try:
        if not appointment_setting.phone_number:
           raise Exception('phone_number is required')
       
        row = get_appointment_setting_by_phone_number(appointment_setting.phone_number)
        if row:
            raise Exception('phone_number already exists')
        
        conversation_history_json = [json.dumps(x.to_dict(), ensure_ascii = False) for x in appointment_setting.conversation_history]

        query = text(
            f"INSERT INTO public.appointment_setting (phone_number, name, email, conversation_history) VALUES (:phone_number, :name, :email, ARRAY {conversation_history_json}::jsonb[]);"
        ).bindparams(
            phone_number=appointment_setting.phone_number,
            name=appointment_setting.name,
            email=appointment_setting.email,
        )

        get_db().execute(query)
        get_db().commit()
        return get_appointment_setting_by_phone_number(appointment_setting.phone_number)
    except Exception as e:
        print(e, traceback.print_exc())
        get_db().rollback()
        return None
    
def update_appointment_setting(appointment_setting: UpdateAppointmentSettingModel) -> AppointmentSettingEntity:
    try:
        if not appointment_setting.phone_number:
           raise Exception('phone_number is required')
       
        query = text(
            "SELECT * FROM public.appointment_setting WHERE phone_number = :phone_number"
        ).bindparams(phone_number=appointment_setting.phone_number)

        row =  get_db().execute(query).first()

        if not row:
            raise Exception('phone_number does not exists')
        
        conversation_history_json = [json.dumps(x.to_dict(), ensure_ascii = False) for x in appointment_setting.conversation_history]

        name = appointment_setting.name if appointment_setting.name else row.name
        email = appointment_setting.email if appointment_setting.email else row.email
        conversation_history = conversation_history_json if appointment_setting.conversation_history else row.conversation_history

        query = text(
            f"""
            UPDATE public.appointment_setting 
            SET name = :name, email = :email, conversation_history = ARRAY {conversation_history}::jsonb[]
            WHERE phone_number = :phone_number;
            """
        ).bindparams(
            phone_number=appointment_setting.phone_number,
            name=name,
            email=email,
        )

        get_db().execute(query)
        get_db().commit()
        return get_appointment_setting_by_phone_number(appointment_setting.phone_number)
    except Exception as e:
        print(e, traceback.print_exc())
        get_db().rollback()
        return None