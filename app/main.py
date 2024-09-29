from fastapi import FastAPI
from app.api import users,jobs


app = FastAPI(title="StudentJobs")


app.include_router(users.router)
#app.include_router(jobs.router)




@app.get("/")
def read_root():
    return {"message": "Welcome to the Job Search Platform!"}