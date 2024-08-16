import sqlite3

connection = sqlite3.connect('not_telegram.db')
cursor = connection.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS Products(
id INTEGER PRIMARY KEY,
title TEXT NOT NULL,
description TEXT,
price INTEGER NOT NULL
)''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS User(
id INTEGER PRIMARY KEY,
username TEXT NOT NULL,
email TEXT NOT NULL,
age INTEGER,
balance NOT NULL
)''')


def initiate_db(title, description, price):
    check_title = cursor.execute('SELECT * FROM Products WHERE title = ?', (title,))

    if check_title.fetchone() is None:
        cursor.execute(f"INSERT INTO Products (title, description, price)VALUES('{title}', '{description}', '{price}')")
    connection.commit()


initiate_db('протеин', 'изолят', 1000)
initiate_db('креатин', 'моногидрат', 2000)
initiate_db('бцаа', 'аминокислоты', 3000)
initiate_db('гейнер', 'БЖУ', 4000)


def get_all_products(id):
    title_list = cursor.execute('SELECT * FROM Products WHERE id = ?', (id,))
    mess = ''
    for title in title_list:
        mess += f'{title[0]} Название: {title[1]} | Описание: {title[2]} | Цена: {title[3]}\n'
        return mess
    connection.commit()
    connection.close()



def is_included(name):
    check_name = cursor.execute(f'SELECT username FROM User WHERE username = "{name}"')
    if check_name.fetchone() is None:
        #print('такого имени нет')
        return False
    else:
        #print('Пользователь уже существует, введите другое имя')
        return True



def add_user(username, email, age):
    check_title = cursor.execute('SELECT * FROM User WHERE username = ?', (username,))

    if check_title.fetchone() is None:
        cursor.execute(
            f"INSERT INTO User (username, email, age, balance)VALUES ('{username}', '{email}', '{age}', '1000')")
    connection.commit()
    connection.close()
