from tkinter import *
import sqlite3

status_label = None

# Rest of the code...

def main():
    global status_label
    # Rest of the code...
def create_table():
    conn = sqlite3.connect('company.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS employees 
        (id INTEGER PRIMARY KEY AUTOINCREMENT, 
        fio TEXT, 
        phone TEXT, 
        email TEXT, 
        salary REAL)''')
    conn.commit()
    conn.close()
 
def add_employee():
    fio = name_entry.get()
    phone = phone_entry.get()
    email = email_entry.get()
    salary = float(salary_entry.get())
 
    conn = sqlite3.connect('company.db')
    c = conn.cursor()
    c.execute("INSERT INTO employees (fio, phone, email, salary) VALUES (?, ?, ?, ?)", (fio, phone, email, salary))
    conn.commit()
    conn.close()
    employees_list.insert(END, fio)
    clear_entries()
    status_label.config(text="Сотрудник успешно добавлен")
 
def edit_employee():
    selected_employee = employees_list.curselection()
    if len(selected_employee) > 0:
        index = selected_employee[0]
        employee_id = employees_data[index][0]
        fio = name_entry.get()
        phone = phone_entry.get()
        email = email_entry.get()
        salary = float(salary_entry.get())
 
        conn = sqlite3.connect('company.db')
        c = conn.cursor()
        c.execute("UPDATE employees SET fio = ?, phone = ?, email = ?, salary = ? WHERE id = ?", 
                  (fio, phone, email, salary, employee_id))
        conn.commit()
        conn.close()
        employees_list.delete(index)
        employees_list.insert(index, fio)
        clear_entries()
        status_label.config(text="Сотрудник успешно изменен")
    else:
        status_label.config(text="Сначала выберите сотрудника для изменения")
 
def delete_employee():
    selected_employee = employees_list.curselection()
    if len(selected_employee) > 0:
        index = selected_employee[0]
        employee_id = employees_data[index][0]
 
        conn = sqlite3.connect('company.db')
        c = conn.cursor()
        c.execute("DELETE FROM employees WHERE id = ?", (employee_id,))
        conn.commit()
        conn.close()
        employees_list.delete(index)
        clear_entries()
        status_label.config(text="Сотрудник успешно удален")
    else:
        status_label.config(text="Сначала выберите сотрудника для удаления")
 
def search_employee():
    fio = search_entry.get()
 
    conn = sqlite3.connect('company.db')
    c = conn.cursor()
    c.execute("SELECT * FROM employees WHERE fio = ?", (fio,))
    employee = c.fetchone()
    conn.close()
 
    if employee is not None:
        clear_entries()
        name_entry.insert(END, employee[1])
        phone_entry.insert(END, employee[2])
        email_entry.insert(END, employee[3])
        salary_entry.insert(END, employee[4])
        status_label.config(text="")
    else:
        clear_entries()
        status_label.config(text="Сотрудник с таким ФИО не найден")
 
def clear_entries():
    name_entry.delete(0, END)
    phone_entry.delete(0, END)
    email_entry.delete(0, END)
    salary_entry.delete(0, END)
 
def update_selection(event):
    selected_employee = employees_list.curselection()
    if len(selected_employee) > 0:
        index = selected_employee[0]
        employee_id = employees_data[index][0]
 
        conn = sqlite3.connect('company.db')
        c = conn.cursor()
        c.execute("SELECT * FROM employees WHERE id = ?", (employee_id,))
        employee = c.fetchone()
        conn.close()
 
        clear_entries()
        name_entry.insert(END, employee[1])
        phone_entry.insert(END, employee[2])
        email_entry.insert(END, employee[3])
        salary_entry.insert(END, employee[4])
        status_label.config(text="")
    else:
        clear_entries()
        status_label.config(text="Сначала выберите сотрудника")
 
def main():
    create_table()
 
    global employees_list, employees_data, name_entry, phone_entry, email_entry, salary_entry, search_entry, status_label
 
    window = Tk()
    window.title("Управление сотрудниками")
 
    frame = Frame(window)
    frame.pack(padx=10, pady=10)
 
    lbl_name = Label(frame, text="ФИО:")
    lbl_name.grid(row=0, column=0, sticky=W)
    name_entry = Entry(frame)
    name_entry.grid(row=0, column=1)
 
    lbl_phone = Label(frame, text="Телефон:")
    lbl_phone.grid(row=1, column=0, sticky=W)
    phone_entry = Entry(frame)
    phone_entry.grid(row=1, column=1)
 
    lbl_email = Label(frame, text="Email:")
    lbl_email.grid(row=2, column=0, sticky=W)
    email_entry = Entry(frame)
    email_entry.grid(row=2, column=1)
 
    lbl_salary = Label(frame, text="Зарплата:")
    lbl_salary.grid(row=3, column=0, sticky=W)
    salary_entry = Entry(frame)
    salary_entry.grid(row=3, column=1)
 
    frame_buttons = Frame(window)
    frame_buttons.pack(pady=10)
 
    add_button = Button(frame_buttons, text="Добавить", command=add_employee)
    add_button.pack(side=LEFT)
    edit_button = Button(frame_buttons, text="Изменить", command=edit_employee)
    edit_button.pack(side=LEFT)
    delete_button = Button(frame_buttons, text="Удалить", command=delete_employee)
    delete_button.pack(side=LEFT)
 
    frame_search = Frame(window)
    frame_search.pack(pady=10)
 
    lbl_search = Label(frame_search, text="Поиск по ФИО:")
    lbl_search.pack(side=LEFT)
    search_entry = Entry(frame_search)
    search_entry.pack(side=LEFT)
    search_button = Button(frame_search, text="Найти", command=search_employee)
    search_button.pack(side=LEFT)
 
    frame_employee_list = Frame(window)
    frame_employee_list.pack(pady=10)
 
    scrollbar = Scrollbar(frame_employee_list)
    scrollbar.pack(side=RIGHT, fill=Y)
 
    employees_list = Listbox(frame_employee_list, width=50, yscrollcommand=scrollbar.set)
    employees_list.pack(side=LEFT, fill=BOTH)
    scrollbar.config(command=employees_list.yview)
 
    employees_list.bind('<<ListboxSelect>>', update_selection)
 
    conn = sqlite3.connect('company.db')
    c = conn.cursor()
    c.execute("SELECT * FROM employees")
    employees_data = c.fetchall()
    conn.close()
 
    for employee in employees_data:
        employees_list.insert(END, employee[1])
 
    status_label = Label(window, text="", fg="red")
    status_label.pack()
 
    window.mainloop()
 
if __name__ == "__main__":
    main()