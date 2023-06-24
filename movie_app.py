GREEN = '\033[32m'
RED = '\033[31m'
YELLOW = '\033[33m'
BLUE = '\033[34m'
MAGENTA = '\033[35m'
RESET = '\033[0m'
API_KEY = "13043d11"


class MovieApp:
    def __init__(self, storage):
        self._storage = storage

    def run(self):
        while True:
            try:

                print("********** My Movies Database **********")
                print(f"""{YELLOW}
            Menu:
            0. Exit
            1. List movies
            2. Add movie
            3. Delete movie
            4. Update movie
            5. Stats
            6. Random movie
            7. Search movie
            8. Movies sorted by rating
            9. Generate Website

                    {RESET}""")
                user = int(input(f"{MAGENTA}Enter choice (1-10) or (0) to Exit: {RESET}"))
                print(user)
                if user == 0:
                    print(f"{RED}Bye!{RESET}")
                    break
                elif user == 1:
                    print(self._storage.list_movies())
                elif user == 2:
                    print(self._storage.add_movie())
                elif user == 3:
                    print(self._storage.delete_movie())
                elif user == 4:
                    print(self._storage.update_movie())
                elif user == 5:
                    print(self._storage.movie_stats())
                elif user == 6:
                    print(self._storage.random_movie())
                elif user == 7:
                    print(self._storage.search_movie())
                elif user == 8:
                    print(self._storage.sort_by_rating())
                elif user == 9:
                    print(self._storage.file_io())
                input(f"{MAGENTA}\nPress Enter to continue{RESET}")
            except ValueError as e:
                print(f"Invalid input. {e} Error!!")
            except TypeError as e:
                print(f"Invalid input. {e} Error!!")
            except KeyError as e:
                print(f"Invalid choice. {e} Error!!")
