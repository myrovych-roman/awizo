from app.db.session import engine
from app.models.user import Base as UserBase
from app.models.avization import Base as AvizationBase

def create_tables():
    UserBase.metadata.create_all(bind=engine)
    AvizationBase.metadata.create_all(bind=engine)

if __name__ == "__main__":
    create_tables()
