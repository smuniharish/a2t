from imports import AutoModelForSpeechSeq2Seq,AutoProcessor,torch,is_torch_sdpa_available
from utilities.logger import logger

cudaIsAvailable = torch.cuda.is_available()
spdaIsAvailable = is_torch_sdpa_available()
logger.info("Is sdpa available {spdaIsAvailable}".format(spdaIsAvailable=spdaIsAvailable))
logger.info("Is cuda available {cudaIsAvailable}".format(cudaIsAvailable=cudaIsAvailable))
torch_device = "cuda:0" if cudaIsAvailable else "cpu"
torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32

audio2Text_model_id = "openai/whisper-large-v3"
if(spdaIsAvailable):
    audio2Text_model = AutoModelForSpeechSeq2Seq.from_pretrained(audio2Text_model_id, torch_dtype=torch_dtype, low_cpu_mem_usage=True, use_safetensors=True,attn_implementation="sdpa")
else:
    audio2Text_model = AutoModelForSpeechSeq2Seq.from_pretrained(audio2Text_model_id, torch_dtype=torch_dtype, low_cpu_mem_usage=True, use_safetensors=True)
audio2Text_model.to(torch_device)
audio2Text_processor = AutoProcessor.from_pretrained(audio2Text_model_id)
audio2Text_torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32