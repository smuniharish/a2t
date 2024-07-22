from imports import APIRouter,File,UploadFile
from app.utilities.audio import transcribe_audio

audio_router = APIRouter(prefix="/audio")

@audio_router.post("/",summary="audio to text conversion endpoint")
async def root(audio_file:UploadFile = File(...)):
    transcription = transcribe_audio(audio_file)
    return {"message":transcription}