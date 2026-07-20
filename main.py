from fastapi import FastAPI

app = FastAPI(title="Training Copilot API")

@app.get("/")
def read_root():
    """
    A simple root endpoint to verify our server is alive.
    """
    return {"status": "training-copilot API is running"}