class BookStoreException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class FileOperationException(BookStoreException):
    def __init__(self, message, filename):
        self.filename = filename
        super().__init__(f"{message} (Файл: {filename})")

class BookNotFoundException(BookStoreException):
    def __init__(self, book_id):
        super().__init__(f"Книга с ID {book_id} не найдена")

class ValidationException(BookStoreException):
    def __init__(self, field, value):
        super().__init__(f"Некорректное значение '{value}' для поля '{field}'")
