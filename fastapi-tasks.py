from fastapi import FastAPI, Query, Path, Body, HTTPException
from pydantic import BaseModel, EmailStr
from typing import Optional, List

app = FastAPI()
#uvicorn main:app --reload
@app.get("/")
def read_root():
    """Return a greeting message."""
    return {"message": "Hello, World!"}

##create a post endpoint called postApplication() return "message": "Application submitted successfully"

# @app.post("/application")
# def postApplication():
#     """Return a greeting message."""
#     return {"message": "Application submitted successfully"}

#Create another POST request called applyForCandidate() -> /application/{candidate_id}
#return "Application for candidateID: 122 successfully submitted"

@app.post("/apply/{candidate_id}")
def apply(candidate_id: str):
    return {
        "status": "success",
        "message": f"Application for {candidate_id} successfully submitted"
    }

#add a get request called /applications it should support query params.
#If the  query params are included in the request return ---> "Here is your application for {CompanyName}"
#If the query param is not included in the request return ---> "Here are all of your application"

# @app.get("/applications")
# def get_applications(company_name: str = Query(None, description="optional query param for company_name")):
#     if company_name:
#         return {"status": "success",
#                "message": "Here is your application for " + company_name
#         }
#     else:
#         return {"status": "success",
#                "message": "Here are all of your application"
#         }



#Build a simple API for managing job applications using FastAPI.
# 1. POST /applications
# Accepts a JSON request body with:

# {
#   "candidate_id": "abc123",
#   "name": "Alice Smith",
#   "email": "alice@example.com",
#   "job_id": "job456"
# }
#data model
class Candidate(BaseModel):
    candidate_id: str
    name: str
    email: str
    job_id: str

#"database" - list in cache memory
applications: List[Candidate] = []

@app.post("/applications")
def postApplication(candidate: Candidate):
    applications.append(candidate)
    return {
        "status": "success",
        "message": f"Application successfully submitted for {candidate.name}"
    }

# 2.GET /applications
# Optional query parameters:
# company_name: st
# candidate_email: str
# If query params are present, return filtered message:
# Here is your application for {company_name}
# Here is your application for {candidate_email}
# If not, return:
# Here are all of your applications

@app.get("/applications")
def get_applications(company_name: str = Query(None, description="optional query param for company_name"), company_email: str = Query(None, description="optional query param for company_email")):
    if company_name:
        return {
            "status": "success",
            "message": f"Here is your application for {company_name}"
        }
    elif company_email:
        return {
            "status": "success",
            "message": f"Here is your application for {company_email}"
        }
    else:
        return {
            "status": "success",
            "message": "Here are all of your applications"
        }

# 3. GET /applications/{candidate_id}
# Use a path parameter
# Return a message like:
# Application found for candidate ID: abc123

@app.get("/applications/{candidate_id}")
def getCandidateId(candidate_id = int):
    return {
    "status": "success",
    "message": f"Application found for {candidate_id}"
}

# 4.PUT /applications/{candidate_id}
# Use a path param and accept a JSON body:
# {
#   "email": "newemail@example.com",
#   "job_id": "job789"
# }

class Candidate(BaseModel):
    email: str
    job_id: str

applications: List[Candidate] = []

@app.put("/applications/{candidate_id}")
def putCandidate(candidate_id: str, candidate: Candidate):
    return {
        "status": "success",
        "message": f"Application updated for {candidate.email} with job {candidate.job_id}"
    }


# 5.PATCH /applications/{candidate_id}
# Update only 1 field: email OR job_id
# Request body is optional keys
# Return a message showing updated fields
# added EmailSt(pydantic)
# from fastapi import FastAPI, HTTPException, Path
# from pydantic import BaseModel
# from typing import Optional

# app = FastAPI()

# # Mock database (for demo purposes)
# applications_db = {
#     "123": {"email": "old@example.com", "job_id": 101}
# }

class UpdateApplication(BaseModel):
    email: Optional[EmailStr] = None
    job_id: Optional[int] = None

@app.patch("/applications/{candidate_id}")
def update_application(
    candidate_id: str = Path(...),
    updates: UpdateApplication = Body(...)
):
    update_data = updates.dict(exclude_unset=True)

    # Check that exactly one field is being updated
    if len(update_data) != 1:
        raise HTTPException(
            status_code=400,
            detail="Request body must contain exactly one field: either 'email' or 'job_id'."
        )

    # Mock DB check
    if candidate_id not in applications_db:
        raise HTTPException(status_code=404, detail="Candidate not found.")

    # Update the specific field
    applications_db[candidate_id].update(update_data)

    updated_field = list(update_data.keys())[0]
    return {
        "message": f"Updated {updated_field} successfully.",
        "updated": update_data
    }


# DELETE /applications/{candidate_id}
# Return:
# {
#   "status": "success",
#   "message": "Application for abc123 has been deleted"
# }

from fastapi import FastAPI, HTTPException

app = FastAPI()

# Fake in-memory "database"
applications_db = {
    "abc123": {"email": "user@example.com", "job_id": 101},
    "def456": {"email": "jane@example.com", "job_id": 102}
}

@app.delete("/applications/{candidate_id}")
def delete_application(candidate_id: str):
    if candidate_id not in applications_db:
        raise HTTPException(status_code=404, detail="Application not found")

    # Delete the application
    del applications_db[candidate_id]

    return {
        "status": "success",
        "message": f"Application for {candidate_id} has been deleted"
    }
