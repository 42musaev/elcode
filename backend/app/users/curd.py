from passlib.context import CryptContext

from app.base.base_crud import BaseCrud
from app.users import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserCrud(BaseCrud):
    model = User
