from typing import List


class User:
    """Stores user characteristics.

    Attributes:
        identifier (int): unique identifier
        name (str): user name
        viewed (List[int]): movies viewed by user
        purchased (List[int]): movies purchased by user
    """

    def __init__(
        self, identifier: int, name: str, viewed: List[int], purchased: List[int]
    ) -> None:
        self.identifier = identifier
        self.name = name
        self.viewed = viewed
        self.purchased = purchased
