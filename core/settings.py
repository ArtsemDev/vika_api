from pathlib import Path

from passlib.context import CryptContext

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = '34cxyn8n87Bt86rtb*&Bytb76btB^&76v8t&6vr7VB*'
PWD_CONTEXT = CryptContext(schemes=["bcrypt"], deprecated="auto")
ALGORITHM = 'HS256'
EXPIRE_ACCESS_TOKEN = 5
EXPIRE_REFRESH_TOKEN = 15
TOKEN_TYPE = 'Bearer'
HTTP_HEADER = 'Authorization'
