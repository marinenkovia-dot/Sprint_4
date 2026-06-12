from main import BooksCollector
import pytest


class TestBooksCollector:
    @pytest.mark.parametrize("book_name", [
        "Война и мир",
        "Властелин колец",
        "a" * 40])
    def test_add_new_book_success(self, collector, book_name):
        collector.add_new_book(book_name)
        assert book_name in collector.books_genre

    @pytest.mark.parametrize("invalid_name", ["", "a" * 41])
    def test_add_new_book_invalid_length(self, collector, invalid_name):
        collector.add_new_book(invalid_name)
        assert invalid_name not in collector.books_genre

    def test_set_book_genre_valid(self, collector):
        book_name = "Гарри Поттер"
        genre = "Фантастика"
        collector.add_new_book(book_name)
        collector.set_book_genre(book_name, genre)        
        assert collector.get_book_genre(book_name) == genre

    def test_set_book_genre_missing_genre(self, collector):
        collector.add_new_book("Книга")
        collector.set_book_genre("Книга", "Неизвестный жанр")
        assert collector.get_book_genre("Книга") == ""

    def test_set_book_genre_not_exists_book(self, collector):
        collector.set_book_genre("Несуществующая книга", "Фантастика")
        assert collector.get_book_genre("Несуществующая книга") is None

    def test_get_books_with_specific_genre(self, collector):
        books_data = [
            ("Книга 1", "Фантастика"),
            ("Книга 2", "Фантастика"),
            ("Книга 3", "Детективы")]
        
        for name, genre in books_data:
            collector.add_new_book(name)
            collector.set_book_genre(name, genre)
            
        result = collector.get_books_with_specific_genre("Фантастика")
        expected = ["Книга 1", "Книга 2"]
        assert result == expected

    def test_get_books_for_children(self, collector):
        books_data = [
            ("Детская сказка", "Мультфильмы"),
            ("Страшилка", "Ужасы"),
            ("Детектив для детей", "Детективы"),
            ("Научная фантастика", "Фантастика")]
        
        for name, genre in books_data:
            collector.add_new_book(name)
            collector.set_book_genre(name, genre)
            
        result = collector.get_books_for_children()
        expected = ["Детская сказка", "Научная фантастика"]
        assert result == expected

    def test_favorites_add_and_uniqueness(self, collector):
        book_name = "Любимая книга"
        collector.add_new_book(book_name) 
        collector.add_book_in_favorites(book_name)
        collector.add_book_in_favorites(book_name)
        
        assert len(collector.get_list_of_favorites_books()) == 1
        assert collector.get_list_of_favorites_books()[0] == book_name

    def test_favorites_add_invalid_book(self, collector):
        invalid_book = "Книга не из коллекции"
        collector.add_book_in_favorites(invalid_book)
        assert invalid_book not in collector.get_list_of_favorites_books()

    def test_delete_from_favorites(self, collector):
        book_name = "Удаляемая книга"
        collector.add_new_book(book_name)
        collector.add_book_in_favorites(book_name)
        assert book_name in collector.get_list_of_favorites_books()
        
        collector.delete_book_from_favorites(book_name)
        assert book_name not in collector.get_list_of_favorites_books()

    def test_delete_nonexistent_from_favorites(self, collector):
        collector.delete_book_from_favorites("Нет такой книги")
        assert collector.get_list_of_favorites_books() == []