# imports
from typing import List, Literal
import pandas as pd

# import movie recommendations modules
from movie_recommendations.DataManager import DataManager
from movie_recommendations.Movie import Movie


class SimilarMovieRecommender:
    """Manages recommendations based on similarity of movies

    Attributes:
        data_manager (DataManager): manages data associated with users, movies and user sessions
        correlation_threshold (float): correlations with a smaller value are not considered for recommendations
    """

    def __init__(self, data_manager: DataManager, correlation_threshold=0.6) -> None:
        self.data_manager = data_manager
        self.correlation_threshold = correlation_threshold

    def __get_correlations(
        self, movie_id: int, based_on: Literal["purchases", "genres"]
    ) -> pd.DataFrame:
        """Calculates the correlation of a movie with other movies based on common genres or how often they were bought together.

        Args:
            movie_id (int): Identifier of movie
            based_on (Literal['purchases', 'genres']): What correlation should be based on

        Raises:
            ValueError: If based_on is not a supported value
            ValueError: If movie_id is not in corresponding (purchases or genres) data

        Returns:
            pd.DataFrame: Contains all identifiers of movies sorted in descending order by their correlation with the given movie
        """
        if based_on not in ["purchases", "genres"]:
            raise ValueError(
                f"Implementation only supports recommendation based on purchases or genre."
            )
        movie_info = (
            self.data_manager.purchases_of_movies
            if based_on == "purchases"
            else self.data_manager.genres_of_movies
        )
        # if there is no purchases or genre data, raise an error
        if movie_id not in movie_info.keys():
            return (
                pd.DataFrame
            )  # TODO raise ValueError(f"Input identifier is not existent in {based_on} data.")
        correlations = movie_info.corrwith(movie_info[movie_id])
        correlations.dropna(inplace=True)
        correlations = pd.DataFrame(correlations, columns=["correlation"]).reset_index()
        correlations = correlations.sort_values(by="correlation", ascending=False)
        # remove self correlation
        correlations = correlations[correlations["movie_id"] != movie_id]
        # remove correlations below threshold
        correlations = correlations[
            correlations["correlation"] >= self.correlation_threshold
        ]
        return correlations

    def get_similar_movies(
        self, movie: Movie, n_similar_movies=3, based_on=Literal["purchases", "genres"]
    ) -> List[Movie]:
        """Creates list of n_similar_movies most similar movies.

        Returns:
            Literal['purchases', 'genres']]: most similar videos and how that was judged
        """
        if based_on == "purchases":
            # movies are recommened based on jointly purchases
            correlations = self.__get_correlations(
                movie_id=movie.identifier, based_on="purchases"
            )
        elif based_on == "genres":
            # movies are recommended based on similar genres
            correlations = self.__get_correlations(
                movie_id=movie.identifier, based_on="genres"
            )
        else:
            raise ValueError(f"Input '{based_on}' for based_on is not defined.")
        # if no correlation was calculated
        if correlations.empty:
            return []
        high_correlations = correlations[0:n_similar_movies]
        similar_movies_ids = high_correlations["movie_id"].to_list()
        similar_movies = []
        for similar_movie_id in similar_movies_ids:
            movie = self.data_manager.get_movie_by_movie_id(similar_movie_id)
            similar_movies.append(movie)
        return similar_movies
