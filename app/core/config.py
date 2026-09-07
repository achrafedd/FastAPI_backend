from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config =  SettingsConfigDict(
            env_file='.env'
            )
    PROJECT_NAME: str
    ENVIRONMENT: str = "dev"
    DATABASE_URL: str
    REDIS_URL: str
    ACCESS_TOKEN_EXPIRE_MINUTES: str

if __name__ == '__main__':
    settings = Settings()
    print(settings)
