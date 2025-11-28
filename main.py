from classes import BookStore
from exceptions import BookStoreException

def main():
    store = BookStore()
    
    print("=== КНИЖНЫЙ МАГАЗИН ===")
    
    # Загружаем данные
    try:
        if store.load_from_json():
            print("✓ Данные загружены из файла")
        else:
            print("Начинаем с пустого магазина")
    except Exception as e:
        print(f"Ошибка загрузки: {e}")
    
    while True:
        print("\n1. Добавить книгу")
        print("2. Показать все книги") 
        print("3. Выйти")
        
        choice = input("Выберите: ")
        
        if choice == '1':
            try:
                print("\n--- ДОБАВЛЕНИЕ КНИГИ ---")
                title = input("Название книги: ")
                author = input("Автор: ")
                price = float(input("Цена: "))
                quantity = int(input("Количество: "))
                
                book = store.add_book(title, author, price, quantity)
                print(f"✓ Добавлено: {book}")
                
                # Сохраняем с проверкой
                try:
                    store.save_to_json()
                    store.save_to_xml()
                    print("✓ Данные сохранены в JSON и XML")
                except Exception as e:
                    print(f"✗ Ошибка сохранения: {e}")
                    
            except Exception as e:
                print(f"✗ Ошибка: {e}")
            
        elif choice == '2':
            books = store.get_books()
            if books:
                print(f"\n--- КНИГИ ({len(books)} шт.) ---")
                for book in books:
                    print(f"  {book}")
            else:
                print("Нет книг в магазине")
                
        elif choice == '3':
            print("До свидания!")
            break
            
        else:
            print("Неверный выбор!")

if __name__ == "__main__":
    main()
