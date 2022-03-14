# imports
from typing import List, Literal

# import movie recommendations modules
from movie_recommendations.Movie import Movie


class Printer:
    """Helper class to display results."""

    @staticmethod
    def display_recent_popular_movies(
        popular_movies: List[Movie],
    ) -> None: 
        """Prints text that recommends recent popular products.

        Args:
            popular_movies (List[Movie]): contains movies with highest scores
        """
        # create text to be displayed
        text_to_be_displayed = f"---------> Checkout our most popular movies"
        for n_movie, movie in enumerate(popular_movies):
            if n_movie < (len(popular_movies) - 1):
                # add movie name to text_to_be_displayed
                text_to_be_displayed += f' "{movie.name}",'
            else:
                # add last movie name to text_to_be_displayed
                text_to_be_displayed += f' and "{movie.name}"! <---------'
        print(text_to_be_displayed)

    @staticmethod
    def display_similar_movies(
        movie: Movie,
        similar_movies: List[Movie],
        based_on: Literal["purchases", "genres"],
    ) -> None:
        """Prints text that recommends similar movies either based on similar genres or based on bought together.

        Args:
            movie (Movie): movie the recommendation is based on
            similar_movies (List[Movie]): recommendations based on given movie
            based_on (Literal['purchases', 'genres']): what recommendation is based on

        Raises:
            ValueError: if based_on is not a supported value
        """
        if based_on not in ["purchases", "genres"]:
            raise ValueError(
                f"Implementation only supports recommendation based on purchases or genre."
            )
        if based_on == "purchases":
            if not similar_movies:
                print(
                    f'---------> "{movie.name}" was not yet bought together with other movies. <---------'
                )
                return
            text_to_be_displayed = (
                f'---------> "{movie.name}" was frequently bought together with'
            )
        else:
            # this can be the case when correlations below threshold
            if not similar_movies:
                print(
                    f'---------> "{movie.name}" has no similar gernes to other movies. <---------'
                )
                return
            text_to_be_displayed = (
                f'---------> Movies with most similar genres to "{movie.name}" are:'
            )
        # append text_to_be_displayed with movies to be printed
        for n_similar_movie, similar_movie in enumerate(similar_movies):
            if n_similar_movie < (len(similar_movies) - 1):
                # add movie name to text_to_be_displayed
                text_to_be_displayed += f' "{similar_movie.name}",'
            else:
                # add last movie name to text_to_be_displayed
                text_to_be_displayed += f' and "{similar_movie.name}"! <---------'
        print(text_to_be_displayed)
