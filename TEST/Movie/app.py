from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
import sqlite3, threading, time, os, json
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'secretkey'


def create_database():
    conn = sqlite3.connect('Movie.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS MOVIE (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            MOVIE_NAME TEXT NOT NULL,
            GENRE TEXT NOT NULL, 
            DIRECTORS_NAME TEXT NOT NULL,  
            DATE_RELEASE TEXT NOT NULL,
            DATE_STARTED TEXT NOT NULL,
            MOVIE_BUDGET TEXT NOT NULL
        )
    ''')

    conn.commit()
    conn.close()




def get_db_connection():
    conn = sqlite3.connect('Movie.db')
    conn.row_factory = sqlite3.Row  
    return conn


@app.route('/')
def homepage():
    
    conn = sqlite3.connect('Movie.db')
    cursor = conn.cursor()
    movies = cursor.execute('SELECT * FROM MOVIE').fetchall()
    conn.close()
    return render_template('homepage.html',movies=movies)

@app.route('/ADD_MOVIE', methods=['POST'])
def ADD_MOVIE():

        MOVIE_NAME = request.form['MOVIE_NAME']
        GENRE = request.form['GENRE']
        DIRECTORS_NAME = request.form['DIRECTORS_NAME']
        DATE_RELEASE =  request.form['DATE_RELEASE']
        DATE_STARTED = request.form['DATE_STARTED']
        MOVIE_BUDGET = request.form['MOVIE_BUDGET']

        conn = get_db_connection()
        cursor = conn.cursor()

        try:
            cursor.execute(''' 
                INSERT INTO MOVIE (MOVIE_NAME, GENRE, DIRECTORS_NAME, DATE_RELEASE, DATE_STARTED, MOVIE_BUDGET )
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (MOVIE_NAME, GENRE, DIRECTORS_NAME, DATE_RELEASE, DATE_STARTED, MOVIE_BUDGET))
            conn.commit()
            print("Movie Added Successfuly!")

        except Exception as e:
            flash(f"Error adding news: {str(e)}", "error")
        finally:
            conn.close()

        return redirect(url_for('homepage'))


@app.route('/UPDATE_MOVIE/<int:id>', methods=['POST'])
def UPDATE_MOVIE(id):
    MOVIE_NAME = request.form['MOVIE_NAME']
    GENRE = request.form['GENRE']
    DIRECTORS_NAME = request.form['DIRECTORS_NAME']
    DATE_RELEASE = request.form['DATE_RELEASE']
    DATE_STARTED = request.form['DATE_STARTED']
    MOVIE_BUDGET = request.form['MOVIE_BUDGET']

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(''' 
            UPDATE MOVIE 
            SET MOVIE_NAME = ?, GENRE = ?, DIRECTORS_NAME = ?, DATE_RELEASE = ?, DATE_STARTED = ?, MOVIE_BUDGET = ?
            WHERE id = ?
        ''', (MOVIE_NAME, GENRE, DIRECTORS_NAME, DATE_RELEASE, DATE_STARTED, MOVIE_BUDGET, id))
        conn.commit()
        print("MOVIE UPDATED SUCCESSFULLY!")

    except Exception as e:
        flash(f"Error updating movie: {str(e)}", "error")
    finally:
        conn.close()

    return redirect(url_for('homepage'))


@app.route('/EDIT_MOVIE/<int:id>', methods=['GET'])
def EDIT_MOVIE(id):
    conn = get_db_connection()
    movie = conn.execute('SELECT * FROM MOVIE WHERE id = ?', (id,)).fetchone()
    conn.close()
    return render_template('edit_movie.html', movie=movie)


@app.route('/DELETE_MOVIE/<int:id>', methods=['POST'])
def DELETE_MOVIE(id):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute('DELETE FROM MOVIE WHERE id = ?', (id,))
        conn.commit()
        print("MOVIE DELETED SUCCESSFULLY!")
    except Exception as e:
        print(f"Error deleting movie: {str(e)}", "error")
    finally:
        conn.close()

    return redirect(url_for('homepage'))



if __name__ == '__main__':
    create_database()
    app.run(debug=True)
