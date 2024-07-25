import data.decorators
from flask import Flask, render_template, request, redirect, url_for, flash, session, abort
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import data


app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///site.db'
app.config['SECRET_KEY'] = 'aa2'

engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
Base = declarative_base()
Session = sessionmaker(bind=engine) 

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String(20), unique = True, nullable=False)
    password = Column(String(150),nullable=False)
    city = Column(String(100), nullable=False)

Base.metadata.create_all(engine)
session_db = Session()




class Owners(Base):
    __tablename__ = 'owner'
    id = Column(Integer, primary_key=True)
    name = Column(String(20), unique = True, nullable=False)
    price = Column(String(150),nullable=False)
    city = Column(String(100), nullable=False)


Base.metadata.create_all(engine)
session_db = Session()





class Apartment(Base):
    __tablename__ = 'apartment'
    id = Column(Integer, primary_key=True)
    address = Column(String(120), unique = True, nullable=False)
    room = Column(Integer,nullable=False)
    area = Column(Integer, nullable=False)

Base.metadata.create_all(engine)
session_db = Session()




class Order(Base):
    __tablename__ = 'order'
    id = Column(Integer, primary_key=True)
    apartment_id = Column(Integer, ForeignKey("apartment.id", ondelete="CASCADE"))
    startday = Column(Integer,nullable=False)
    lastday = Column(Integer, nullable=False)


Base.metadata.create_all(engine)
session_db = Session()



# @login.user_loader
# def load_user(id):
#     return User.query.get(int(id))


@app.route('/')
def home():
    users = session_db.query(User).all()
    owners = session_db.query(Owners).all()
    apartments = session_db.query(Apartment).all()
    orders = session_db.query(Order).all()
    return render_template("index.html", users=users)
    return render_template("index.html", orders=orders)
    return render_template("index.html", owners=owners)
    return render_template("index.html", apartments=apartments)



@app.route('/register/',  methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        city = request.form['city']
        user = User(username=username, password=password, city=city)
        session_db.add(user)
        session_db.commit()
        return redirect(url_for('home'))
    return render_template("register.html")


@app.route('/owner_reg/', methods=['POST', 'GET'])
def owner_reg():
    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']
        city = request.form['city']
        owner = Owners(name=name, price=price, city=city)
        session_db.add(owner)
        session_db.commit()
        return redirect(url_for('home'))
    return render_template('owner_reg.html')


@app.route('/variant/', methods=['POST', 'GET'])
def variant():
    if request.method == 'POST':
        address = request.form['address']
        room = request.form['room']
        area = request.form['area']
        apartment = Apartment(address=address, room=room, area=area)
        session_db.add(apartment)
        session_db.commit()
        return redirect(url_for('home'))
    return render_template('variant.html') 
    


@app.route('/data_are/', methods=['POST', 'GET'])
def data_are():
    if request.method == 'POST':
        startday = request.form['startday']
        lastday = request.form['lastday']
       
        order = Order(startday=startday, lastday=lastday)
        session_db.add(order)
        session_db.commit()
        return redirect(url_for('home'))
    return render_template('data_are.html')


@app.route('/arenda/', methods=['GET'])
def arenda():

 
    orders = session_db.query(Order).all()
    apartments = session_db.query(Apartment).all()
    return render_template("arenda.html", apartments=apartments, orders=orders)




if __name__ =='__main__':
    app.run(debug=True)