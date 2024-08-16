import sqlite3

connection = sqlite3.connect('not_telegram.db')
cursor = connection.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS Users(
id INTEGER PRIMARY KEY,
username TEXT NOT NULL,
email TEXT NOT NULL,
age INTEGER,
balance INTEGER NOT NULL
)''')

cursor.execute('CREATE INDEX IF NOT EXISTS idx_email ON Users (email)')

age = 0
for i in range(1, 11):
    age += 10
    cursor.execute('INSERT INTO Users(username, email, age, balance) VALUES (?, ?, ?, ?)',
                   (f'user{i}', 'example1@gmail.com', age, '1000'))

for i in range(1, 11):
    if i % 2 != 0:
        cursor.execute('UPDATE Users SET balance = ? WHERE username = ?', (500, f'user{i}'))

num = -2
while num <= 8:
    num += 3
    cursor.execute('DELETE FROM Users WHERE username = ?', (f'user{num}',))

cursor.execute('DELETE FROM Users WHERE id = ?', (6,))

cursor.execute('SELECT COUNT(*) FROM Users')
count_use = cursor.fetchone()[0]
cursor.execute('SELECT SUM(balance) FROM Users')
all_balance = cursor.fetchone()[0]
user = all_balance / count_use
print(user)

# for i in range(1, 11):
#     cursor.execute('DELETE FROM Users WHERE username = ?', (f'user{i}',))

connection.commit()
connection.close()
