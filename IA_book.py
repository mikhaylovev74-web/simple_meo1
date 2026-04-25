import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

DATA_FILE = "books.json"
books = []

def load_books():
    global books
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            try:
                books = json.load(f)
            except json.JSONDecodeError:
                books = []
                messagebox.showwarning("Ошибка", "Файл JSON повреждён. Создан новый список.")
    else:
        books = []

def save_books():
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(books, f, ensure_ascii=False, indent=4)
    messagebox.showinfo("Успех", f"Данные сохранены в {DATA_FILE}")

def add_book():
    title = title_entry.get().strip()
    author = author_entry.get().strip()
    genre = genre_entry.get().strip()
    pages = pages_entry.get().strip()

    if not title or not author or not genre or not pages:
        messagebox.showerror("Ошибка", "Все поля должны быть заполнены!")
        return

    if not pages.isdigit():
        messagebox.showerror("Ошибка", "Количество страниц должно быть числом!")
        return

    book = {"title": title, "author": author, "genre": genre, "pages": int(pages)}
    books.append(book)
    update_tree()
    clear_entries()

def clear_entries():
    title_entry.delete(0, tk.END)
    author_entry.delete(0, tk.END)
    genre_entry.delete(0, tk.END)
    pages_entry.delete(0, tk.END)

def update_tree():
    for i in tree.get_children():
        tree.delete(i)
    for book in books:
        tree.insert("", tk.END, values=(book["title"], book["author"], book["genre"], book["pages"]))

def filter_books():
    genre_filter = filter_genre.get().strip().lower()
    try:
        pages_filter = int(filter_pages.get().strip())
        has_pages_filter = True
    except:
        pages_filter = 0
        has_pages_filter = False

    for i in tree.get_children():
        tree.delete(i)

    for book in books:
        match_genre = genre_filter == "" or genre_filter in book["genre"].lower()
        match_pages = not has_pages_filter or book["pages"] > pages_filter

        if match_genre and match_pages:
            tree.insert("", tk.END, values=(book["title"], book["author"], book["genre"], book["pages"]))


# --- Основное окно ---
root = tk.Tk()
root.title("Book Tracker")
root.geometry("700x500")

frame = ttk.Frame(root, padding=10)
frame.pack(fill=tk.BOTH, expand=True)

# Поля ввода
ttk.Label(frame, text="Название:").grid(row=0, column=0, sticky=tk.W)
title_entry = ttk.Entry(frame, width=30)
title_entry.grid(row=0, column=1, columnspan=2, sticky=tk.W)

ttk.Label(frame, text="Автор:").grid(row=1, column=0, sticky=tk.W)
author_entry = ttk.Entry(frame, width=30)
author_entry.grid(row=1, column=1, columnspan=2, sticky=tk.W)

ttk.Label(frame, text="Жанр:").grid(row=2, column=0, sticky=tk.W)
genre_entry = ttk.Entry(frame, width=30)
genre_entry.grid(row=2, column=1, columnspan=2, sticky=tk.W)

ttk.Label(frame, text="Страниц:").grid(row=3, column=0, sticky=tk.W)
pages_entry = ttk.Entry(frame, width=10)
pages_entry.grid(row=3, column=1, sticky=tk.W)

# Кнопка добавления книги
ttk.Button(frame, text="Добавить книгу", command=add_book).grid(row=4, column=0, columnspan=3)

# Фильтры
ttk.Label(frame, text="Фильтр по жанру:").grid(row=5, column=0, sticky=tk.W)
filter_genre = ttk.Entry(frame, width=20)
filter_genre.grid(row=5, column=1, sticky=tk.W)
ttk.Button(frame, text="Фильтровать", command=filter_books).grid(row=5, column=2)

ttk.Label(frame, text="Страниц >").grid(row=6, column=0, sticky=tk.W)
filter_pages = ttk.Entry(frame, width=10)
filter_pages.grid(row=6, column=1, sticky=tk.W)
ttk.Button(frame, text="Фильтровать", command=filter_books).grid(row=6, column=2)

# Таблица книг
tree = ttk.Treeview(frame, columns=("title", "author", "genre", "pages"), show='headings')
tree.heading("title", text="Название")
tree.heading("author", text="Автор")
tree.heading("genre", text="Жанр")
tree.heading("pages", text="Страниц")
tree.grid(row=7, column=0, columnspan=3, pady=10, sticky="nsew")

# Кнопки сохранения/загрузки
ttk.Button(frame, text="Сохранить в JSON", command=save_books).grid(row=8, column=0)
ttk.Button(frame, text="Загрузить из JSON", command=lambda: [load_books(), update_tree()]).grid(row=8, column=1)

# Настройка сетки для растягивания
frame.grid_rowconfigure(7, weight=1)
frame.grid_columnconfigure(1, weight=1)

# Загрузка данных при старте
load_books()
update_tree()
root.mainloop()
