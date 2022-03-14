# imports
from typing import List, Union


class Movie:
    """Stores movie characteristics.

    Attributes:
        identifier (int): unique identifier
        name (str): movie name
        year (int): the year the movie was first released
        genres (List[str]): genres in which the movie is classified
        rating (Union[int,float]): average user review (rating 0-5)
        price (Union[int,float]): price
    """

    def __init__(
        self,
        identifier: int,
        name: str,
        year: int,
        genres: List[str],
        rating: Union[int, float],
        price: Union[int, float],
    ) -> None:
        self.identifier = identifier
        self.name = name
        self.year = year
        self.genres = genres
        self.rating = rating
        self.price = price

    def __str__(self) -> str:
        """Overrides string method.

        Returns:
            str: string representation of Movie instance
        """
        return (
            f"\n====== Movie ======\n"
            f"id: {self.identifier}\n"
            f"name: {self.name}\n"
            f"year: {self.year}\n"
            f"genres: {', '.join(self.genres)}\n"
            f"rating: {self.rating}\n"
            f"price: {self.price}\n"
            f"===================\n"
        )
