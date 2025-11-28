import json
import xml.etree.ElementTree as ET
import os
from exceptions import ValidationException, BookNotFoundException, FileOperationException

class Book:
    def __init__(self, book_id, title, author, price, quantity):
        self._validate_input(book_id, title, author, price, quantity)
        self.id = book_id
        self.title = title
        self.author = author
        self.price = price
        self.quantity = quantity
    
    def _validate_input(self, book_id, title, author, price, quantity):
        if not isinstance(book_id, int) or book_id < 0:
            raise ValidationException("ID", book_id)
        if not title or not isinstance(title, str):
            raise ValidationException("Название", title)
        if not author or not isinstance(author, str):
            raise ValidationException("Автор", author)
        if not isinstance(price, (int, float)) or price < 0:
            raise ValidationException("Цена", price)
        if not isinstance(quantity, int) or quantity < 0:
            raise ValidationException("Количество", quantity)
    
    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "price": self.price,
            "quantity": self.quantity
        }
    
    @staticmethod
    def from_dict(data):
        return Book(data["id"], data["title"], data["author"], data["price"], data["quantity"])
    
    def __str__(self):
        return f"ID: {self.id}, '{self.title}' - {self.author}, {self.price} руб., {self.quantity} шт."

class BookStore:
    def __init__(self, filename="bookstore_data"):
        self.books = []
        self.filename = filename
    
    def add_book(self, title, author, price, quantity):
        try:
            book_id = max([book.id for book in self.books], default=0) + 1
            book = Book(book_id, title, author, price, quantity)
            self.books.append(book)
            return book
        except ValidationException as e:
            raise e
    
    def get_books(self, book_id=None):
        try:
            if book_id is None:
                return self.books
            book = next((book for book in self.books if book.id == book_id), None)
            if not book:
                raise BookNotFoundException(book_id)
            return book
        except BookNotFoundException:
            raise
    
    def update_book(self, book_id, title=None, author=None, price=None, quantity=None):
        try:
            book = self.get_books(book_id)
            if book:
                if title is not None:
                    book.title = title
                if author is not None:
                    book.author = author
                if price is not None:
                    book.price = price
                if quantity is not None:
                    book.quantity = quantity
                return book
            return None
        except BookNotFoundException:
            raise
    
    def delete_book(self, book_id):
        try:
            book = self.get_books(book_id)
            self.books = [book for book in self.books if book.id != book_id]
            return True
        except BookNotFoundException:
            raise
    
    def get_stats(self):
        total_books = sum(book.quantity for book in self.books)
        total_value = sum(book.price * book.quantity for book in self.books)
        return {
            "total_books": total_books,
            "total_value": total_value,
            "unique_titles": len(self.books)
        }
    
    def save_to_json(self, filename=None):
        try:
            filename = filename or f"{self.filename}.json"
            data = {
                "books": [book.to_dict() for book in self.books]
            }
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            raise FileOperationException(f"Ошибка сохранения JSON", filename)
    
    def load_from_json(self, filename=None):
        try:
            filename = filename or f"{self.filename}.json"
            if not os.path.exists(filename):
                return False
            
            with open(filename, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            self.books = [Book.from_dict(book_data) for book_data in data["books"]]
            return True
        except Exception as e:
            raise FileOperationException(f"Ошибка загрузки JSON", filename)
    
    def save_to_xml(self, filename=None):
        try:
            filename = filename or f"{self.filename}.xml"
            root = ET.Element("bookstore")
            
            for book in self.books:
                book_elem = ET.SubElement(root, "book")
                for key, value in book.to_dict().items():
                    child = ET.SubElement(book_elem, key)
                    child.text = str(value)
            
            tree = ET.ElementTree(root)
            with open(filename, "wb") as f:
                tree.write(f, encoding="utf-8", xml_declaration=True)
            return True
        except Exception as e:
            raise FileOperationException(f"Ошибка сохранения XML", filename)
    
    def load_from_xml(self, filename=None):
        try:
            filename = filename or f"{self.filename}.xml"
            if not os.path.exists(filename):
                return False
            
            tree = ET.parse(filename)
            root = tree.getroot()
            
            self.books = []
            for book_elem in root.findall("book"):
                book_data = {}
                for child in book_elem:
                    if child.tag in ["id", "quantity"]:
                        book_data[child.tag] = int(child.text)
                    elif child.tag == "price":
                        book_data[child.tag] = float(child.text)
                    else:
                        book_data[child.tag] = child.text
                
                self.books.append(Book.from_dict(book_data))
            return True
        except Exception as e:
            raise FileOperationException(f"Ошибка загрузки XML", filename)
