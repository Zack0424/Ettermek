from sqlalchemy import create_engine, ForeignKey, Column,String, Integer, CHAR
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


Base = declarative_base()




class User(Base):
    __tablename__ = "users"

    id = Column("id", Integer, primary_key=True)
    email = Column("email", String)
    first_name = Column("firstname", String)
    last_name = Column("lastname", String)
    password = Column("password",String)


    def __init__(self, uid, email, first_name, last_name, password):
        self.id = uid
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.password = password

    def __repr__(self) -> str:
        return f"({self.id}) {self.first_name} {self.last_name}, {self.email}"


class Restaurant(Base):
    __tablename__ = "restaurants"

    id = Column("id", Integer, primary_key = True)
    name = Column("name", Integer)
    type = Column("type", String)
    score = Column("score", Integer)

    def __init__(self, id, name, type, score=0):
        self.id = id
        self.name = name
        self.type = type
        self.score = score
    
    def __repr__(self):
        return f"({self.id}) {self.name} {self.type} {self.score}"


class Rest_user_connector(Base):
    __tablename__ = "rest_user_connector"
    cid = Column("connector_id", Integer, primary_key=True)
    rid = Column(Integer, ForeignKey("restaurants.id"))
    uid = Column(Integer, ForeignKey("users.id"))
    score = Column("score",Integer)

    def __init__(self, uid, rid,score):
        self.uid = uid
        self.rid = rid
        self.score = score

    def __repr__(self):
        return f"({self.uid}) - ({self.rid}) {self.score}"




engine = create_engine("sqlite:///mydb.db", echo=True)
Base.metadata.create_all(bind=engine)


Session = sessionmaker(bind=engine)
session = Session()




"""
user1 = User(123,"asd@asd.asd","Zoltán", "Novák","1223")
user2 = User(1233,"asd@asd.afsd","Zoltán", "Novasák","12443")
user3 = User(1243,"asd@asd.awsd","Zasdfoltán", "Nováask","1as23")
user4 = User(1213,"asd@asd.assd","Zoltán", "Noasdvák","12323")

session.add(user1)
session.add(user2)
session.add(user3)
session.add(user4)

session.commit()

rest1 = Restaurant(1,"Paqwe","Pizza")
rest2 = Restaurant(1121,"12Paqwe","Pizza")
rest3 = Restaurant(114,"Paqwe31","Hamburger")
rest4 = Restaurant(131,"Paqwasde","Saláta")

session.add(rest1)
session.add(rest2)
session.add(rest3)
session.add(rest4)
session.commit()

conn = Rest_user_connector(1,1,5)



session.add(conn)
session.commit()
"""
results = session.query(User,Rest_user_connector,Restaurant).filter(User.id == Rest_user_connector.uid).filter(Rest_user_connector.rid == Restaurant.id).all()

for r in results:
    print(r)