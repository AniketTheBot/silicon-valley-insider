from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # These match the keys in your .env file
    NEO4J_URI: str
    NEO4J_USERNAME: str
    NEO4J_PASSWORD: str
    GROQ_API_KEY: str

    class Config:
        env_file = ".env"
        # This allows the .env file to be in the current folder or parent folder
        extra = "ignore" 

settings = Settings()