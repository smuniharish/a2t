from imports import BaseSettings

class Settings(BaseSettings):
    logging_level:str = "INFO"

settings = Settings()