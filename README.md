# DS_Assignment1

The goal of the assignment is twofold:

• Firstly, using the API of https://themoviedb.org, the goal is to create
a RESTful API that functions as a very basic recommendation engine for
movies.

• Secondly, implement a simple webpage that consumes the
API. This will mainly serve to easily illustrate the functionalities.

<p>&nbsp;</p>

To run the application, execute the run.sh script in the root folder.

**TMDB API KEY** = "4b5e824d2ef9e90fcf23c141bfed9388"

**(Additional) libraries used:**

(requirements.txt)

Flask==2.0.3,
Flask_Cors==3.0.10,
Flask_RESTful==0.3.9

---


<p>&nbsp;</p>

## API manual:

<p>&nbsp;</p>

### **Movie**

<p>&nbsp;</p>

### Movie GET Method

**Description:** This method retrieves information about a movie with a given ID.

**Request:**

- Endpoint: `/movies/<int:movie_id>`
- HTTP Method: GET
- URL Parameters:
    * movie_id: int (required) The ID of the movie to retrieve. This should be an integer value. 
- Example Request:
    `GET http://127.0.0.1:5000/movies/76600`

**Response:**

HTTP Status Code: 200 OK

Response Body:
```
The response body contains a JSON object with the following properties:

movie: array[object]:
    (see object schema on https://developers.themoviedb.org/3/movies/get-movie-details)
```
Example Response:
```
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
        ...
    }
}
```
**Error Responses:**
```
If the requested movie ID does not exist, the server will return a 400 Bad Request error.

HTTP Status Code: 400 Bad Request
```

### Movie DELETE Method

**Description:** This method deletes a movie with a given ID (from the local database).

**Request:**

- Endpoint: `/movies/<int:movie_id>`
- HTTP Method: DELETE
- URL Parameters:
    * movie_id: int (required) The ID of the movie to delete. This should be an integer value. 
- Example Request:
    `DELETE http://127.0.0.1:5000/movies/76600`

**Response:**
```
HTTP Status Code: 204 No Content
Response Body: N/A
```
**Note:** The movie ID is added to a set of deleted movie IDs to keep track of deleted movies.

### Movie PUT Method

**Description:** This method updates information about a movie with a given ID (in the local database). Updating means liking/unliking the movie.

**Request:**

- Endpoint: `/movies/<int:movie_id>`
- HTTP Method: PUT
- URL Parameters:
    * movie_id: int (required) The ID of the movie to update. This should be an integer value. 
- Example Request:
    `PUT http://127.0.0.1:5000/movies/76600`

**Response:**
```
HTTP Status Code: 201 Created
Response Body: N/A
```

**Note:** The movie ID is added (or removed if it was already present in the set) to a set of liked movie IDs to keep track of liked movies.

---

### **Movies**

<p>&nbsp;</p>

### Movies GET Method

**Description:** This method retrieves information about the latest (now_playing) ten movies from the TMDB API.

**Request:**

- Endpoint: `/movies`, `/`
- HTTP Method: GET
- URL Parameters:
- Example Request:
    `GET http://127.0.0.1:5000/movies`

**Response:**

HTTP Status Code: 200 OK

Response Body:
```
The response body contains a JSON object with the following properties:
    movies: array[object] (optional)
        id: int (optional)
        liked: bool (optional)
        name: str (optional)
        pop: float (optional)
        avg_score: float (optional)
```
Example Response:
```
{
    "movies": [
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
```

**Error Responses:**
```
If an error occurs while retrieving movie data from the TMDB API, the server will return a 500 Internal Server Error.

HTTP Status Code: 500 Internal Server Error
```

### Movies DELETE Method

**Description:** This method deletes all movies (from the local database).

**Request:**

- Endpoint: `/movies`, `/`
- HTTP Method: DELETE
- URL Parameters:
- Example Request:
    `DELETE http://127.0.0.1:5000/movies`

**Response:**
```
HTTP Status Code: 204 No Content
Response Body: N/A
```

### Movies PUT Method

**Description:** This method updates (likes/unlikes) all movies (from the local database).

**Request:**

- Endpoint: `/movies`, `/`
- HTTP Method: PUT
- URL Parameters:
- Example Request:
    `PUT http://127.0.0.1:5000/movies`

**Response:**
```
HTTP Status Code: 201 Created
Response Body: N/A
```

---

### **Popular**

<p>&nbsp;</p>

### Popular GET Method

**Description:**

This method retrieves information about the most popular movies from the TMDB API.
If no amount is given given, it returns the 10 first popular movies from the TMDB API.
If a correct (> 0) amount is given, that amount is shown.

**Request:**

- Endpoint: `/movies/popular`
- HTTP Method: GET
- URL Parameters:
    * amount : int (optional) Integer amount representing the amount of popular movies to show.
    If this parameter is not provided, 
    the API will use the 10 first popular movies from the TMDB API. 
- Example Request:
    `GET http://127.0.0.1:5000/movies/popular?amount=5`

**Response:**

HTTP Status Code: 200 OK

Response Body:
```
The response body contains a JSON object with the following properties:
    movies: array[object] (optional)
        id: int (optional)
        liked: bool (optional)
        name: str (optional)
        pop: float (optional)
        avg_score: float (optional)
```
Example Response:
```
{
    "movies": [
        {
            "id": 76600,
            "liked": false,
            "name": "Avatar: The Way of Water",
            "pop": 10224.28,
            "avg_score": 7.7
        },
        ...
    ]
}
```

**Error Responses:**
```
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
```
---

### **WithGenres**

<p>&nbsp;</p>

### WithGenres GET Method

**Description:** 

This method retrieves information about movies with exactly the same genres as the movie with the given movie id.
The shown amount is limited to 20.

**Request:**

- Endpoint: `/movies/<int:movie_id>/similar-genres`
- HTTP Method: GET
- URL Parameters:
    * movie_id: int (required) The ID of the movie used to search for movies with the same genres. This should be an integer value. 
- Example Request:
    `GET http://127.0.0.1:5000/movies/76600/similar-genres`

**Response:**

HTTP Status Code: 200 OK

Response Body:
```
The response body contains a JSON object with the following properties:
    movies: array[object] (optional)
        id: int (optional)
        liked: bool (optional)
        name: str (optional)
        pop: float (optional)
        avg_score: float (optional)
```
Example Response:
```
{
    "movies": [
        {
            "id": 505642,
            "liked": false,
            "name": "Black Panther: Wakanda Forever",
            "pop": 1178.753,
            "avg_score": 7.3
        },
        ...
    ]
}
```

**Error Responses:**
```
HTTP Status Code: 500 Internal Server Error

The response body contains a JSON object with the following properties:
    message: str
Example Response:
    {"message": "An internal server error occurred"}
```
---

### **WithRuntime**

<p>&nbsp;</p>

### WithRuntime GET Method

**Description:** 

This method retrieves information about movies with (roughly) the same runtime as the movie with the given movie id.
The shown amount is limited to 20.

**Request:**

- Endpoint: `/movies/<int:movie_id>/similar-runtime`
- HTTP Method: GET
- URL Parameters:
    * movie_id: int (required) The ID of the movie used to search for movies with the same runtime. This should be an integer value. 
- Example Request:
    `GET http://127.0.0.1:5000/movies/76600/similar-runtime`

**Response:**

HTTP Status Code: 200 OK

Response Body:
```
The response body contains a JSON object with the following properties:
    movies: array[object] (optional)
        id: int (optional)
        liked: bool (optional)
        name: str (optional)
        pop: float (optional)
        avg_score: float (optional)
```
Example Response:
```
{
    "movies": [
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
```

**Error Responses:**
```
HTTP Status Code: 500 Internal Server Error
Response Body:
    The response body contains a JSON object with the following properties:
        message: str
    Example Response:
        {"message": "An internal server error occurred"}
```

---

### **WithActors**

<p>&nbsp;</p>

### WithActors GET Method

**Description:** 

This method retrieves information about movies with the same (two first) actors as the movie with the given movie id.
The shown amount is limited to 20.

**Request:**

- Endpoint: `/movies/<int:movie_id>/similar-actors`
- HTTP Method: GET
- URL Parameters:
    * movie_id: int (required) The ID of the movie used to search for movies with the same (two first) actors. This should be an integer value. 
- Example Request:
    `GET http://127.0.0.1:5000/movies/76600/similar-actors`

**Response:**

HTTP Status Code: 200 OK

Response Body:
```
The response body contains a JSON object with the following properties:
    movies: array[object] (optional)
        id: int (optional)
        liked: bool (optional)
        name: str (optional)
        pop: float (optional)
        avg_score: float (optional)
```
Example Response:
```
{
    "movies": [
        {
            "id": 19995,
            "liked": false,
            "name": "Avatar",
            "pop": 432.199,
            "avg_score": 7.6
        },
        ...
    ]
}
```

**Error Responses:**
```
HTTP Status Code: 500 Internal Server Error
Response Body:
    The response body contains a JSON object with the following properties:
        message: str
    Example Response:
        {"message": "An internal server error occurred"}
```
---

### **MoviesBarplot**

<p>&nbsp;</p>

### MoviesBarplot GET Method

**Description:** 

Generates a link that redirects to a bar chart comparing the average score 
of the given 10 first (popular) movies. If no movie ids are given, it takes the 10 first 'now playing movies' 
from the TMDB API. The bar chart is generated using the QuickChart API.

**Request:**

- Endpoint: `/movies/barplot`
- HTTP Method: GET
- URL Parameters:
    * movie-ids : str (optional) Comma-separated list of existing movie IDs. 
    Only the first 10 IDs will be used to generate the chart. 
    If this parameter is not provided or is an empty string, 
    the API will use the 10 first 'now playing movies' from the TMDB API. 
- Example Request:
    `GET http://127.0.0.1:5000/movies/barplot?movie-ids=76600,67890`

**Response:**

HTTP Status Code: 200 OK

Response Body:
```
    The response body contains a JSON object with the following properties:
        chart_url: str (optional)
```
Example Response:
```
{
    "chart_url": "https://quickchart.io/chart?c={type:'bar',data:{labels:[\"Avatar: The Way of Water\",\"Katha Parayumbol\"],datasets:[{label:'Vote Average Score',data:[7.74,7.531]}]}}"
}
```
**Error Responses:**
```
HTTP Status Code: 500 Internal Server Error
Response Body:
    The response body contains a JSON object with the following properties:
        message: str
    Example Response:
        {"message": "An internal server error occurred"}
```
---

### **Explanatory notes:**

Endpoints:

- resource(Movies, `/`, `/movies`)

- resource(Movie, `/movies/<int:movie_id>`)

    * requirement: Be able to ’delete’ a movie, i.e., the movie won’t be returned from the API after ’deletion’, unless the API is restarted.

    * requirement: Be able to ’like’ and ’un-like’ a movie

- resource(Popular, `/movies/popular`)

    * requirement: List the first x popular movies. (x can be any arbitrary number)

- resource(WithGenres, `/movies/<int:movie_id>/similar-genres`)

    * requirement: Given a movie, return the movies that have exactly the same genres.

- resource(WithRuntime, `/movies/<int:movie_id>/similar-runtime`)

    * requirement: Given a movie, return the movies that have a similar runtime. (You can assume a similar runtime has a maximum of 10 minutes difference)

- resource(WithActors, `/movies/<int:movie_id>/similar-actors`)

    * requirement: Given a movie, return the movies that have two overlapping actor(s). (You can assume the first 2 actors listed)

- resource(MoviesBarplot, `/movies/barplot`)

    * requirement: Given a set of movies, have the ability to generate a barplot comparing the average score of these movies.

<p>&nbsp;</p>

The first 'base' endpoint, connected to the Movies class, is `/movies` (and `/` that does the same for the purpose of RESTfulness). It's a kind of default, it shows the 10 (latest) movies that are now playing.

Further, everything was made as simple as possible so that users of the api can easily navigate through it. We have `/movies/popular` that takes a query parameter 'amount' which specifies the amount of popular movies to show. Should we remove that parameter from the URL, then `/movies/popular` will show the 10 most popular movies by default.

`/movies/<int:movie_id>/similar-genres` retrieves information about movies with exactly the same genres as the movie with the given movie id. For the runtime we use `/movies/<int:movie_id>/similar-runtime` and for the actors we have `/movies/<int:movie_id>/similar-actors`.
Then, `/movies/barplot` uses a query parameter 'movie-ids' to generate a barchart comparing the average scores of the (maximum 10) movies with those id's. Should we remove that parameter from the URL, then `/movies/barplot` will take the movie id's of the 10 (latest) movies that are now playing.

Last but not least, the final endpoint to make the whole thing RESTfull, is `/movies/<int:movie_id>`. Here we can retrieve a specific movie and delete/like/unlike it. This endpoint ensures that if we for example 'hack' and remove the last part of the URL `/movies/<int:movie_id>/similar-genres`, nothing breaks. Additionally, it looks good and simple.

This 'hacking' the URL can be done in any endpoint above, and there will always be a correct response and result. The order in which I did my explanation and the endpoints can be used to verify this.