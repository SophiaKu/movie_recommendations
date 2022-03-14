# imports
import pandas as pd

# import movie recommendations modules
from movie_recommendations.Movie import Movie
from movie_recommendations.User import User


class DataManager:
    """Manages data associated with users, movies and user sessions.

    Attribues:
        user_data (pd.DataFrame): user data with columns "user_id", "user_name", "viewed", "purchased"
        movie_data (pd.DataFrame): movie data with columns "movie_id", "movie_name", "year", "keyword1", "keyword2", "keyword3", "keyword4", "keyword5", "rating", "price"
        session_data (pd.DataFrame): session data with columns "user_id", "movie_id"
        purchases_of_movies (pd.DataFrame): overview of which films were bought by which users
        genres_of_movies (pd.DataFrame): overview of which films belong to which genres
    """

    def __init__(
        self,
        user_data: pd.DataFrame,
        movie_data: pd.DataFrame,
        session_data: pd.DataFrame,
    ):
        self.user_data = user_data
        self.movie_data = movie_data
        self.session_data = session_data
        self.purchases_of_movies = self.__get_purchases_of_movies()
        self.genres_of_movies = self.__get_genres_of_movies()

    def __get_purchases_of_movies(self) -> pd.DataFrame:
        """Creates an overview of which films were bought by which users.

        Returns:
            pd.DataFrame: overview on purchases by users
        """
        ## proceed user_data
        purchases = self.user_data.copy(deep=True)
        # select relevant columns
        purchases = purchases[["user_id", "purchased"]]
        # rename purchases column
        purchases.rename({"purchased": "movie_id"}, axis=1, inplace=True)
        # split string of column movie_id into list
        purchases["movie_id"] = purchases["movie_id"].str.split(";")
        # explode list where every entry of movie_id is in separate row
        purchases = purchases.explode("movie_id").reset_index(drop=True)
        # convert movie_id to int
        purchases["movie_id"] = purchases["movie_id"].astype(int)
        ## proceed movie_data
        movie_id = self.movie_data.copy(deep=True)
        # select relevant column
        movie_id = movie_id[["movie_id"]]

        ## join movie information to purchase dataframe
        purchases.join(movie_id.set_index("movie_id"), on="movie_id")
        purchases["was_purchased"] = True

        ## return purchases of movies
        return purchases.pivot_table(
            values="was_purchased", index="user_id", columns=["movie_id"]
        ).fillna(0)

    def __get_genres_of_movies(self) -> pd.DataFrame:
        """Creates an overview of which films belong to which genres.

        Returns:
            pd.DataFrame: overview on genres of movies
        """
        ## proceed movie_data
        genres = self.movie_data.copy(deep=True)
        # select_relevant_columns
        genres = genres[
            ["movie_id", "keyword1", "keyword2", "keyword3", "keyword4", "keyword5"]
        ]
        # put every genre of every movie into its own row
        genres = genres.set_index(["movie_id"]).stack()
        genres = genres.reset_index(-1, drop=True).reset_index(name="genre")
        genres["has_genre"] = True

        ## return genres of movies
        return genres.pivot_table(
            values="has_genre", index="genre", columns=["movie_id"]
        ).fillna(0)

    def get_movie_by_movie_id(self, movie_id: int) -> Movie:
        """Generates Movie instance from movie id.

        Args:
            movie_id (int): id of Movie instance

        Returns:
            Movie: created by id
        """
        table_row = self.movie_data[self.movie_data["movie_id"] == movie_id]
        identifier = table_row["movie_id"].iloc[0]
        movie_name = table_row["movie_name"].iloc[0]
        year = table_row["year"].iloc[0]
        genre_columns = ["keyword1", "keyword2", "keyword3", "keyword4", "keyword5"]
        # collect genres from keyword column and filter out 'nan' values
        genres = [
            table_row[column].iloc[0]
            for column in genre_columns
            if not pd.isna(table_row[column].iloc[0])
        ]
        rating = table_row["rating"].iloc[0]
        price = table_row["price"].iloc[0]
        return Movie(identifier, movie_name, year, genres, rating, price)

    def get_user_by_user_id(self, user_id: int) -> User:
        """Generates User instance from user id.

        Args:
            user_id (int): id of User instance

        Returns:
            User: created by id
        """
        table_row = self.user_data[self.user_data["user_id"] == user_id]
        identifier = table_row["user_id"].iloc[0]
        user_name = table_row["user_name"].iloc[0]
        # split entries in viewed into list
        viewed = table_row["viewed"].iloc[0].split(";")
        # convert entries in list into int
        viewed = list(map(int, viewed))
        # split entries in purchased into list
        purchased = table_row["purchased"].iloc[0].split(";")
        # convert entries in list into int
        purchased = list(map(int, purchased))
        return User(identifier, user_name, viewed, purchased)
