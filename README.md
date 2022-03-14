# Movie Recommendations #

This feature recommends movies in an online movie store.
Recommendations are based on (i) how often a movie was purchased, (ii) how a movie was rated by users, (iii) movies frequently bought together, and (iv) movies with similar genres.

## Running the program ##
1. use Python 3.8 
2. clone via `git clone`
3. install requirements `pip install -r requirements.txt`
4. start program `python main.py`

## File structure ## 
```
| main.py
|
|___ movie_recommendations
|   |   DataManager.py
|   |   Movie.py
|   |   User.py
|   |   PopularMovieRecommender.py
|   |   SimilarMovieRecommender.py
|   |   Printer.py
|
|___ data
    |   Products.txt
    |   Users.txt
    |   CurrentUserSession.txt
```


## Program Flow ##
* A user is randomly selected from current user sessions (CurrentUserSessions.txt)
* Task 1: Recommendation of "recent popular products", based on products that are most frequently purchased and best rated.
    * Based on data in Users.txt, a total popularity score is calculated for every movie in Products.txt
    * Movies with the highest scores are recommended to the user by printing them to the command line.
* Task 2: Recommendation based on "frequently bought together" and similar genres.
    * For a given movie the randomly chosen user in CurrentUserSessions.txt looks at, following information is obtained:
        * correlation of given movie to other movies based on if they were bought together (information on movies that are purchased together obtained from Users.txt)
        * correlation of given movie to other movies based on if they have similar genres (information on movie genres obtained from Products.txt)
    * For both categories ("frequently bought together" and similar genres), recommended movies are printed to the command line
    


