from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base




SQLALCHEMY_DATABASE_URL = "postgresql://escemavp:4_N5QwWlyYCyWNE3Z6JEJD14wcRY9j1C@balarama.db.elephantsql.com/escemavp"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)


# # Using sqlite3
# SQLALCHEMY_DATABASE_URL = "sqlite:///./todos.db"

# engine = create_engine(
#     SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
# )



# # MYSQL Series
# SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:test1234!@127.0.0.1:3306/todoapp"

# # MYSQL Series
# engine = create_engine(
#     SQLALCHEMY_DATABASE_URL
# )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
