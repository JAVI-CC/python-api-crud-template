from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from database import engine
from dependencies.root_dir import ROOT_DIR
from models.role import Role as ModelRole
from schemas.role import RoleCreateSeeder as SchemaRoleCreateSeeder
import json

json_file = open(f"{ROOT_DIR}/seeders/data/roles.json")

session = Session(engine)
for role in json.load(json_file):
    role = SchemaRoleCreateSeeder(**role)
    with session as db:
        db_role = ModelRole(**role.model_dump())
        db.add(db_role)
        try:
            db.commit()
        except SQLAlchemyError:
            pass
            # 1062, Duplicate entry

json_file.close()
