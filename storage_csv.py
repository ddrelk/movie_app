import istorage
import csv
import random
import statistics
from fuzzywuzzy import fuzz

GREEN = '\033[32m'
RED = '\033[31m'
YELLOW = '\033[33m'
BLUE = '\033[34m'
MAGENTA = '\033[35m'
RESET = '\033[0m'


def web_serialize(movies):
    """
    This function returns a string representing the movie's details in HTML format.
    """
    output_string = ""
    output_string += "<li>"
    output_string += "<div class='movie'>"
    output_string += f"<a href='https://www.imdb.com/find/?q={movies[0]}&ref_=nv_sr_sm' target='_blank'>"
    output_string += f"<img class='movie-poster' src={movies[3]} alt='{movies[0]}'/>"
    output_string += "</a>"
    output_string += f"<div class='movie-title'>{movies[0]}</div>"
    output_string += f"<div class='movie-year'>{movies[2]}</div>"
    output_string += f"<div class='movie-rating'>{movies[1]}</div>"
    output_string += "</div>"
    output_string += "</li>"
    return output_string


def create_file(file_path):
    """This function creates an empty CSV file, if the file does not already exist.
    If the file does exist, it does nothing and continues without raising an error.
    """
    try:
        with open(file_path, 'x', newline=""):
            pass
    except FileExistsError:
        pass


def _file_exists(file_path):
    try:
        with open(file_path, 'r'):
            return True
    except FileNotFoundError:
        return False


class StorageCsv(istorage.IStorage):
    def __init__(self, filepath):
        if not _file_exists(filepath):
            create_file(filepath)
        self.filepath = filepath

    def load_from_file(self):
        with open(self.filepath, "r") as handle:
            return list(csv.reader(handle))

    def save_file(self, movie):
        """
        Saves the given product dict to the file, overwriting what's in the file.
        """
        with open(self.filepath, 'w', newline="") as file:
            csv_writer = csv.writer(file)
            csv_writer.writerows(movie)

    def list_movies(self):
        """
        List the movies in the movie database along with their ratings.
    Loads the movie information from the file.
    Formats the movie titles and ratings.
    Prints the total number of movies.
        """
        movies = self.load_from_file()
        print(type(movies))
        count = 0
        movies_string = ""
        for index in range(len(movies)):
            count += 1
            movies_string += f"{movies[index][0]}: {movies[index][1]}\n"
        print(f"{BLUE}{count} movies in total\n")
        return f"{movies_string}{RESET}"

    def add_movie(self):
        """
        Add a new movie to the movie database.
    Prompts the user to enter the name of the movie to add.
    Checks if the movie already exists in the database.
    If the movie doesn't exist, generates the movie information and adds it to the database.
        """
        load_movie = self.load_from_file()
        title = input("Enter movie name: ")
        for movie in load_movie:
            if title == movie[0]:
                return f"Movie {title} already exist"
        generated_movie = istorage.api_movie(title)
        new_movie_row = [generated_movie[key] for key in generated_movie]  # Extract values from dictionary
        load_movie.append(new_movie_row)
        self.save_file(load_movie)
        return f"Movie '{title}' added successfully."

    def delete_movie(self):
        """
        Delete a movie from the movie database based on its title.
    Prompts the user to enter the name of the movie to delete.
    Searches for the movie in the loaded movie list and removes it if found.
    Saves the updated movie information back to the file.
        """
        load_movie = self.load_from_file()
        title = input("Enter movie name: ")
        for movie in load_movie:
            if title == movie[0]:
                load_movie.remove(movie)
                self.save_file(load_movie)
                return f"{GREEN}Movie {title} successfully deleted{RESET}"
        return f"{RED}Error, Movie not found!!{RESET}"

    def update_movie(self):
        """
        Update the notes of a movie in the movie database.
    Prompts the user to enter the name of the movie and the new notes for the movie.
    Searches for the movie in the loaded movie list and updates its notes if found.
    Saves the updated movie information back to the file.
        """
        load_movie = self.load_from_file()
        title = input("Enter movie name: ")
        notes = input("Enter movie notes: ")
        for movie in load_movie:
            if title == movie[0]:
                movie.append(notes)
                self.save_file(load_movie)
                return f"Movie {title} successfully updated"
        return f"{RED}Error: Movie not found!!{RESET}"

    def movie_stats(self):
        """
        This function calculate statistics about the movies in the data.json file and print them to the console.
            The function calculates the average rating, median rating, the best movie, and the worst movie.
        """
        movies = self.load_from_file()
        num_movies = len(movies)
        total = 0
        ratings = []
        for movie_info in movies:
            rating_float_value = float(movie_info[1].split("/")[0])
            total += rating_float_value
            ratings.append(rating_float_value)
        print(f"{GREEN}Average rating: {total / num_movies}{RESET}")

        # Use the statistics module to calculate median
        print(f"{GREEN}Median rating: {statistics.median(ratings)}{RESET}")

        max_ratings = max([mov_1[1] for mov_1 in movies])
        for i in movies:
            if i[1] == max_ratings:
                print(f"{BLUE}Best movie: {i[0]}, {max_ratings}{RESET}")

        # WORST MOVIE
        worst_rating = min([mov_2[1] for mov_2 in movies])
        for j in movies:
            if j[1] == worst_rating:
                print(f"{RED}Worst movie: {j[0]}, {worst_rating}{RESET}")

    def random_movie(self):
        """Use the random module to randomly select a movie from the list"""
        movies = self.load_from_file()
        movie_random = random.choice(movies)
        return f"{GREEN}Your movie for tonight is: {movie_random[0]}, {movie_random[1]}{RESET}"

    def search_movie(self):
        """
        Search for movies in the movie storage by entering a partial or full movie name.
        The function will return a list of movies with matching titles sorted by rating,
        from highest to lowest. If no movies are found, the function will return an error message.
        """
        movies = self.load_from_file()
        search = input(f"{MAGENTA}Enter part of movie name: {RESET}")
        found_movies = []
        for movie_info in movies:
            movie = movie_info[0]
            score = fuzz.token_sort_ratio(search, movie)
            if score > 50:
                found_movies.append(movie_info)
        if found_movies:
            sorted_found_movies = sorted(found_movies, key=lambda x: x[1], reverse=True)
            print(f"No exact matches found for '{search}'. Did you mean:")
            for movie in sorted_found_movies:
                print(f"{GREEN}{movie[0]}{RESET}")
        else:
            print(f"{RED}Sorry, we couldn't find any movies similar to '{search}'.{RESET}")

    def sort_by_rating(self):
        """
        Loads the list of movies from the file, sorts them by rating (highest to lowest),
        and prints the sorted list to the console.
        """
        movies = self.load_from_file()
        sorted_movies = sorted(movies, key=lambda x: x[1], reverse=True)
        movies_str = ""
        for movie in sorted_movies:
            movies_str += f"{GREEN}{movie[0]}: {movie[1]}{RESET}\n"
        return movies_str

    def web_generator(self):
        """
        This function returns a string representing a list of movies in HTML format.
        """
        load_movie = self.load_from_file()
        movie_str = ""
        for movie in load_movie:
            movie_str += web_serialize(movie)
        return movie_str

    def file_io(self):
        """
        Generates a new HTML file "movie_app.html" by replacing the placeholder string
        "__TEMPLATE_MOVIE_GRID__" in the "index_template.html" file with the HTML string
        generated by the "web_generator()" function.
        """
        try:
            result = self.web_generator()
            template_file = "index_template.html"
            output_file = "movie_app.html"
            with open(template_file, "r") as file_obj:
                data = file_obj.readlines()
            with open(output_file, "w") as file_obj:
                new_data = [item.replace("        __TEMPLATE_MOVIE_GRID__", result) for item in data]
                file_obj.writelines(new_data)
                return "Website was generated successfully."
        except FileNotFoundError as e:
            return f"Error: File not found: {e}"
