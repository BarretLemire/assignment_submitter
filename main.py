import os

import requests

from dotenv import load_dotenv

from models import Course, Assignment, Submission

from fastapi import FastAPI


app = FastAPI()

#https://dixietech.instructure.com/courses/942225/assignments

load_dotenv()

access_token = os.getenv("ACCESS_TOKEN")

base_url = "https://dixietech.instructure.com/api/v1"

headers: dict[str, str] = {
    "Authorization": f"Bearer {access_token}"
}


class CanvasAPI:
    def __init__(self, base_url, access_token):
        self.base_url = base_url
        self.access_token = access_token
        self.headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        
    def submit_assignment(self, course_id, assignment_id, submission_file):
        url = f"{self.base_url}/courses/{course_id}/assignments/{assignment_id}/submissions"
        payload = {
                "submission[submission_type]": "online_url",
                "submission[url]": submission_file
            }
        response = requests.put(url, headers=self.headers, json=payload)
        return response.status_code == 200, response.json() if response.status_code == 200 else response.text

canvas_api = CanvasAPI(base_url, access_token)

@app.get("/courses")
async def get_courses() -> list[Course]:
    response = requests.get(url=f"{base_url}/courses", headers=headers)
    r_json = response.json()
    courses: list[Course] = []
    for course_json in r_json:
        course = Course(id=course_json["id"], name=course_json["name"])
        courses.append(course)
    return courses

@app.get("/courses/{course_id}/assignments")
async def get_assignments(course_id: int) -> list[Assignment]:
    response = requests.get(url=f"{base_url}/courses/{course_id}/assignments?per_page=50", headers=headers)
    r_json = response.json()
    assignments: list[Assignment] = []
    for assignment_json in r_json:
        assignment = Assignment(id=assignment_json["id"], title=assignment_json["name"])
        assignments.append(assignment)
    return assignments
    
@app.post("/courses/{course_id}/assignments/{assignment_id}/submissions")
async def submit_assignment(course_id: int, assignment_id: int, submission_file: str):
    success, response = canvas_api.submit_assignment(course_id, assignment_id, submission_file)
    if success:
        return {"message": "Assignment submitted successfully", "response": response}
    else:
        return {"error": "Failed to submit assignment", "response": response}