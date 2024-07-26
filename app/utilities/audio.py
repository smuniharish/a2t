from app.imports import NamedTemporaryFile,torchaudio,torch
from . import audio2Text_model,audio2Text_processor,audio2Text_torch_dtype,torch_device
from app.utilities.logger import logger

def transcribe_audio(audio_file):
    with NamedTemporaryFile(delete=False) as temp_audio:
        temp_audio.write(audio_file.file.read())
        temp_audio_path = temp_audio.name
    logger.info("Available backends {availableBackends}".format(availableBackends=torchaudio.list_audio_backends()))
    waveform, sample_rate = torchaudio.load(temp_audio_path)

    # Ensure the audio has the correct sample rate
    if sample_rate != audio2Text_processor.feature_extractor.sampling_rate:
        resampler = torchaudio.transforms.Resample(orig_freq=sample_rate, new_freq=audio2Text_processor.feature_extractor.sampling_rate)
        waveform = resampler(waveform)
        sample_rate = audio2Text_processor.feature_extractor.sampling_rate

    # Process the audio input
    inputs = audio2Text_processor(waveform.squeeze().numpy(), return_tensors="pt", sampling_rate=sample_rate)

    # Move inputs to the appropriate device and data type
    inputs = {key: value.to(torch_device, dtype=audio2Text_torch_dtype) for key, value in inputs.items()}
    generate_kwargs={"task":"translate","max_new_tokens":128}
    with torch.no_grad():
        generated_ids = audio2Text_model.generate(inputs["input_features"],**generate_kwargs)
    transcription = audio2Text_processor.batch_decode(generated_ids, skip_special_tokens=True)
    return transcription[0]
