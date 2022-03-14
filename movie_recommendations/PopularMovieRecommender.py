# imports
from typing import List
import pandas as pd

# import movie recommendations modules
from movie_recommendations.DataManager import DataManager
from movie_recommendations.Movie import Movie


class PopularMovieRecommender:
    """Manages recommendations based on popularity of movie.

    Attributes:
        data_manager (DataManager): manages data associated with users, movies and user sessions
    """

    def __init__(self, data_manager: DataManager) -> None:
        self.data_manager = data_manager

    def __calculate_rating_scores(self) -> pd.DataFrame:
        """Calculates scores indicating popularity of movies based on user ratings.

        Returns:
            pd.DataFrame: Contains scores based on ratings sorted in ascending order by movie_id. Scores range between lowest score 0 and highest score 1.
        """
        # get highest rating
        highest_rating = self.data_manager.movie_data["rating"].max()
        # get rating for each movie
        scores_rating = self.data_manager.movie_data[["movie_id", "rating"]].copy(
            deep=True
        )
        # get rating score for each movie
        scores_rating["rating"] = scores_rating["rating"].div(highest_rating)
        # rename column containing score
        scores_rating.rename(columns={"rating": "score"}, inplace=True)
        # sort by ascending movie identifier
        scores_rating = scores_rating.sort_values(by="movie_id").reset_index(drop=True)
        return scores_rating

    def __calculate_purchase_scores(self) -> pd.DataFrame:
        """Calculates scores indicating popularity of movies based on how often they were purchased.

        Returns:
            pd.DataFrame: Contains scores based on purchases sorted in ascending order by movie_id. Scores range between lowest score 0 and highest score 1.
        """
        # get total purchase sum
        total_purchases_of_movies = (
            self.data_manager.purchases_of_movies.to_numpy().sum()
        )
        # get purchase sum for each movie
        purchases_of_movie = self.data_manager.purchases_of_movies.sum()
        # get purchases score for each movie by dividing by totoal_purchases_of_movies
        scores_purchases = pd.DataFrame(
            purchases_of_movie.div(total_purchases_of_movies), columns=["score"]
        )
        # join scores with movie ids
        movie_ids = pd.DataFrame(self.data_manager.movie_data["movie_id"])
        scores_purchases = (
            scores_purchases.join(movie_ids, on="movie_id", how="outer")
            .reset_index(drop=True)
            .fillna(0)
        )
        # sort by ascending movie identifier
        scores_purchases = scores_purchases.sort_values(by="movie_id").reset_index(
            drop=True
        )
        return scores_purchases

    def __calculate_total_scores(
        self, weight_rating=0.85
    ) -> pd.DataFrame:  # TODO instead of weight_rating ratio of rating and purchases
        """Calculates score indicating popularity of movie based on purchase rate and user rating. Both factors are weighted.

        Args:
            weight_rating (float, optional): Defines the weighting with which the rating is included in the calculation. Defaults to 0.85.

        Returns:
            pd.DataFrame: Total scores describing popularity of movies. Scores take on values between 1 and 0, where 0 describes the lowest and 1 the highest popularity.
        """
        scores_rating = self.__calculate_rating_scores()
        scores_purchases = self.__calculate_purchase_scores()
        # make sure that input value for weight is in correct interval
        if weight_rating > 1 or weight_rating < 0:
            raise ValueError(f"Input value for weight should be in interval [0, 1].")
        # both weights sum up to 1
        weight_purchases = 1 - weight_rating
        # weight scores
        scores_rating["score"] = scores_rating["score"].mul(weight_rating)
        scores_purchases["score"] = scores_purchases["score"].mul(weight_purchases)
        # calculate total score
        total_scores = scores_rating.copy(deep=True)
        total_scores["score"] = scores_rating["score"] + scores_purchases["score"]
        return total_scores

    def get_popular_movies(self, n_popular_movies: int) -> List[Movie]:
        """Creates list of n_popular_movies most popular movies based on purchase rate and user rating.

        Args:
            n_popular_movies (int): number of popular movies to be returned

        Returns:
            List[Movie]: contains n_popular_movies popular movies
        """
        # receive total scores for movies
        total_movie_scores = self.__calculate_total_scores()
        # sort dataframe by scores in descending order
        movie_scores_sorted_by_score = total_movie_scores.sort_values(
            by="score", ascending=False
        )
        # select ids of n_popular_movies highest scored movies
        highly_scored_movies_id = movie_scores_sorted_by_score["movie_id"].iloc[
            0:n_popular_movies
        ]
        # create empty list to collect n_popular_movies highest scored movie objects
        highly_scored_movies: List[Movie] = []
        for id in highly_scored_movies_id:
            # create movie object
            movie = self.data_manager.get_movie_by_movie_id(id)
            # add movie object to list
            highly_scored_movies.append(movie)
        return highly_scored_movies
