from dotenv import load_dotenv
import os
from pathlib import Path

root = Path(__file__).parent
env_path = root / ".env"
if env_path.exists():
    load_dotenv(env_path)

import uvicorn

if __name__ == "__main__":
    uvicorn.run("src.main:app", host="127.0.0.1", port=8001, reload=False)
