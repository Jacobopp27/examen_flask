from flask_app.config.mysqlconnection import connectToMySQL
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
from flask import flash


class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def save(cls, formulario):
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s , %(email)s , %(password)s)"
        result = connectToMySQL('examen').query_db(query , formulario)
        return result

    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL('examen').query_db(query,data)
        if len(results)<1:
            return False
        else:
            user= cls(results[0])
            return user

    @classmethod
    def get_by_id(cls, formulario):
        query = "SELECT * FROM users WHERE id= %(id)s"
        result= connectToMySQL('examen').query_db(query,formulario)
        user = cls(result[0])
        return user

    @classmethod 
    def get_all(cls):
        query = "SELECT * FROM users"
        result= connectToMySQL('examen').query_db(query)
        users = []
        for user in result:
            users.append(cls(user))
        return users



    @staticmethod
    def valida_usuario(formulario):
        es_valido = True
        if len(formulario['first_name']) < 2:
            flash('Nombre debe tener al menos 2 caracteres', 'registro')
            es_valido = False

        if len(formulario['last_name']) < 2:
            flash('Apellido debe tener al menos 2 caracteres', 'registro')
            es_valido = False

        if not EMAIL_REGEX.match(formulario['email']):
            flash('Email invalido', 'registro')
            es_valido = False

        if len(formulario['password']) < 8:
            flash('Contraseña debe tener al menos 8 caracteres', 'registro')
            es_valido = False
        
        if formulario['password'] != formulario['confirm']:
            flash('Contraseñas no coinciden', 'registro')
            es_valido = False

        query = "SELECT * FROM users WHERE email = %(email)s"
        results = connectToMySQL('examen').query_db(query , formulario)
        if len(results) >= 1:
            flash('Email registrado previamente', 'registro')
            es_valido = False

        return es_valido