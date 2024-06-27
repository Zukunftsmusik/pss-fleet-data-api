from datetime import datetime, timedelta, timezone
from typing import Union

import dateutil

from .models.enums import UserAllianceMembership, UserCreateAllianceMembership

PSS_START_DATE: datetime = datetime(2016, 1, 6, tzinfo=timezone.utc)


def add_timezone_utc(dt: datetime) -> datetime:
    return dt.replace(tzinfo=timezone.utc) if dt else None


def convert_alliance_membership_to_int(membership: Union[str, UserAllianceMembership]) -> int:
    if isinstance(membership, str):
        membership = UserAllianceMembership(membership)

    match membership:
        case UserAllianceMembership.NONE:
            return int(UserCreateAllianceMembership.NONE)
        case UserAllianceMembership.CANDIDATE:
            return int(UserCreateAllianceMembership.CANDIDATE)
        case UserAllianceMembership.ENSIGN:
            return int(UserCreateAllianceMembership.ENSIGN)
        case UserAllianceMembership.LIEUTENANT:
            return int(UserCreateAllianceMembership.LIEUTENANT)
        case UserAllianceMembership.MAJOR:
            return int(UserCreateAllianceMembership.MAJOR)
        case UserAllianceMembership.COMMANDER:
            return int(UserCreateAllianceMembership.COMMANDER)
        case UserAllianceMembership.VICE_ADMIRAL:
            return int(UserCreateAllianceMembership.VICE_ADMIRAL)
        case UserAllianceMembership.FLEET_ADMIRAL:
            return int(UserCreateAllianceMembership.FLEET_ADMIRAL)


def convert_datetime_to_seconds(dt: datetime) -> int:
    if not dt:
        return None

    dt = add_timezone_utc(dt)
    if dt < PSS_START_DATE:
        return 0

    return (dt - PSS_START_DATE).seconds


def convert_int_to_alliance_membership(membership: Union[int, UserCreateAllianceMembership]) -> UserAllianceMembership:
    if isinstance(membership, int):
        membership = UserCreateAllianceMembership(membership)

    match membership:
        case UserCreateAllianceMembership.NONE:
            return UserAllianceMembership.NONE
        case UserCreateAllianceMembership.CANDIDATE:
            return UserAllianceMembership.CANDIDATE
        case UserCreateAllianceMembership.ENSIGN:
            return UserAllianceMembership.ENSIGN
        case UserCreateAllianceMembership.LIEUTENANT:
            return UserAllianceMembership.LIEUTENANT
        case UserCreateAllianceMembership.MAJOR:
            return UserAllianceMembership.MAJOR
        case UserCreateAllianceMembership.COMMANDER:
            return UserAllianceMembership.COMMANDER
        case UserCreateAllianceMembership.VICE_ADMIRAL:
            return UserAllianceMembership.VICE_ADMIRAL
        case UserCreateAllianceMembership.FLEET_ADMIRAL:
            return UserAllianceMembership.FLEET_ADMIRAL


def localize_to_utc(dt: datetime) -> datetime:
    return dt.astimezone(timezone.utc) if dt else None


def parse_datetime(dt: Union[datetime, int, str]) -> datetime:
    """Parses a `str` or `int` to `datetime` or returns the passed datetime.

    Args:
        dt (Union[datetime, int, str]): The `str` or `int` to be parsed. If it's an `int`, it represents the seconds since Jan 6th, 2016 12 am.

    Returns:
        datetime: The parsed `datetime`.
    """
    if not value:
        return None
    if isinstance(value, int):
        # If it's an integer value, then it's likely encoded as seconds from Jan 6th, 2016 00:00 UTC
        value = datetime(2016, 1, 6) + timedelta(seconds=value)
    elif isinstance(value, str):
        value = dateutil.parser.parse(value)
    return value
