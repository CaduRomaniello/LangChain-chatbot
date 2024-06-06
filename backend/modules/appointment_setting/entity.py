from database import Base
from pydantic import BaseModel
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy import Column, String

class ConversationHistory(BaseModel):
    message_type: str
    message: str

    def to_dict(self):
        return {"message_type": self.message_type, "message": self.message}

class AppointmentSettingEntity(Base):
    __tablename__ = "appointment_setting"
    __table_args__ = {"schema": "public"}

    phone_number = Column(String,  primary_key=True, nullable=False)
    name = Column(String, nullable=True)
    email = Column(String, nullable=True)
    conversation_history = Column(JSONB, nullable=True)
    
    