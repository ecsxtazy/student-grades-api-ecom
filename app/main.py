from fastapi import FastAPI

app = FastAPI(title="Student Grades Service")

@app.get("/health")
async def health():
    return {"status": "ok"}