from fastapi import FastAPI

app = FastAPI(title="SafeSpace API")


@app.get("/")
async def root():
    return {"Hello World!"}
