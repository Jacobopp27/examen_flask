from flask import render_template, redirect, session, request, flash
from flask_app import app
from flask_app.models.users import User
from flask_app.models.appointments import Appointment
from datetime import datetime, date, time

@app.route('/new/appointment')
def new():
    if 'user_id' not in session: 
        return redirect('/')

    formulario = {
        "id": session['user_id']
    }
    user = User.get_by_id(formulario)
    hoy = datetime.today()
    return render_template('new.html', user=user, hoy=hoy)

@app.route('/create/appointment', methods=['POST'])
def create_appointment():
    if 'user_id' not in session:  
        return redirect('/')

    if not Appointment.valida_cita(request.form):
        return redirect('/new/appointment')

    Appointment.save(request.form)
    return redirect('/dashboard')


@app.route('/edit/appointment/<int:id>') 
def edit_appointment(id):
    if 'user_id' not in session: 
        return redirect('/')
    
    formulario = {
        "id": session['user_id']
    }

    user = User.get_by_id(formulario)
    formulario_receta = { "id": id }

    appointment = Appointment.get_by_id(formulario_receta)

    return render_template('edit.html', user=user, appointment=appointment)

@app.route('/update/appointment', methods=['POST'])
def update_appointment():
    if 'user_id' not in session:
        return redirect('/')
    
    if not Appointment.valida_cita(request.form):
        return redirect('/edit/appointment/'+request.form['id']) 

    Appointment.update(request.form)

    return redirect('/dashboard')

@app.route('/delete/appointment/<int:id>')
def delete_appointment(id):
    if 'user_id' not in session:  
        return redirect('/')
    
    formulario = {"id": id}
    Appointment.delete(formulario)

    return redirect('/dashboard')