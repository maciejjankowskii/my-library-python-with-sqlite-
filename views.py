from abc import ABC, abstractmethod
from terminaltables import AsciiTable
from exception import WrongValueNewLastReadPage, WrongIdNumber
import unidecode


class AbstractView(ABC):
    def __init__(self):
        self.repositories = {}

    @abstractmethod
    def render(self):
        pass

    def set_repository(self, name, repository):
        self.repositories[name] = repository


class LastReadPage(AbstractView):
    SHORTCUT = '1'
    LABEL = 'Podaj ostatnią przeczytaną stronę książki'

    def render(self):
        print(LastReadPage.LABEL)
        done = False

        while not done:
            user_choice_book_id = int(input('Podaj id książki: '))
            for book_id, last_day_of_reading, last_read_page, number_of_pages in self.repositories['entry'].get_book_id_with_pages():
                if user_choice_book_id == book_id:
                    new_last_read_page = int(input('Podaj ostatnią przeczytaną stronę: '))
                    try:
                        if new_last_read_page < 0 or new_last_read_page > number_of_pages:
                            raise WrongValueNewLastReadPage()
                        self.repositories['entry'].save_new_read_page(book_id, new_last_read_page)
                        done = True
                    except WrongValueNewLastReadPage:
                        print('Sprawdź. Nieprawidłowa wartość.')
                        done = True


class AddBook(AbstractView):
    SHORTCUT = '2'
    LABEL = 'Dodaj książkę'

    def render(self):
        print(AddBook.LABEL)
        title = input('Tytuł: ')
        author = input('Autor: ')

        self._category_id_list = []

        self._category_list_iteration()

        if self.user_category_id == 0:
            new_category = input('Podaj nazwę nowej kategorii: ')
            self.repositories['category'].save_new_category(new_category)
            print('Dodano nową kategorię''\n')
            self._category_list_iteration()

        while self.user_category_id not in self._category_id_list:
            self.user_category_id = int(input('Błędne id kategorii, podaj jeszcze raz: '))

        year_of_release = input('Data wydania: ')
        number_of_pages = int(input('Ilość stron: '))
        self.repositories['entry'].save(title, author, self.user_category_id, year_of_release, number_of_pages)

    def _category_list_iteration(self):
        for category_id, category_name in self.repositories['category'].get_list_all_category_with_id():
            print(f'[{category_id}] - {category_name}')
            self._category_id_list.append(category_id)
        print('\n')
        print('[0] - dodanie nowej kategorii')
        self.user_category_id = int(input('Kategoria: '))


class DeleteBook(AbstractView):
    SHORTCUT = '3'
    LABEL = 'Usuń książkę'

    def render(self):
        print(DeleteBook.LABEL)
        id = int(input('Podaj id książki: '))

        try:
            if (id,) not in self.repositories['entry'].get_book_id(id):
                raise WrongIdNumber()
            self.repositories['entry'].delete(id)
            print(f'Usunięto pomyślnie książkę o nr id: {id}')
        except WrongIdNumber:
            print(f'Sprawdź. Nie ma na liście książki o podanym nr id: {id}.')


class ListAllBooks(AbstractView):
    SHORTCUT = '4'
    LABEL = 'Wypisz wszystkie książki'

    def render(self):
        print(ListAllBooks.LABEL)
        rows = [
            ['id',
             'Tytuł',
             'Autor',
             'Kategoria',
             'Rok wydania',
             'Ostatnio czytana',
             'Ostatnia strona',
             'Il. stron',
             'Poziom ukończenia',
             'Dostępność']
        ]
        for id, title, author, category_name, year_of_release, last_day_of_reading, \
            last_read_page, number_of_pages, status in self.repositories['entry'].get_list_all_books():

            book_percentage = round(last_read_page / number_of_pages * 100, 2)
            book_percentage_completion_bar = f'{book_percentage} % ' +  f'{"[" + "#" * int(book_percentage / 4) + "-" * (25 - int(book_percentage / 4)) + "]"}'

            rows.append([id, str(f'\x1B[3m{title}\x1B[0m'), author, category_name, year_of_release, last_day_of_reading,
                         last_read_page, number_of_pages, book_percentage_completion_bar, '\033[92m' + status + '\033[0m'])

        table = AsciiTable(rows)
        print(table.table)


class LendBook(AbstractView):
    SHORTCUT = '5'
    LABEL = 'Wypożycz książkę'

    def render(self):
        print(LendBook.LABEL)
        id = int(input('Podaj id książki: '))

        try:
            if (id,) not in self.repositories['entry'].get_book_id(id):
                raise WrongIdNumber()
            status = input(f'Podaj komu pożyczyłeś książkę: ')
            status = str('\033[93m' + f'Wypożyczona: ' + status + '\033[0m')
            self.repositories['entry'].save_lend_book(id, status)
            print(f'Zmieniono pomyślnie status książki o nr id: {id}')
        except WrongIdNumber:
            print(f'Sprawdź. Nie ma na liście książki o podanym nr id: {id}.')


class GetBackBook(AbstractView):
    SHORTCUT = '6'
    LABEL = 'Otrzymano wypożyczoną książkę'

    def render(self):
        print(GetBackBook.LABEL)
        id = int(input('Podaj id książki: '))

        try:
            if (id,) not in self.repositories['entry'].get_book_id(id):
                raise WrongIdNumber()
            status = str('\033[92m' + 'dostępna' + '\033[0m')
            self.repositories['entry'].save_lend_book(id, status)
            print(f'Zmieniono pomyślnie status książki o nr id: {id}')
        except WrongIdNumber:
            print(f'Sprawdź. Nie ma na liście książki o podanym nr id: {id}.')


class SearchBook(AbstractView):
    SHORTCUT = '7'
    LABEL = 'Wyszukaj książki'

    def render(self):
        print(SearchBook.LABEL)
        guessing_title = [input('Podaj tytuł książki to sprawdzenia: ')]

        titles_of_books = []
        for id, title, author, category_name, year_of_release, last_day_of_reading, \
            last_read_page, number_of_pages, status in self.repositories['entry'].get_list_all_books():

            titles_of_books.append(title)

        self._list_of_suggestions = []
        x = 0
        for word in titles_of_books:
            word = word.lower().strip()
            word = unidecode.unidecode(word)
            word = ''.join(char for char in word if char.isalnum())
            for word_old in guessing_title:
                for n in range(0, int(len(guessing_title[0]) - 4)):
                    word_2 = word_old.lower().strip()
                    word_2 = unidecode.unidecode(word_2)
                    word_2 = ''.join(char for char in word_2 if char.isalnum())
                    word_2 = word_2[n:n+3]
                    if word_2 in word:
                        self._list_of_suggestions.append(titles_of_books[x])
            x += 1

        try:
            print(f'Czy nie chodzi Tobie o książkę o tytule: \033[94m\x1B[3m{self.most_common_titles_from_list_of_suggestion()}\x1B[0m ?')
        except ValueError:
            print('Niestety nie ma na liście książki o takim lub podobnym tytule')

        rows = [
            ['id',
             'Tytuł',
             'Autor',
             'Kategoria',
             'Rok wydania',
             'Ostatnio czytana',
             'Ostatnia strona',
             'Il. stron',
             'Poziom ukończenia',
             'Dostępność']
        ]
        for id, title, author, category_name, year_of_release, last_day_of_reading, \
            last_read_page, number_of_pages, status in self.repositories['entry'].get_list_all_books():

            if self.most_common_titles_from_list_of_suggestion() == title:
                book_percentage = round(last_read_page / number_of_pages * 100, 2)
                book_percentage_completion_bar = f'{book_percentage} % ' + f'{"[" + "#" * int(book_percentage / 4) + "-" * (25 - int(book_percentage / 4)) + "]"}'
                rows.append([id, str(f'\x1B[3m{title}\x1B[0m'), author, category_name, year_of_release, last_day_of_reading,
                             last_read_page, number_of_pages, book_percentage_completion_bar,
                             '\033[92m' + status + '\033[0m'])
                print('Dane dla sugerowanej książki: ')
                table = AsciiTable(rows)
                print(table.table)

    def most_common_titles_from_list_of_suggestion(self):
        return max(set(self._list_of_suggestions), key=self._list_of_suggestions.count)


class Report(AbstractView):
    SHORTCUT = '8'
    LABEL = 'Wypisz raport mojej biblioteki'

    def render(self):
        counter_all_books = 0
        available_books = []
        lend_books = []

        for _, status in self.repositories['entry'].report_books():
            counter_all_books += 1
            if str('dostępna') in status:
                available_books.append(status)
            if str('Wypożyczona') in status:
                lend_books.append(status)

        print(f'Twoja aktualna biblioteczka składa się z {counter_all_books} książek')
        print(f'Ilość dostępnych książek: {len(available_books)}')
        print(f'Ilość pożyczonych książek: {len(lend_books)}')


class MainMenu:
    OPTIONS = {
        LastReadPage.SHORTCUT: LastReadPage(),
        AddBook.SHORTCUT: AddBook(),
        DeleteBook.SHORTCUT: DeleteBook(),
        ListAllBooks.SHORTCUT: ListAllBooks(),
        LendBook.SHORTCUT: LendBook(),
        GetBackBook.SHORTCUT: GetBackBook(),
        SearchBook.SHORTCUT: SearchBook(),
        Report.SHORTCUT: Report(),
     }

    def render(self):
        print('***Program do zarządzania moją domową biblioteczką***')
        print('Wybierz jedną z dostępnych opcji: ')
        for shortcut, label in MainMenu.OPTIONS.items():
            print(f'[{shortcut}] {label.LABEL}')

    def check_option(self):
        option = None
        while option not in MainMenu.OPTIONS:
            option = input('Wybierz opcję: ')

        return MainMenu.OPTIONS[option]
