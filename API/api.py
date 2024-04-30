from flask import Flask, request
from flask_restful import Resource, Api, abort
from flask_cors import CORS
import json, urllib.request
import urllib
import math

app = Flask(__name__)
api = Api(app)

CORS(app, resources={r"/*":{'origins':"*"}})
CORS(app, resources={r"/*":{'origins':'http://localhost:5173', "allow_headers": "Access-Control-Allow-Origin"}})

TMDB_API_KEY = "4b5e824d2ef9e90fcf23c141bfed9388"

############## temporary "in memory" database ##############

deleted_movies = set()
allMoviesDeleted = False # if this is set to True, the only way back is to restart the API ¯\_(ツ)_/¯

liked_movies = set()
allMoviesLiked = False

############## classes ##############

# Movie
# shows all the info about the movie, lets you delete a movie and lets you like/unlike a movie
class Movie(Resource):

    def get(self, movie_id):
        """
        Movie GET Method

        Description: This method retrieves information about a movie with a given ID.

        Request:

            Endpoint: `/movies/<int:movie_id>`
            HTTP Method: GET
            URL Parameters:
                movie_id: int (required) The ID of the movie to retrieve. This should be an integer value. 
            Example Request:
                GET http://127.0.0.1:5000/movies/76600
        
        Response:

            HTTP Status Code: 200 OK
            Response Body:
                The response body contains a JSON object with the following properties:
                    movie: array[object]:
                        -(see object schema on https://developers.themoviedb.org/3/movies/get-movie-details)
            Example Response:
                {
                    "movie": {
                        "adult": false,
                        "backdrop_path": "/ovM06PdF3M8wvKb06i4sjW3xoww.jpg",
                        "belongs_to_collection": {
                            "id": 87096,
                            "name": "Avatar Collection",
                            "poster_path": "/uO2yU3QiGHvVp0L5e5IatTVRkYk.jpg",
                            "backdrop_path": "/iaEsDbQPE45hQU2EGiNjXD2KWuF.jpg"
                        },
                        "budget": 460000000,
                        "genres": [
                            {
                                "id": 878,
                                "name": "Science Fiction"
                            },
                            {
                                "id": 12,
                                "name": "Adventure"
                            },
                            {
                                "id": 28,
                                "name": "Action"
                            }
                        ],
                        "homepage": "https://www.avatar.com/movies/avatar-the-way-of-water",
                        "id": 76600,
                        "imdb_id": "tt1630029",
                        "original_language": "en",
                        "original_title": "Avatar: The Way of Water",
                        "overview": "Set more than a decade after the events of the first film, learn the story of the Sully family (Jake, Neytiri, and their kids), the trouble that follows them, the lengths they go to keep each other safe, the battles they fight to stay alive, and the tragedies they endure.",
                        "popularity": 10255.685,
                        "poster_path": "/t6HIqrRAclMCA60NsSmeqe9RmNV.jpg",
                        "production_companies": [
                            {
                                "id": 127928,
                                "logo_path": "/cxMxGzAgMMBhTXkcpYYCxWCOY90.png",
                                "name": "20th Century Studios",
                                "origin_country": "US"
                            },
                            {
                                "id": 574,
                                "logo_path": "/iB6GjNVHs5hOqcEYt2rcjBqIjki.png",
                                "name": "Lightstorm Entertainment",
                                "origin_country": "US"
                            }
                        ],
                        "production_countries": [
                            {
                                "iso_3166_1": "US",
                                "name": "United States of America"
                            }
                        ],
                        "release_date": "2022-12-14",
                        "revenue": 2309660236,
                        "runtime": 192,
                        "spoken_languages": [
                            {
                                "english_name": "English",
                                "iso_639_1": "en",
                                "name": "English"
                            }
                        ],
                        "status": "Released",
                        "tagline": "Return to Pandora.",
                        "title": "Avatar: The Way of Water",
                        "video": false,
                        "vote_average": 7.74,
                        "vote_count": 6285
                    }
                }

        Error Responses:

            If the requested movie ID does not exist, the server will return a 400 Bad Request error.

            HTTP Status Code: 400 Bad Request

        """

        if movie_id in deleted_movies or allMoviesDeleted:
            return "This movie has been deleted."
        else:
            movie_data = getMovieDataFromURL(f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={TMDB_API_KEY}&language=en-US')
            return {'movie': movie_data}


    def delete(self, movie_id):
        """
        Movie DELETE Method

        Description: This method deletes a movie with a given ID (from the local database).

        Request:

            Endpoint: `/movies/<int:movie_id>`
            HTTP Method: DELETE
            URL Parameters:
                movie_id: int (required) The ID of the movie to delete. This should be an integer value. 
            Example Request:
                DELETE http://127.0.0.1:5000/movies/76600
        
        Response:
            - HTTP Status Code: 204 No Content
            - Response Body: N/A

        Note: The movie ID is added to a set of deleted movie IDs to keep track of deleted movies.

        """

        deleted_movies.add(movie_id)
        return '', 204

    def put(self, movie_id):
        """
        Movie PUT Method

        Description: This method updates information about a movie with a given ID (in the local database). Updating means liking/unliking.

        Request:

            Endpoint: `/movies/<int:movie_id>`
            HTTP Method: PUT
            URL Parameters:
                movie_id: int (required) The ID of the movie to update. This should be an integer value. 
            Example Request:
                PUT http://127.0.0.1:5000/movies/76600
        
        Response:
            - HTTP Status Code: 201 Created
            - Response Body: N/A

        Note: The movie ID is added (or removed if it was already present in the set) to a set of liked movie IDs to keep track of liked movies.

        """

        if movie_id in liked_movies:
            liked_movies.remove(movie_id)
        else:
            liked_movies.add(movie_id)
        return '', 201

# Movies
# shows the latest (10) movies and lets you delete all movies. The put method likes/unlikes all movies.
class Movies(Resource):

    def get(self):
        """
        Movies GET Method

        Description: This method retrieves information about the latest (now_playing) ten movies from the TMDB API.

        Request:

            Endpoint: `/movies`, `/`
            HTTP Method: GET
            URL Parameters:
            Example Request:
                GET http://127.0.0.1:5000/movies
        
        Response:

            HTTP Status Code: 200 OK
            Response Body:
                The response body contains a JSON object with the following properties:
                    movies: array[object] (optional)
                        id: int (optional)
                        liked: bool (optional)
                        name: str (optional)
                        pop: float (optional)
                        avg_score: float (optional)
            Example Response:
                {
                    "movies": [
                        {
                            "id": 980078,
                            "liked": false,
                            "name": "Winnie the Pooh: Blood and Honey",
                            "pop": 3231.333,
                            "avg_score": 5.9
                        },
                        {
                            "id": 804150,
                            "liked": false,
                            "name": "Cocaine Bear",
                            "pop": 2982.867,
                            "avg_score": 6.5
                        },
                        ...
                    ]
                }

        Error Responses:

            If an error occurs while retrieving movie data from the TMDB API, the server will return a 500 Internal Server Error.

            HTTP Status Code: 500 Internal Server Error

        """
        
        try:
            movies = filterMovieData(10, f'https://api.themoviedb.org/3/movie/now_playing?api_key={TMDB_API_KEY}&language=en-US&page=1', math.inf)
            return {'movies': movies}
        except Exception as e:
            return {'message': str(e)}, 500
    
    def delete(self):
        """
        Movies DELETE Method

        Description: This method deletes all movies (from the local database).

        Request:

            Endpoint: `/movies`
            HTTP Method: DELETE
            URL Parameters:
            Example Request:
                DELETE http://127.0.0.1:5000/movies
        
        Response:
            - HTTP Status Code: 204 No Content
            - Response Body: N/A

        Note: The allMoviesDeleted is set to True so we know all movies were deleted.

        """

        allMoviesDeleted = True
        return '', 204
    
    def put(self):
        """
        Movies PUT Method

        Description: This method updates (likes/unlikes) all movies (from the local database).

        Request:

            Endpoint: `/movies`
            HTTP Method: PUT
            URL Parameters:
            Example Request:
                PUT http://127.0.0.1:5000/movies
        
        Response:
            - HTTP Status Code: 201 Created
            - Response Body: N/A

        Note: The allMoviesLiked is set to True if it was False previously (and vice versa).

        """

        if allMoviesLiked:
            allMoviesLiked = False
        else:
            allMoviesLiked = True
        return '', 201

# Popular
# shows the x most popular movies (default value is 10)
class Popular(Resource):

    def get(self):
        """
        Popular GET Method

        Description: 

            This method retrieves information about the most popular movies from the TMDB API.
            If no amount is given given, it returns the 10 first popular movies from the TMDB API.
            If a correct (> 0) amount is given, that amount is shown.

        Request:

            Endpoint: `/movies/popular`
            HTTP Method: GET
            URL Parameters:
                amount : int (optional) Integer amount representing the amount of popular movies to show.
                If this parameter is not provided, 
                the API will use the 10 first popular movies from the TMDB API. 
            Example Request:
                GET http://127.0.0.1:5000/movies/popular?amount=5
        
        Response:

            HTTP Status Code: 200 OK
            Response Body:
                The response body contains a JSON object with the following properties:
                    movies: array[object] (optional)
                        id: int (optional)
                        liked: bool (optional)
                        name: str (optional)
                        pop: float (optional)
                        avg_score: float (optional)
            Example Response:
                {
                    "movies": [
                        {
                            "id": 76600,
                            "liked": false,
                            "name": "Avatar: The Way of Water",
                            "pop": 10224.28,
                            "avg_score": 7.7
                        },
                        {
                            "id": 980078,
                            "liked": false,
                            "name": "Winnie the Pooh: Blood and Honey",
                            "pop": 3231.333,
                            "avg_score": 5.9
                        },
                        ...
                    ]
                }

        Error Responses:

            HTTP Status Code: 400 Bad Request
            Response Body:
                The response body contains a JSON object with the following properties:
                    message: str
                Example Response:
                    {"message": "Amount parameter is not an integer"}

            HTTP Status Code: 400 Bad Request
            Response Body:
                The response body contains a JSON object with the following properties:
                    message: str
                Example Response:
                    {"message": "Amount parameter is not positive"}

            HTTP Status Code: 500 Internal Server Error
            Response Body:
                The response body contains a JSON object with the following properties:
                    message: str
                Example Response:
                    {"message": "An internal server error occurred"}

        """

        amount = request.args.get('amount')
        if amount is None:
            amount = 10
        try:
            amount = int(amount)
            if amount <= 0:
                abort(400, message='Amount parameter is not positive')
        except ValueError:
            abort(400, message='Amount parameter is not an integer')

        try:
            movies = filterMovieData(amount, f'https://api.themoviedb.org/3/movie/popular?api_key={TMDB_API_KEY}&language=en-US', math.inf)
            return {'movies': movies}
        except:
            abort(500, message='An internal server error occurred')
        
# WithGenres
# shows movies with similar genres to the movie with the given movie id
class WithGenres(Resource):

    def get(self, movie_id):
        """
        WithGenres GET Method

        Description: 

            This method retrieves information about movies with exactly the same genres as the movie with the given movie id.
            The shown amount is limited to 20.

        Request:

            Endpoint: `/movies/<int:movie_id>/similar-genres`
            HTTP Method: GET
            URL Parameters:
                movie_id: int (required) The ID of the movie used to search for movies with the same genres. This should be an integer value. 
            Example Request:
                GET http://127.0.0.1:5000/movies/76600/similar-genres
        
        Response:

            HTTP Status Code: 200 OK
            Response Body:
                The response body contains a JSON object with the following properties:
                    movies: array[object] (optional)
                        id: int (optional)
                        liked: bool (optional)
                        name: str (optional)
                        pop: float (optional)
                        avg_score: float (optional)
            Example Response:
                {
                    "movies": [
                        {
                            "id": 505642,
                            "liked": false,
                            "name": "Black Panther: Wakanda Forever",
                            "pop": 1178.753,
                            "avg_score": 7.3
                        },
                        {
                            "id": 843794,
                            "liked": false,
                            "name": "JUNG_E",
                            "pop": 460.015,
                            "avg_score": 6.3
                        },
                        ...
                    ]
                }

        Error Responses:

            HTTP Status Code: 500 Internal Server Error
            Response Body:
                The response body contains a JSON object with the following properties:
                    message: str
                Example Response:
                    {"message": "An internal server error occurred"}

        """

        try:
            movie_data = getMovieDataFromURL(f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={TMDB_API_KEY}&language=en-US')
            genre_ids = [genre_id['id'] for genre_id in movie_data["genres"]]
            movies = filterMovieData(20, f'https://api.themoviedb.org/3/discover/movie?api_key={TMDB_API_KEY}&language=en-US&with_genres={",".join(map(str, genre_ids))}', movie_id, with_genres=True, genres_length=len(genre_ids))
            return {'movies': movies}
        except Exception as e:
            return {"message": "An internal server error occurred"}, 500

# WithGenres
# shows movies with similar runtimes to the movie with the given movie id
class WithRuntime(Resource):

    def get(self, movie_id):
        """
        WithRuntime GET Method

        Description: 

            This method retrieves information about movies with (roughly) the same runtime as the movie with the given movie id.
            The shown amount is limited to 20.

        Request:

            Endpoint: `/movies/<int:movie_id>/similar-runtime`
            HTTP Method: GET
            URL Parameters:
                movie_id: int (required) The ID of the movie used to search for movies with the same runtime. This should be an integer value. 
            Example Request:
                GET http://127.0.0.1:5000/movies/76600/similar-runtime
        
        Response:

            HTTP Status Code: 200 OK
            Response Body:
                The response body contains a JSON object with the following properties:
                    movies: array[object] (optional)
                        id: int (optional)
                        liked: bool (optional)
                        name: str (optional)
                        pop: float (optional)
                        avg_score: float (optional)
            Example Response:
                {
                    "movies": [
                        {
                            "id": 980078,
                            "liked": false,
                            "name": "Winnie the Pooh: Blood and Honey",
                            "pop": 3231.333,
                            "avg_score": 5.9
                        },
                        {
                            "id": 842945,
                            "liked": false,
                            "name": "Supercell",
                            "pop": 3000.274,
                            "avg_score": 6.1
                        },
                        ...
                    ]
                }

        Error Responses:

            HTTP Status Code: 500 Internal Server Error
            Response Body:
                The response body contains a JSON object with the following properties:
                    message: str
                Example Response:
                    {"message": "An internal server error occurred"}

        """

        try:
            movie_data = getMovieDataFromURL(f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={TMDB_API_KEY}&language=en-US')
            runtime = movie_data['runtime']
            movies = filterMovieData(20, f'https://api.themoviedb.org/3/discover/movie?api_key={TMDB_API_KEY}&language=en-US&with_runtime_gte={runtime-10}&with_runtime_lte={runtime+10}', movie_id)
            return {'movies': movies}
        except Exception as e:
            return {"message": "An internal server error occurred"}, 500

# WithGenres
# shows movies with similar actors to the movie with the given movie id
class WithActors(Resource):

    def get(self, movie_id):
        """
        WithActors GET Method

        Description: 

            This method retrieves information about movies with the same (two first) actors as the movie with the given movie id.
            The shown amount is limited to 20.

        Request:

            Endpoint: `/movies/<int:movie_id>/similar-actors`
            HTTP Method: GET
            URL Parameters:
                movie_id: int (required) The ID of the movie used to search for movies with the same (two first) actors. This should be an integer value. 
            Example Request:
                GET http://127.0.0.1:5000/movies/76600/similar-actors
        
        Response:

            HTTP Status Code: 200 OK
            Response Body:
                The response body contains a JSON object with the following properties:
                    movies: array[object] (optional)
                        id: int (optional)
                        liked: bool (optional)
                        name: str (optional)
                        pop: float (optional)
                        avg_score: float (optional)
            Example Response:
                {
                    "movies": [
                        {
                            "id": 19995,
                            "liked": false,
                            "name": "Avatar",
                            "pop": 432.199,
                            "avg_score": 7.6
                        },
                        {
                            "id": 183392,
                            "liked": false,
                            "name": "Capturing Avatar",
                            "pop": 70.096,
                            "avg_score": 7.8
                        },
                        ...
                    ]
                }

        Error Responses:

            HTTP Status Code: 500 Internal Server Error
            Response Body:
                The response body contains a JSON object with the following properties:
                    message: str
                Example Response:
                    {"message": "An internal server error occurred"}

        """

        try:
            movie_data = getMovieDataFromURL(f'https://api.themoviedb.org/3/movie/{movie_id}/credits?api_key={TMDB_API_KEY}')
            actor_ids = [actor['id'] for actor in movie_data['cast'][:2]]
            print("actor_ids", actor_ids)
            movies = filterMovieData(20, f'https://api.themoviedb.org/3/discover/movie?api_key={TMDB_API_KEY}&language=en-US&with_cast={",".join(map(str, actor_ids))}', movie_id)
            return {'movies': movies}
        except Exception as e:
            return {"message": "An internal server error occurred"}, 500
    
# MoviesBarplot
# generates the link to create a barplot comparing the average score of the given 10 first popular movies (10 first 'now playing movies' if no movie id's were given)
class MoviesBarplot(Resource):

    def get(self):
        """
        MoviesBarplot GET Method

        Description: 

            Generates a link that redirects to a bar chart comparing the average score 
            of the given 10 first (popular) movies. If no movie ids are given, it takes the 10 first 'now playing movies' 
            from the TMDB API. The bar chart is generated using the QuickChart API.

        Request:

            Endpoint: `/movies/barplot`
            HTTP Method: GET
            URL Parameters:
                movie-ids : str (optional) Comma-separated list of existing movie IDs. 
                Only the first 10 IDs will be used to generate the chart. 
                If this parameter is not provided or is an empty string, 
                the API will use the 10 first 'now playing movies' from the TMDB API. 
            Example Request:
                GET http://127.0.0.1:5000/movies/barplot?movie-ids=76600,67890
        
        Response:

            HTTP Status Code: 200 OK
            Response Body:
                The response body contains a JSON object with the following properties:
                    chart_url: str (optional)
            Example Response:
                {
                    "chart_url": "https://quickchart.io/chart?c={type:'bar',data:{labels:[\"Avatar: The Way of Water\",\"Katha Parayumbol\"],datasets:[{label:'Vote Average Score',data:[7.74,7.531]}]}}"
                }

        Error Responses:

            HTTP Status Code: 500 Internal Server Error
            Response Body:
                The response body contains a JSON object with the following properties:
                    message: str
                Example Response:
                    {"message": "An internal server error occurred"}

        """

        try:
            movie_ids_string: str = request.args.get('movie-ids')
            movie_ids: list = []
            
            if movie_ids_string is None or movie_ids_string == "":
                movies_data = getMoviesDataFromURL(f'https://api.themoviedb.org/3/movie/now_playing?api_key={TMDB_API_KEY}&language=en-US&page=1')
                for j in range(10): # filtering of the movies in the list of returned movies
                    movie_ids.append(str(movies_data[j]["id"]))
            else:
                movie_ids = movie_ids_string.split(",")[:10] # limit amount of movies to plot to 10

            chart_url = generateBarplotURL(movie_ids)
            return {"chart_url": chart_url}
        except Exception as e:
            return {"message": "An internal server error occurred"}, 500


############## API resource routing ##############

api.add_resource(Movies, '/', '/movies')
# requirement: Be able to ’delete’ a movie, i.e., the movie won’t be returned from the API after ’deletion’, unless the API is restarted.
# requirement: Be able to ’like’ and ’un-like’ a movie
api.add_resource(Movie, '/movies/<int:movie_id>')
# requirement: List the first x popular movies. (x can be any arbitrary number)
api.add_resource(Popular, '/movies/popular')
# requirement: Given a movie, return the movies that have exactly the same genres.
api.add_resource(WithGenres, '/movies/<int:movie_id>/similar-genres')
# requirement: Given a movie, return the movies that have a similar runtime. (You can assume a similar runtime has a maximum of 10 minutes difference)
api.add_resource(WithRuntime, '/movies/<int:movie_id>/similar-runtime')
# requirement: Given a movie, return the movies that have two overlapping actor(s). (You can assume the first 2 actors listed)
api.add_resource(WithActors, '/movies/<int:movie_id>/similar-actors')
# requirement: Given a set of movies, have the ability to generate a barplot comparing the average score of these movies.
api.add_resource(MoviesBarplot, '/movies/barplot')

############## Helper functions ##############

def getMovieDataFromURL(url: str):
    """
    Get all the information (json format) about one (or more) movie(s) given by the url
    """
    try:
        response = urllib.request.urlopen(url)
        data = response.read()
        return json.loads(data)
    except urllib.error.HTTPError as e:
        abort(400, message=e.__dict__) 
    except urllib.error.URLError as e:
        abort(400, message=e.__dict__) 
    except:
        abort(400, message='(One of the) API call(s) failed.') 

def getMoviesDataFromURL(url: str):
    """
    Get all the information (json format) about multiple movies given by the url
    """
    return getMovieDataFromURL(url)["results"]

def filterMovieData(amount: int, url: str, movie_id, with_genres=False, genres_length=0):
    """
    Filter movie data: gets the required fields of the returned movies (by the url) and returns a new array of movie data dictionaries
    @param amount : amount of movies to show
    @param movie_id : passed to ensure we don't return this movie when looking for similar movies to this one
    @param with_genres: True if we require exactly the same genres as the movie_id movie.
    """
    movies = []
    counter = 0
    del_movies_counter = 0
    while counter != amount:

        movies_data = getMoviesDataFromURL(url + f'&page={math.floor((counter+del_movies_counter)/20)+1}')
        temp_amount = min(amount-counter, 20)

        if len(movies_data) < (temp_amount): # if amount of movies returned is smaller than the requested amount
            for j in range(len(movies_data)):
                if movies_data[j]["id"] == movie_id or movies_data[j]["id"] in deleted_movies:
                    pass
                else:
                    if (with_genres and len(movies_data[j]["genre_ids"]) == genres_length) or with_genres is False:
                        movies.append({'id': movies_data[j]["id"], 'liked': True if movies_data[j]["id"] in liked_movies else False, 'name': movies_data[j]["title"], 'pop': movies_data[j]["popularity"], 'avg_score': movies_data[j]["vote_average"]})
            return movies
        for j in range(len(movies_data)): # filtering of the movies in the list of returned movies
            if movies_data[j]["id"] == movie_id or movies_data[j]["id"] in deleted_movies:
                del_movies_counter += 1
            else:
                if (with_genres and len(movies_data[j]["genre_ids"]) == genres_length) or with_genres is False:
                    movies.append({'id': movies_data[j]["id"], 'liked': True if movies_data[j]["id"] in liked_movies else False, 'name': movies_data[j]["title"], 'pop': movies_data[j]["popularity"], 'avg_score': movies_data[j]["vote_average"]})
                counter += 1
                if counter == amount:
                    break
    assert amount >= len(movies)
    return movies

def generateBarplotURL(movie_ids: list):
    """
    Generates the url for the quickchart api, we use this url in the frontend to redirect to.
    @param movie_ids : list of movie id's, from which we can get the names and scores to plot the bar chart
    """
    titles = []
    scores = []
    
    for movie_id in movie_ids:
        movie_data = getMovieDataFromURL(f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={TMDB_API_KEY}&language=en-US')
        titles.append(movie_data["title"])
        scores.append(movie_data["vote_average"])

    conf_string = "{type:'bar',data:{labels:[" + ",".join(f'"{item}"' for item in titles) + "],datasets:[{label:'Vote Average Score',data:[" + ",".join(map(str, scores)) + "]}]}}"
    chart_url = f'https://quickchart.io/chart?c={conf_string}'
    return chart_url

if __name__ == '__main__':
    app.run(debug=True, port=5000)