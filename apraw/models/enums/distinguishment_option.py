from enum import Enum


class DistinguishmentOption(Enum):
    """
    An enum for the distinguishment types.

     - YES | "yes"
     - NO | "no"
     - ADMIN | "admin"
     - SPECIAL | "special"
    """
    YES = "yes"
    NO = "no"
    ADMIN = "admin"
    SPECIAL = "special"
