from flask import render_template, redirect, session, request, flash
from flask_app import app
from flask_app.models.users import User
from flask_app.models.appointments import Appointment
from flask_bcrypt import Bcrypt        
bcrypt = Bcrypt(app)



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/logout', methods=['POST'])
def home():
    session.clear()
    return redirect('/')

@app.route('/register', methods=['POST'])
def register():
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    print(pw_hash)

    data = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password" : pw_hash 
    }
    if not User.valida_usuario(request.form):
        return redirect('/')
    
    id = User.save(data)

    session['user_id'] = id
    return redirect('/dashboard')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/')

    formulario = {
        "id": session['user_id']
    }
    user = User.get_by_id(formulario)
    users = User.get_all()
    appointments=Appointment.get_all()


    return render_template('dashboard.html', user = user, users=users, appointments=appointments)

@app.route('/login', methods=['POST'])
def login():
    data = { "email" : request.form["email"] }
    user_in_db = User.get_by_email(data)
    if not user_in_db:
        flash("Email o Contraseña incorrectos", "login")
        return redirect("/")

    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash("Email o Contraseña incorrectos", "login")
        return redirect('/')
    session['user_id'] = user_in_db.id
    return redirect('/dashboard')