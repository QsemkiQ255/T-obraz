import json
import os

DATA_FILE = "library.json"

class Book:
    """Модель книги."""
    def __init__(self, title, author, genre, year, description):
        self.title = title
        self.author = author
        self.genre = genre
        self.year = year
        self.description = description
        self.is_read = False
        self.is_favorite = False

    def to_dict(self):
        return {
            "title": self.title,
            "author": self.author,
            "genre": self.genre,
            "year": self.year,
            "description": self.description,
            "is_read": self.is_read,
            "is_favorite": self.is_favorite
        }

    @staticmethod
    def from_dict(data):
        book = Book(
            title=data["title"],
            author=data["author"],
            genre=data["genre"],
            year=data["year"],
            description=data["description"]
        )
        book.is_read = data["is_read"]
        book.is_favorite = data["is_favorite"]
        return book


class Library:
    def __init__(self):
        self.books = []
        self.load_from_file()

    def add_book(self, title, author, genre, year, description):
        book = Book(title, author, genre, year, description)
        self.books.append(book)
        self.save_to_file()
        print(f"Книга '{title}' успешно добавлена!")

    def list_books(self, sort_by=None, filter_genre=None, filter_read=None):
        books = self.books[:]
        if filter_genre:
            books = [b for b in books if b.genre.lower() == filter_genre.lower()]
        if filter_read is not None:
            books = [b for b in books if b.is_read == filter_read]
        if sort_by == "title":
            books.sort(key=lambda b: b.title.lower())
        elif sort_by == "author":
            books.sort(key=lambda b: b.author.lower())
        elif sort_by == "year":
            books.sort(key=lambda b: b.year)
        return books

    def mark_as_read(self, title):
        for book in self.books:
            if book.title.lower() == title.lower():
                book.is_read = True
                self.save_to_file()
                print(f"Книга '{title}' отмечена как прочитанная.")
                return
        print(f"Книга с названием '{title}' не найдена.")

    def mark_as_unread(self, title):
        for book in self.books:
            if book.title.lower() == title.lower():
                book.is_read = False
                self.save_to_file()
                print(f"Книга '{title}' отмечена как непрочитанная.")
                return
        print(f"Книга с названием '{title}' не найдена.")

    def add_to_favorites(self, title):
        for book in self.books:
            if book.title.lower() == title.lower():
                book.is_favorite = True
                self.save_to_file()
                print(f"Книга '{title}' добавлена в избранное.")
                return
        print(f"Книга с названием '{title}' не найдена.")

    def remove_from_favorites(self, title):
        for book in self.books:
            if book.title.lower() == title.lower():
                book.is_favorite = False
                self.save_to_file()
                print(f"Книга '{title}' удалена из избранного.")
                return
        print(f"Книга с названием '{title}' не найдена.")

    def list_favorites(self):
        return [book for book in self.books if book.is_favorite]

    def delete_book(self, title):
        for i, book in enumerate(self.books):
            if book.title.lower() == title.lower():
                del self.books[i]
                self.save_to_file()
                print(f"Книга '{title}' удалена из библиотеки.")
                return
        print(f"Книга с названием '{title}' не найдена.")

    def search_books(self, keyword):
        keyword = keyword.lower()
        results = []
        for book in self.books:
            if (keyword in book.title.lower() or
                keyword in book.author.lower() or
                keyword in book.description.lower()):
                results.append(book)
        return results

    def save_to_file(self):
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump([book.to_dict() for book in self.books], f, ensure_ascii=False, indent=4)

    def load_from_file(self):
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.books = [Book.from_dict(item) for item in data]
            except Exception as e:
                print(f"Ошибка загрузки файла: {e}. Будет создана новая библиотека.")
                self.books = []
        else:
            self.books = []


def display_books(books):
    if not books:
        print("Нет книг для отображения.")
        return
    print("\n" + "="*100)
    print(f"{'№':<3} {'Название':<25} {'Автор':<20} {'Жанр':<15} {'Год':<6} {'Статус':<10} {'Избранное':<10}")
    print("="*100)
    for idx, book in enumerate(books, 1):
        status = "Прочитана" if book.is_read else "Не прочитана"
        fav = "Да" if book.is_favorite else "Нет"
        print(f"{idx:<3} {book.title[:25]:<25} {book.author[:20]:<20} {book.genre[:15]:<15} {book.year:<6} {status:<10} {fav:<10}")
    print("="*100 + "\n")


library = Library()

while True:
    print("\n--- T-Библиотека ---")
    print("1. Добавить книгу")
    print("2. Просмотреть все книги")
    print("3. Просмотреть избранное")
    print("4. Найти книгу")
    print("5. Отметить как прочитанную")
    print("6. Отметить как непрочитанную")
    print("7. Добавить в избранное")
    print("8. Удалить из избранного")
    print("9. Удалить книгу")
    print("0. Выход")

    choice = input("Выберите действие: ").strip()

    if choice == "1":
        title = input("Название: ").strip()
        author = input("Автор: ").strip()
        genre = input("Жанр: ").strip()
        year = input("Год издания: ").strip()
        description = input("Краткое описание: ").strip()
        if not all([title, author, genre, year, description]):
            print("Ошибка: все поля должны быть заполнены.")
            continue
        try:
            year = int(year)
        except ValueError:
            print("Ошибка: год должен быть числом.")
            continue
        library.add_book(title, author, genre, year, description)

    elif choice == "2":
        print("\nФильтры (оставьте пустым, чтобы пропустить):")
        filter_genre = input("Жанр: ").strip() or None
        filter_read_input = input("Статус (1 - прочитана, 0 - не прочитана): ").strip()
        filter_read = None
        if filter_read_input == "1":
            filter_read = True
        elif filter_read_input == "0":
            filter_read = False
        sort_by = input("Сортировать по (title/author/year): ").strip().lower()
        if sort_by not in ["title", "author", "year"]:
            sort_by = None

        books = library.list_books(sort_by, filter_genre, filter_read)
        display_books(books)

    elif choice == "3":
        favorites = library.list_favorites()
        display_books(favorites)

    elif choice == "4":
        keyword = input("Введите ключевое слово для поиска: ").strip()
        if not keyword:
            print("Ключевое слово не может быть пустым.")
            continue
        results = library.search_books(keyword)
        display_books(results)

    elif choice == "5":
        title = input("Введите название книги: ").strip()
        library.mark_as_read(title)

    elif choice == "6":
        title = input("Введите название книги: ").strip()
        library.mark_as_unread(title)

    elif choice == "7":
        title = input("Введите название книги: ").strip()
        library.add_to_favorites(title)

    elif choice == "8":
        title = input("Введите название книги: ").strip()
        library.remove_from_favorites(title)

    elif choice == "9":
        title = input("Введите название книги: ").strip()
        library.delete_book(title)

    elif choice == "0":
        print("До свидания!")
        break

    else:
        print("Неверный ввод, попробуйте снова.")
