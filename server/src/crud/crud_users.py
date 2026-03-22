from fastcrud import FastCRUD

from ..models.user import User

CRUDUser = FastCRUD(User)
crud_users = CRUDUser(User)
