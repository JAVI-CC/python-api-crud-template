import json
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from database import engine
from dependencies.hash_password import hash_password
from dependencies.root_dir import ROOT_DIR
from models.user import User as ModelUser
from schemas.user import UserCreateSeeder as SchemaUserCreateSeeder

json_file = open(f"{ROOT_DIR}/seeders/data/users.json")

session = Session(engine)
for user in json.load(json_file):

    user_hashed_password = user["hashed_password"]
    del user["hashed_password"]

    user = SchemaUserCreateSeeder(
        **user, hashed_password=hash_password(user_hashed_password)
    )

    with session as db:
        db_user = ModelUser(**user.model_dump())
        db.add(db_user)
        try:
            db.commit()
        except SQLAlchemyError:
            pass
            # 1062, Duplicate entry

json_file.close()
