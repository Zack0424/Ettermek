from flask import Flask, redirect, url_for, render_template,request,session,flash
from datetime import timedelta
from sqlalchemy import create_engine, ForeignKey, Column,String, Integer, CHAR
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker



##################DATABASE


Base = declarative_base()



class User(Base):
    __tablename__ = "users"

    id = Column("id", Integer, primary_key=True)
    email = Column("email", String)
    first_name = Column("firstname", String)
    last_name = Column("lastname", String)
    password = Column("password",String)
    rank = Column("rank",Integer)


    def __init__(self, uid, email, first_name, last_name, password):
        self.id = uid
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.password = password
        self.rank = 0

    def __repr__(self) -> str:
        return f"({self.id}) {self.first_name} {self.last_name}, {self.email} {self.rank}"


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
session2 = Session()


###############ACCOUNT MANAGEMENT################








###############BACKEND##########################










app = Flask(__name__)
app.secret_key = "hello"
app.permanent_session_lifetime = timedelta(days=20)


@app.route("/")
def mainpage():
    return render_template("index.html")

@app.route("/login", methods=['POST', "GET"])
def login():
    session_login = Session()
    if request.method == "POST":
        session.permanent = True
        user = request.form["email_input"]
        pw  = request.form["password_input"]
        x = session_login.query(User).filter(User.email ==user).filter(User.password== pw).first()
        
        if x:
            session["user"] = user
            return redirect(url_for("logged"))
    return render_template("login.html")



@app.route("/register", methods=['POST', "GET"])
def register():
    
    if request.method == "POST":
        first_name = request.form["first_name_input"]
        last_name = request.form["last_name_input"]
        email = request.form["email_input"]
        pw = request.form["password_input"]
        pw_conf = request.form["password_confirmation_input"]
        if first_name =="" and last_name =="" and email ==""and pw == "" and pw_conf =="":
            pass
        
        else:
            if session2.query(User).filter(User.email == email).first():
                flash("Ezzel az emaillel már van fiók regisztrálva!")
            
            else:
                session3 = Session()
                id = len(session3.query(User).all())
                user_registration = User(uid = id,email=email,first_name=first_name, last_name=last_name,password=pw)
                session2.add(user_registration)
                session2.commit()
                session3.close()
                return redirect(url_for("login"))
                
                
    return render_template("register.html")

@app.route("/logout")
def logout():
    if "user" in session:
        session.pop("user")
        return redirect(url_for("mainpage"))
    return redirect(url_for("mainpage"))

@app.route("/logged")
def logged():
    if "user" in session:
        session4 = Session()
        rank= str(session4.query(User.rank).filter(session["user"] == User.email).first())
        rank = int(rank[1])
        session4.close()
        session5 = Session()
        restaurants = session5.query(Restaurant).all()

        session5.close()
        return render_template("logged.html",search=True, name=session["user"], rank=rank, restaurants=restaurants)

@app.route("/addRestaurant", methods=['POST', "GET"])
def add_restaurants():
    session4 = Session()
    rank= str(session4.query(User.rank).filter(session["user"] == User.email).first())
    rank = int(rank[1])
    session4.close()
    if rank>2:
        if request.method=="POST":
            name = request.form["restaurant_name_input"]
            type = request.form["select"]

            if name =="" or type== "":
                pass
                
            else:
                session6= Session()
                id = len(session6.query(Restaurant).all())
                rest = Restaurant(id,name,type)
                session6.add(rest)
                session6.commit()
                return redirect(url_for("logged"))
        
        return render_template("addRestaurant.html")
    return redirect(url_for("logged"))



if __name__ == "__main__":
    app.run(debug=True)