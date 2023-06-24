from abc import ABC, abstractmethod
import requests
API_KEY = "13043d11"


def api_movie(title):
    """
    This function sends a request to the OMDB API to retrieve details of a movie based on its title.
    It returns a dictionary containing the movie details, including title, rating, year, and poster.
    It raises KeyError if the requested movie does not exist in the OMDB database.
    It raises OSError if an error occurs while sending the request, typically due to a network
    connectivity issue.
    """
    try:
        url = f'http://www.omdbapi.com/?apikey={API_KEY}&t={title}'
        res = requests.get(url)
        result = res.json()
        movie_details = {"title": result['Title'],
                         "rating": result['Ratings'][0]['Value'].split("/")[0],
                         "year": result['Year'],
                         "poster": result['Poster']}
        return movie_details
    except KeyError:
        print("Movie doesn't exist in our database")
    except OSError as e:
        print(f"An {e} Occurred, Please check your internet Connection!")


def web_serialize(movies):
    """
    This function returns a string representing the movie's details in HTML format.
    """
    output_string = ""
    output_string += "<li>"
    output_string += "<div class='movie'>"
    output_string += f"<a href='https://www.imdb.com/find/?q={movies['title']}&ref_=nv_sr_sm' target='_blank'>"
    output_string += f"<img class='movie-poster' src={movies['poster']} alt='{movies['title']}'/>"
    output_string += "</a>"
    output_string += f"<div class='movie-title'>{movies['title']}</div>"
    output_string += f"<div class='movie-year'>{movies['year']}</div>"
    output_string += f"<div class='movie-rating'>{movies['rating']}</div>"
    output_string += "</div>"
    output_string += "</li>"
    return output_string


class IStorage(ABC):
    @abstractmethod
    def list_movies(self):
        pass

    @abstractmethod
    def add_movie(self):
        pass

    @abstractmethod
    def delete_movie(self):
        pass

    @abstractmethod
    def update_movie(self):
        pass
