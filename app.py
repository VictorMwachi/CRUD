from flask import Flask, render_template,request,redirect,flash,url_for
from flask_sqlalchemy import SQLAlchemy
import psycopg2

app = Flask(__name__)
app.config['SECRET_KEY']="dev"
#app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///crud.db"
app.config['SQLALCHEMY_DATABASE_URI']="postgresql+psycopg2://victor:7mudaki@localhost:5432/crud"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

db=SQLAlchemy(app)

class Employee(db.Model):
   # __tablename__ = "employees"
    id=db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(25),nullable=False)
    last_name= db.Column(db.String(25),nullable=False)
    email = db.Column(db.String(100),nullable=False,unique=True)
    date_of_birth = db.Column(db.Date, nullable=False)

    def __init__(self,first_name,last_name,email,date_of_birth):
        self.first_name=first_name
        self.last_name=last_name
        self.email=email
        self.date_of_birth=date_of_birth
with app.app_context():
    db.create_all()

@app.route('/update', methods=['POST','GET'], strict_slashes=False)
def update():
    if request.method=='POST':
        my_data = Employee.query.get(request.form.get("id"))
        my_data.first_name=request.form["fname"]
        my_data.last_name=request.form["lname"]
        my_data.email=request.form["email"]
        my_data.date_of_birth=request.form["dob"]
    try:
        db.session.add(my_data)
        db.session.commit()
        flash(f"Employee {my_data.first_name} {my_data.last_name} updated succesfully")
        return redirect(url_for('index'))
    except:
        flash("error not edited")
        return redirect(url_for('index'))

@app.route('/',strict_slashes=False)
def index():
    all_data = Employee.query.all()
    return render_template('index.html', employees=all_data)

@app.route('/delete/<int:id>/', methods=['GET','POST'] ,strict_slashes=False)
def delete(id):
    my_data=Employee.query.get(id)
    db.session.delete(my_data)
    db.session.commit()
    flash("Deleted successfully")
    return redirect(url_for('index'))


@app.route('/insert',methods=['POST'],strict_slashes=False)
def insert():
    if request.method=='POST':
        first_name=request.form["fname"]
        last_name=request.form["lname"]
        email=request.form["email"]
        date_of_birth=request.form["dob"]
    try:
        employee=Employee(first_name,last_name,email,date_of_birth)
        db.session.add(employee)
        db.session.commit()
        flash(f"Employee {first_name} {last_name} added succesfully")
        return redirect(url_for('index'))
    except:
        flash("error not added")
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
