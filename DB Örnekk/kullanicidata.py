import sqlite3 as sql
# from kayit import *

def create_table():
    conn = sql.connect('kullanici.db')
    cursor = conn.cursor()

    cursor.execute("""create table if not exists users(
        id integer primary key,
        isim text,
        soyisim text,
        parola text, 
        email text,
        adres text,
        telefon text,
        cinsiyet text
    )""")
    conn.commit()
    conn.close()

def insert(isim, soyisim, parola, email, adres, telefon, cinsiyet):
    conn = sql.connect('kullanici.db')
    cursor = conn.cursor()

    add_command = """INSERT INTO users(isim, soyisim, parola, email, adres, telefon, cinsiyet) values(?, ?, ?, ?, ?, ?, ?)"""
    data = (isim, soyisim, parola, email, adres, telefon, cinsiyet)

    cursor.execute(add_command, data)

    conn.commit()
    conn.close()

def update_password(email, newParola):
    conn = sql.connect('kullanici.db')
    cursor = conn.cursor()

    upd_command = """update users set parola = '{}' where email = '{}' """
    cursor.execute(upd_command.format(newParola, email))

    conn.commit()
    conn.close()

def delete_account(email):
    conn = sql.connect('kullanici.db')
    cursor = conn.cursor()

    dlt_command = """delete from users where email = '{}' """
    cursor.execute(dlt_command.format(email))

    conn.commit()
    conn.close()

def delete_table():
    conn = sql.connect('kullanici.db')
    cursor = conn.cursor()

    cursor.execute("""drop table users """)

    conn.commit()
    conn.close()