from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def home():
    return {"message": "Welcome to Weather Intelligence Dashboard"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}
