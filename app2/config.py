from pydantic import BaseSettings


class Settings(BaseSettings):
    db_username: str
    db_passowrd: str
    db_hostname: str
    db_name: str
    db_port: str
    access_token_expire_minutes: int
    secret_key: str
    algorithm: str
    
    class Config:
        env_file = ".env"


settings = Settings()