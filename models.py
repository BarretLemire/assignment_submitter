from pydantic import BaseModel

class Course(BaseModel):
    id: int
    name: str

class Assignment(BaseModel):
    id: int
    title: str

class Submission(BaseModel):
    submission_type: str = "online_url"
    url: str