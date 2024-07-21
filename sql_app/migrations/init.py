from models import user as User
from models import role as Role
from database import engine

Role.Base.metadata.create_all(bind=engine)
User.Base.metadata.create_all(bind=engine)