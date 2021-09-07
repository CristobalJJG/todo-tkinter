from os import remove
from sqlite3.dbapi2 import connect
from tkinter import *
import sqlite3

root = Tk()
root.title("To do List")
root.geometry("400x500")

conn = sqlite3.connect("todo.db")
c = conn.cursor()

#todo[id, created_at, description, completed]
c.execute(
    """CREATE TABLE if not EXISTS todo(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        description TEXT NOT NULL,
        completed BOOLEAN NOT NULL
    );"""
)
conn.commit()

def complete(id):
    def _complete():
        print(id)
        todo = c.execute("SELECT * FROM todo WHERE id = ?", (id, )).fetchone()
        c.execute("UPDATE todo SET completed = ? WHERE id = ?", (not todo[3], id))
        conn.commit()
        render_todos(0)
    return _complete

def addTodo():
    todo = e.get()
    if todo:
        c.execute("INSERT INTO todo (description, completed) VALUES (?, ?)", (todo, False))
        conn.commit()
        render_todos(1)
        e.delete(0, END)

def removeTodo(id):
    def _rmTodo():
        c.execute("DELETE FROM todo WHERE id = ?", (id, ))
        conn.commit()
        render_todos(1)
    return _rmTodo

def render_todos(z):
    rows = c.execute("SELECT * FROM todo").fetchall()
    if z: print(rows)

    for widget in f.winfo_children():
        widget.destroy()

    for n in range(0, len(rows)):
        #i = id; comp = completed; desc = description
        i, comp, desc = rows[n][0], rows[n][3], rows[n][2]
        color = "#888888" if comp else "#000000"
        ch = Checkbutton(f, text=desc, width=42, fg=color, anchor="w", command=complete(i))
        ch.select() if comp else ch.deselect()
        ch.grid(row=n, column=0, sticky="w")
        
        color = "#b9b9b9" if comp else "#ffffff"
        btn = Button(f, text = "Eliminar", background=color, command=removeTodo(i))
        btn.grid(row=n, column=1)

l = Label(root, text="Tarea")
l.grid(row=0, column=0)

e = Entry(root, width=40)
e.grid(row=0, column=1)

btn = Button(root, text="Agregar", command=addTodo)
btn.grid(row=0, column=2)

f = LabelFrame(root, text="Mis tareas", padx = 5, pady = 5)
f.grid(row=1, column=0, columnspan=3, sticky="nsew", padx=5)

e.focus()
root.bind("<Return>", lambda x:addTodo())
render_todos(1)
root.mainloop()