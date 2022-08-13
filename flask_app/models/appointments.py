from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from datetime import timedelta,date,datetime


class Appointment:
    def __init__(self, data):
        self.id = data['id']
        self.task = data['task']
        self.date = data['date']
        self.status = data['status']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']



    @staticmethod
    def valida_cita(formulario):
        es_valido = True

        if len(formulario['task']) < 1:
            flash("Insert a Task", "task")
            es_valido = False
        
        if formulario['date'] == "":
            flash("Insert a date", "task")
            es_valido = False

        if len(formulario['status']) < 0:
            flash("Insert status", "task")
            es_valido = False
        
        return es_valido

    @classmethod
    def save(cls, formulario):
        query = "INSERT INTO appointments (task, date, status, user_id) VALUES ( %(task)s, %(date)s, %(status)s, %(user_id)s )"
        nuevoId = connectToMySQL('examen').query_db(query, formulario)
        return nuevoId

    @classmethod
    def get_all(cls):
        query = "SELECT appointments.*, first_name FROM appointments LEFT JOIN users ON users.id = appointments.user_id;" 
        results = connectToMySQL('examen').query_db(query) 
        appointments = []
        
        for row in results:
            appointments.append(cls(row)) 
        return appointments

    @classmethod
    def get_by_id(cls, formulario): 
        query = "SELECT appointments.*, first_name FROM appointments LEFT JOIN users ON users.id = appointments.user_id WHERE appointments.id = %(id)s" 
        result = connectToMySQL('examen').query_db(query, formulario) 
        appointment = cls(result[0]) 
        print(result)
        return appointment

    @classmethod
    def update(cls, formulario):
        query = "UPDATE appointments SET task = %(task)s, date = %(date)s, status = %(status)s WHERE id = %(id)s"
        result = connectToMySQL('examen').query_db(query, formulario)
        return result

    @classmethod
    def delete(cls, formulario): 
        query = "DELETE FROM appointments WHERE id = %(id)s"
        result = connectToMySQL('examen').query_db(query, formulario)
        return result