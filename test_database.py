import time
from sqlalchemy import Column, String, create_engine, Date, DateTime, Integer
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import mysql.connector



# 创建对象的基类:
Base = declarative_base()

class User(Base):
    __tablename__ = 'User'

    id = Column(Integer, primary_key=True)
    username = Column(String(20), nullable=False)
    password = Column(String(128), nullable=False)
    telephone = Column(String(50))
    email = Column(String(50))

# 初始化数据库连接:
engine = create_engine(
    'mysql+mysqlconnector://EasyCharge:XKThZNNwdTW7CMyy@localhost:3306/easycharge')
# 创建DBSession类型:
DBSession = sessionmaker(bind=engine)
session = DBSession()
tmp = session.query(User).group_by(User.telephone).all()
for i in tmp:
    print(i.id,i.username,i.telephone)