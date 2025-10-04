from dotenv import load_dotenv
import uvicorn

from app.infrastructure.configs.fastapi_config import application

load_dotenv()

if __name__ == '__main__':
    uvicorn.run(application, port=8085)



