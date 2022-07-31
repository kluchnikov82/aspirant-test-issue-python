"""Настройки для подключения к базе PostgreSQL"""

class Settings:
    POSTGRES_USER: str = 'postgres'
    # POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
    POSTGRES_SERVER: str = '127.0.0.1'
    POSTGRES_PORT: str = '5432' # default postgres port is 5432
    POSTGRES_DB: str = 'postgres'
    DATABASE_URL = f"postgresql://{POSTGRES_USER}:@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"


settings = Settings()
