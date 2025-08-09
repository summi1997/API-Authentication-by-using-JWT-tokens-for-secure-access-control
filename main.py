from fastapi import FastAPI

app = FastAPI(title="FastAPI Docker AWS")

@app.get("/")
def read_root():
    return {"message": "Welcome to FastAPI with Docker on AWS!"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.post("/doctors")
def create_doctor(doctor: dict):
    return {"message": "Doctor created successfully", "doctor": doctor}