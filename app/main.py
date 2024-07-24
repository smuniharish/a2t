from app.imports import FastAPI,uvicorn,CORSMiddleware
from app.middlewares import ProcessTimeMiddleware
from app.controllers import audio_router


app = FastAPI(
    title = "Audio to Text Conversion Server",
    summary = "Audio to Text Conversion Summary",
    description = "Audio to Text Conversion Description",
    version="0.0.1"
)

app.add_middleware(CORSMiddleware)

app.add_middleware(ProcessTimeMiddleware)

app.include_router(audio_router)

@app.get("/")
async def read_root():
    return {"message":"Server is up and running"}

if __name__ == "__main__":
    config = uvicorn.Config("app.main:app", port=3030, log_level="info",reload=True)
    server = uvicorn.Server(config)
    server.run()