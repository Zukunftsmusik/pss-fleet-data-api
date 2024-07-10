from datetime import datetime, timedelta, timezone
from typing import Optional, Union

import dateutil

from .config import CONSTANTS
from .models.enums import UserAllianceMembership, UserAllianceMembershipEncoded


def add_timezone_utc(dt: Optional[datetime]) -> datetime:
    """Takes a `datetime` and makes it a timezone-aware `datetime` with timezone UTC, if it's not timezone-aware, yet.

    Args:
        dt (datetime): The `datetime` to be localized to the UTC timezone.

    Raises:
        ValueError: Raised, if parameter `dt` is not of type `datetime`.

    Returns:
        datetime: The timezone-aware `datetime` with the UTC timezone, if the provided `datetime` is not timezone-aware. The provided timezone-aware `datetime`, if it's not `None`. `None`, else.
    """
    if dt is None:
        return None

    if not isinstance(dt, datetime):
        raise TypeError("The parameter `dt` must be of type `datetime`!")

    if not dt.tzinfo:
        return dt.replace(tzinfo=timezone.utc)
    else:
        return dt


def convert_datetime_to_seconds(dt: Optional[datetime]) -> int:
    """Takes a `datetime` and converts it to seconds since the PSS start date.

    Args:
        dt (datetime): The `datetime` to be localized to the UTC timezone.

    Raises:
        TypeError: Raised, if parameter `dt` is not of type `datetime`.

    Returns:
        datetime: The seconds since the PSS start date. 0, if the provided `datetime` is before the PSS start date. `None`, else.
    """
    if dt is None:
        return None

    if not isinstance(dt, datetime):
        raise TypeError("The parameter `dt` must be of type `datetime`!")

    dt = localize_to_utc(dt)
    if dt < CONSTANTS.pss_start_date:
        return 0

    return int((dt - CONSTANTS.pss_start_date).total_seconds())


def decode_alliance_membership(membership: Union[int, UserAllianceMembershipEncoded]) -> UserAllianceMembership:
    """Converts an `int` or `UserCreateAllianceMembership` enum into a `UserAllianceMembership`.

    Args:
        membership (Union[int, UserCreateAllianceMembership]): The alliance membership (member rank) to be decoded.

    Raises:
        ValueError: Raised, if parameter `membership` is `None` or not a valid value for the enum `UserCreateAllianceMembership`.
        TypeError: Raised, if parameter `membership` is not of type `int` or `UserCreateAllianceMembership`.

    Returns:
        UserAllianceMembership: The decoded alliance membership (member rank).
    """
    if membership is None:
        raise ValueError("The parameter `membership` must not be `None`!")

    if isinstance(membership, bool) or not isinstance(membership, (int, UserAllianceMembershipEncoded)):
        raise TypeError("The parameter `membership` must be of type `int` or `UserCreateAllianceMembership`!")

    if isinstance(membership, int):
        membership = UserAllianceMembershipEncoded(membership)

    match membership:
        case UserAllianceMembershipEncoded.NONE:
            return UserAllianceMembership.NONE
        case UserAllianceMembershipEncoded.CANDIDATE:
            return UserAllianceMembership.CANDIDATE
        case UserAllianceMembershipEncoded.ENSIGN:
            return UserAllianceMembership.ENSIGN
        case UserAllianceMembershipEncoded.LIEUTENANT:
            return UserAllianceMembership.LIEUTENANT
        case UserAllianceMembershipEncoded.MAJOR:
            return UserAllianceMembership.MAJOR
        case UserAllianceMembershipEncoded.COMMANDER:
            return UserAllianceMembership.COMMANDER
        case UserAllianceMembershipEncoded.VICE_ADMIRAL:
            return UserAllianceMembership.VICE_ADMIRAL
        case UserAllianceMembershipEncoded.FLEET_ADMIRAL:
            return UserAllianceMembership.FLEET_ADMIRAL


def encode_alliance_membership(membership: Union[str, UserAllianceMembership]) -> int:
    """Converts a `str` or `UserAllianceMembership` enum into an `int`.

    Args:
        membership (Union[str, UserAllianceMembership]): The alliance membership (member rank) to be encoded.

    Raises:
        TypeError: Raised, if the parameter `membership` is not of type `str` or `UserAllianceMembership`.
        ValueError: Raised, if the parameter `membership` is `None` or not a valid value of the `StrEnum` `UserAllianceMembership`.

    Returns:
        int: An `int` representing an encoded `AllianceMembership` value.
    """
    if not membership:
        raise ValueError("Parameter `membership` must not be `None`!")

    if not isinstance(membership, (str, UserAllianceMembership)):
        raise TypeError("Parameter `membership` must be of type `str` or `UserAllianceMembership`!")

    if isinstance(membership, str):
        membership = UserAllianceMembership(membership)

    match membership:
        case UserAllianceMembership.NONE:
            return int(UserAllianceMembershipEncoded.NONE)
        case UserAllianceMembership.CANDIDATE:
            return int(UserAllianceMembershipEncoded.CANDIDATE)
        case UserAllianceMembership.ENSIGN:
            return int(UserAllianceMembershipEncoded.ENSIGN)
        case UserAllianceMembership.LIEUTENANT:
            return int(UserAllianceMembershipEncoded.LIEUTENANT)
        case UserAllianceMembership.MAJOR:
            return int(UserAllianceMembershipEncoded.MAJOR)
        case UserAllianceMembership.COMMANDER:
            return int(UserAllianceMembershipEncoded.COMMANDER)
        case UserAllianceMembership.VICE_ADMIRAL:
            return int(UserAllianceMembershipEncoded.VICE_ADMIRAL)
        case UserAllianceMembership.FLEET_ADMIRAL:
            return int(UserAllianceMembershipEncoded.FLEET_ADMIRAL)


def localize_to_utc(dt: Optional[datetime]) -> datetime:
    """Takes a `datetime` and converts it to a timezone-aware UTC `datetime`.

    Args:
        dt (datetime): The `datetime` to be localized to the UTC timezone.

    Raises:
        ValueError: Raised, if parameter `dt` is not of type `datetime`.

    Returns:
        datetime: The localized `datetime`, if `dt` is not `None`. `None`, else.
    """
    if dt is None:
        return None

    if not isinstance(dt, datetime):
        raise TypeError("The parameter `dt` must be of type `datetime`!")

    if not dt.tzinfo:
        return add_timezone_utc(dt)
    elif dt.tzinfo != timezone.utc:
        return dt.astimezone(timezone.utc)
    else:
        return dt


def parse_datetime(dt: Optional[Union[datetime, int, str]]) -> datetime:
    """Parses a `str` or `int` to `datetime` or returns the passed datetime.

    Args:
        dt (Union[datetime, int, str]): The `str` or `int` to be parsed. If it's an `int`, it represents the seconds since Jan 6th, 2016 12 am.

    Raises:
        ValueError: Raised, if parameter `dt` is not of type `datetime`, `int` or `str`.

    Returns:
        datetime: The parsed `datetime`, if `dt` is not `None`. `None`, else.
    """
    if dt is None:
        return None

    if not isinstance(dt, (datetime, int, str)) or isinstance(dt, bool):
        raise TypeError("The parameter `dt` must be of type `datetime`, `int` or `str`!")

    if isinstance(dt, int):
        # If it's an integer value, then it's likely encoded as seconds from Jan 6th, 2016 00:00 UTC
        return CONSTANTS.pss_start_date + timedelta(seconds=dt)
    elif isinstance(dt, str):
        return dateutil.parser.parse(dt)
    return dt


def remove_timezone(dt: Optional[datetime]) -> datetime:
    """Removes timezone information from a timezone-aware `datetime` object.

    Args:
        dt (datetime): The `datetime` to remove the timezone information from.

    Raises:
        TypeError: Raised, if parameter `dt` is not of type `datetime`.

    Returns:
        datetime: A timezone-naive `datetime` object.
    """
    if dt is None:
        return None

    if not isinstance(dt, datetime):
        raise TypeError("The parameter `dt` must be of type `datetime`!")

    return dt.replace(tzinfo=None)
