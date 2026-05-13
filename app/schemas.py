from pydantic import BaseModel

class UploadResponse(BaseModel):
    status: str
    records_loaded: int
    students: int

class StudentTwosCount(BaseModel):
    full_name: str
    count_twos: int