import tkinter as tk
from tkinter import ttk
import sqlite3

# Создание базы данных SQL
conn = sqlite3.connect('employees.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS employees (id INTEGER PRIMARY KEY AUTOINCREMENT,
                                                    name TEXT,
                                                    phone TEXT,
                                                    email TEXT,
                                                    salary INTEGER)''')
conn.commit()

root = tk.Tk()
root.title("Список сотрудников компании")


# Добавление сотрудника
def add_employee():
    name = name_entry.get()
    phone = phone_entry.get()
    email = email_entry.get()
    salary = salary_entry.get()
    c.execute('''INSERT INTO employees (name, phone, email, salary) VALUES (?, ?, ?, ?)''', (name, phone, email, salary))
    conn.commit()

    refresh_table()


# Изменение сотрудника
def update_employee():
    selected_item = tree.selection()
    if selected_item:
        name = name_entry.get()
        phone = phone_entry.get()
        email = email_entry.get()
        salary = salary_entry.get()
        c.execute('''UPDATE employees SET name=?, phone=?, email=?, salary=? WHERE id=?''',
                  (name, phone, email, salary, selected_item[0]))
        conn.commit()

        refresh_table()
    else:
        print("Сотрудник не выбран")


# Удаление сотрудника
def delete_employee():
    selected_item = tree.selection()
    if selected_item:
        item_id = tree.set(selected_item, "#1")
        c.execute('''DELETE FROM employees WHERE id=?''', (item_id,))
        conn.commit()

        refresh_table()
    else:
        print("Сотрудник не выбран")


# Поиск сотрудника
def search_employee():
    search_text = search_entry.get()
    c.execute('''SELECT * FROM employees WHERE name LIKE ?''', ('%' + search_text + '%',))
    rows = c.fetchall()

    tree.delete(*tree.get_children())
    for row in rows:
        tree.insert('', 'end', values=row)


def refresh_table():
    c.execute('''SELECT * FROM employees''')
    rows = c.fetchall()

    tree.delete(*tree.get_children())
    for row in rows:
        tree.insert('', 'end', values=row)


# Создание таблицы
tree = ttk.Treeview(root, columns=['ID', 'ФИО', 'Номер телефона', 'Email', 'Заработная плата'])
tree.heading('ID', text='ID')
tree.heading('ФИО', text='ФИО')
tree.heading('Номер телефона', text='Номер телефона')
tree.heading('Email', text='Email')
tree.heading('Заработная плата', text='Заработная плата')
tree.column('#0', width=0, stretch=tk.NO)
tree.column('ID', width=50, anchor=tk.CENTER)
tree.column('ФИО', width=150, anchor=tk.W)
tree.column('Номер телефона', width=150, anchor=tk.W)
tree.column('Email', width=200, anchor=tk.W)
tree.column('Заработная плата', width=100, anchor=tk.E)
tree.pack(pady=10)


# Фрейм для полей ввода
entry_frame = tk.Frame(root)
entry_frame.pack()

# Поля для ввода
name_label = tk.Label(entry_frame, text="ФИО:")
name_label.grid(row=0, column=0)
name_entry = tk.Entry(entry_frame)
name_entry.grid(row=0, column=1)

phone_label = tk.Label(entry_frame, text="Номер телефона:")
phone_label.grid(row=1, column=0)
phone_entry = tk.Entry(entry_frame)
phone_entry.grid(row=1, column=1)

email_label = tk.Label(entry_frame, text="Email:")


email_label.grid(row=2, column=0)
email_entry = tk.Entry(entry_frame)
email_entry.grid(row=2, column=1)

salary_label = tk.Label(entry_frame, text="Заработная плата:")
salary_label.grid(row=3, column=0)
salary_entry = tk.Entry(entry_frame)
salary_entry.grid(row=3, column=1)


# Кнопки
add_button = tk.Button(root, text="Добавить сотрудника", command=add_employee)
add_button.pack(pady=5)

update_button = tk.Button(root, text="Изменить сотрудника", command=update_employee)
update_button.pack(pady=5)

delete_button = tk.Button(root, text="Удалить сотрудника", command=delete_employee)
delete_button.pack(pady=5)


# Фрейм для поиска
search_frame = tk.Frame(root)
search_frame.pack(pady=10)

search_label = tk.Label(search_frame, text="Поиск:")
search_label.pack(side=tk.LEFT)

search_entry = tk.Entry(search_frame)
search_entry.pack(side=tk.LEFT)

search_button = tk.Button(search_frame, text="Найти", command=search_employee)
search_button.pack(side=tk.LEFT)


# Запуск приложения
refresh_table()
root.mainloop()
