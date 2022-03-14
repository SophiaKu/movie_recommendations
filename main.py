# imports
import pandas as pd
from os.path import abspath

# import movie recommendations modules
from movie_recommendations.DataManager import DataManager
from movie_recommendations.PopularMovieRecommender import PopularMovieRecommender
from movie_recommendations.Printer import Printer
from movie_recommendations.SimilarMovieRecommender import SimilarMovieRecommender

if __name__ == "__main__":
    # read user data, skip spaces after delimiter
    user_data = pd.read_csv(
        abspath("./data/Users.txt"),
        sep=",",
        header=None,
        names=["user_id", "user_name", "viewed", "purchased"],
        skipinitialspace=True,
    )
    # read product data, skip spaces after delimiter
    movie_data = pd.read_csv(
        abspath("./data/Products.txt"),
        sep=",",
        header=None,
        names=[
            "movie_id",
            "movie_name",
            "year",
            "keyword1",
            "keyword2",
            "keyword3",
            "keyword4",
            "keyword5",
            "rating",
            "price",
        ],
        skipinitialspace=True,
    )
    # read session data, skip spaces after delimiter
    session_data = pd.read_csv(
        abspath("./data/CurrentUserSession.txt"),
        sep=",",
        header=None,
        names=["user_id", "movie_id"],
        skipinitialspace=True,
    )

    # create data_manager storing relevant information about users, movies and session data
    data_manager = DataManager(user_data, movie_data, session_data)

    """Welcome User
    """
    # for demonstration of program, one session is randomly chosen from session data
    session = session_data.sample()
    # access user id
    user_id = int(session["user_id"])
    # access user
    user = data_manager.get_user_by_user_id(user_id)
    # access movie id
    movie_id = int(session["movie_id"])
    # movie_id = 8 # remove comment for testing 'frequently bought together'
    # access movie
    movie = data_manager.get_movie_by_movie_id(movie_id)

    # welcome user
    print(f"\n\n++++++++++ Welcome back, {user.name}! ++++++++++\n\n")
    print(f"You are currently looking at {movie}")

    """Taks 1: Recommendation based on movie popularity (high purchase rate and user review).
    """
    # get most popular movies
    popular_movie_recommender = PopularMovieRecommender(data_manager)
    popular_movies = popular_movie_recommender.get_popular_movies(n_popular_movies=3)
    # print most popular movies
    printer = Printer()
    printer.display_recent_popular_movies(popular_movies)

    """Task 2: Recommendation based on similar genres and 'frequently bought together'.
    """
    # generate recommender for similar movies
    similar_movie_recommender = SimilarMovieRecommender(
        data_manager, correlation_threshold=0.4
    )
    # movies 'frequently bought together'
    movies_purchased_togther = similar_movie_recommender.get_similar_movies(
        movie, n_similar_movies=3, based_on="purchases"
    )
    printer.display_similar_movies(
        movie, movies_purchased_togther, based_on="purchases"
    )
    # movies with similar genres
    movies_similar_genres = similar_movie_recommender.get_similar_movies(
        movie, n_similar_movies=3, based_on="genres"
    )
    printer.display_similar_movies(movie, movies_similar_genres, based_on="genres")
