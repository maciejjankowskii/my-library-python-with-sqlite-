from views import MainMenu
from repositories import CategoryRepository, EntryRepository


class Application:
    def main(self):
        menu = MainMenu()
        menu.render()

        category_repository = self.get_category_repository()
        entry_repository = self.get_entry_repository()

        option = menu.check_option()
        option.set_repository('category', category_repository)
        option.set_repository('entry', entry_repository)
        option.render()

    def get_category_repository(self):
        return CategoryRepository()

    def get_entry_repository(self):
        return EntryRepository()


if __name__ == '__main__':
    app = Application()
    app.main()
