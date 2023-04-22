from pydantic import BaseModel, EmailStr


class HealthCheckSchema(BaseModel):
    email: EmailStr
    status_service: str
