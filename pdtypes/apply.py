from __future__ import annotations
from functools import cache, partial
from datetime import datetime, timedelta, timezone
from typing import Any, Callable

import numpy as np
import pandas as pd

from pdtypes.error import error_trace
from pdtypes.util.parse import parse_dtype, parse_string, to_utc


"""
TODO: add unit info to timedeltas
"""


def integer_to_float(
    element: int,
    return_type: type = float
) -> float:
    if pd.isnull(element):
        return np.nan
    return return_type(element)


def integer_to_complex(
    element: int,
    return_type: type = complex
) -> complex:
    if pd.isnull(element):
        return np.nan
    return return_type(element)


def integer_to_string(
    element: int,
    return_type: type = str
) -> str:
    if pd.isnull(element):
        return None
    return return_type(element)


def integer_to_boolean(
    element: int,
    force: bool = False,
    return_type: type = bool
) -> bool:
    if pd.isnull(element):
        return pd.NA
    result = return_type(element)
    if result == element or force:
        return result
    err_msg = (f"[{error_trace()}] could not convert int to bool without "
               f"losing information: {repr(element)}")
    raise ValueError(err_msg)


def integer_to_datetime(
    element: int,
    return_type: type = pd.Timestamp
) -> datetime | pd.Timestamp:
    if pd.isnull(element):
        return pd.NaT
    return return_type.fromtimestamp(element, tz=timezone.utc)


def integer_to_timedelta(
    element: int,
    return_type: type = pd.Timedelta
) -> timedelta | pd.Timedelta:
    if pd.isnull(element):
        return pd.NaT
    return return_type(seconds=int(element))


def float_to_integer(
    element: float,
    force: bool = False,
    round: bool = True,
    ftol: float = 1e-6,
    return_type: type = int
) -> int:
    if pd.isnull(element):
        return np.nan
    rounded = np.round(element.real)
    if round or abs(rounded - element) < ftol:
        result = return_type(rounded)
    else:
        result = return_type(element.real)
    if force or abs(result - element) < ftol:
        return result
    err_msg = (f"[{error_trace()}] could not convert float to int without "
               f"losing information: {repr(element)}")
    raise ValueError(err_msg)


def float_to_complex(
    element: float,
    return_type: type = complex
) -> complex:
    if pd.isnull(element):
        return np.nan
    return return_type(element)


def float_to_string(
    element: float,
    return_type: type = str
) -> str:
    if pd.isnull(element):
        return None
    return return_type(element)


def _float_to_boolean(
    element: float,
    force: bool = False,
    ftol: float = 1e-6,
    return_type: type = bool
) -> bool:
    if pd.isnull(element):
        return pd.NA
    rounded = np.round(element.real)
    if abs(rounded - element) < ftol:
        result = return_type(rounded)
    else:
        result = return_type(element.real)
    if force or abs(result - element) < ftol:
        return result
    err_msg = (f"[{error_trace()}] could not convert float to bool without "
               f"losing information: {repr(element)}")
    raise ValueError(err_msg)


def _float_to_datetime(
    element: float,
    return_type: type = pd.Timestamp
) -> datetime | pd.Timestamp:
    if pd.isnull(element):
        return pd.NaT
    return return_type.fromtimestamp(float(element), timezone.utc)


def _float_to_timedelta(
    element: float,
    return_type: type = pd.Timedelta
) -> timedelta | pd.Timedelta:
    if pd.isnull(element):
        return pd.NaT
    return return_type(seconds=float(element))


def _complex_to_integer(
    element: complex,
    round: bool = True,
    force: bool = False,
    ftol: float = 1e-6,
    return_type: type = int
) -> int:
    if pd.isnull(element):
        return np.nan
    rounded = np.round(element.real)
    if round or abs(rounded - element) < ftol:
        result = return_type(rounded)
    else:
        result = return_type(element.real)
    if force or abs(result - element) < ftol:
        return result
    err_msg = (f"[{error_trace()}] could not convert complex to int without "
               f"losing information: {repr(element)}")
    raise ValueError(err_msg)


def _complex_to_float(
    element: complex,
    force: bool = False,
    ftol: float = 1e-6,
    return_type: type = float
) -> float:
    if pd.isnull(element):
        return np.nan
    if force or abs(element.imag) < ftol:
        return return_type(element.real)
    err_msg = (f"[{error_trace()}] could not convert complex to float without "
               f"losing information: {repr(element)}")
    raise ValueError(err_msg)


def _complex_to_string(
    element: complex,
    return_type: type = str
) -> str:
    if pd.isnull(element):
        return pd.NA
    return return_type(element)


def _complex_to_boolean(
    element: complex,
    force: bool = False,
    ftol: float = 1e-6,
    return_type: type = bool
) -> bool:
    if pd.isnull(element):
        return pd.NA
    rounded = np.round(element.real)
    if abs(rounded - element) < ftol:
        result = return_type(rounded)
    else:
        result = return_type(element.real)
    if force or abs(result - element) < ftol:
        return result
    err_msg = (f"[{error_trace()}] could not convert complex to bool without "
               f"losing information: {repr(element)}")
    raise ValueError(err_msg)


def _complex_to_datetime(
    element: complex,
    force: bool = False,
    ftol: float = 1e-6,
    return_type: type = pd.Timestamp
) -> datetime | pd.Timestamp:
    if pd.isnull(element):
        return pd.NaT
    if force or abs(element.imag) < ftol:
        return return_type.fromtimestamp(float(element.real), tz=timezone.utc)
    err_msg = (f"[{error_trace()}] could not convert complex to datetime "
               f"without losing information: {repr(element)}")
    raise ValueError(err_msg)


def _complex_to_timedelta(
    element: complex,
    force: bool = False,
    ftol: float = 1e-6,
    return_type: type = pd.Timedelta
) -> timedelta | pd.Timedelta:
    if pd.isnull(element):
        return pd.NaT
    if force or abs(element.imag) < ftol:
        return return_type(seconds=float(element.real))
    err_msg = (f"[{error_trace()}] could not convert complex to timedelta "
               f"without losing information: {repr(element)}")
    raise ValueError(err_msg)


def _string_to_integer(
    element: str,
    round: bool = True,
    force: bool = False,
    ftol: float = 1e-6,
    format: str | None = None,
    return_type: type = int
) -> int:
    if pd.isnull(element):
        return np.nan
    conversion_map = {
        int:
            lambda x: return_type(x),
        float:
            partial(_float_to_integer, round=round, force=force,
                    ftol=ftol, return_type=return_type),
        complex:
            partial(_complex_to_integer, round=round, force=force,
                    ftol=ftol, return_type=return_type),
        bool:
            partial(_boolean_to_integer, return_type=return_type),
        datetime:
            partial(_datetime_to_integer, round=round, force=force,
                    ftol=ftol, return_type=return_type),
        timedelta:
            partial(_timedelta_to_integer, round=round, force=force,
                    ftol=ftol, return_type=return_type)
    }
    parsed = parse_string(element, format=format)
    parsed_dtype = parse_dtype(type(parsed))
    try:
        return conversion_map[parsed_dtype](parsed)
    except (KeyError, ValueError):
        err_msg = (f"[{error_trace()}] could not convert str to int without "
                   f"losing information: {repr(element)}")
        raise ValueError(err_msg)


def _string_to_float(
    element: str,
    force: bool = False,
    ftol: float = 1e-6,
    format: str | None = None,
    return_type: type = float
) -> float:
    if pd.isnull(element):
        return np.nan
    conversion_map = {
        int:
            partial(_integer_to_float, return_type=return_type),
        float:
            lambda x: return_type(x),
        complex:
            partial(_complex_to_float, force=force, ftol=ftol,
                    return_type=return_type),
        bool:
            partial(_boolean_to_float, return_type=return_type),
        datetime:
            partial(_datetime_to_float, return_type=return_type),
        timedelta:
            partial(_timedelta_to_float, return_type=return_type)
    }
    parsed = parse_string(element, format=format)
    parsed_dtype = parse_dtype(parsed)    
    try:
        return conversion_map[parsed_dtype](parsed)
    except (KeyError, ValueError):
        err_msg = (f"[{error_trace()}] could not convert str to float: "
                f"{repr(element)}")
        raise ValueError(err_msg)


def _string_to_complex(
    element: str,
    format: str | None = None,
    return_type: type = float
) -> complex:
    if pd.isnull(element):
        return np.nan
    conversion_map = {
        int:
            partial(_integer_to_complex, return_type=return_type),
        float:
            partial(_float_to_complex, return_type=return_type),
        complex:
            lambda x: return_type(x),
        bool:
            partial(_boolean_to_complex, return_type=return_type),
        datetime:
            partial(_datetime_to_complex, return_type=return_type),
        timedelta:
            partial(_timedelta_to_complex, return_type=return_type)
    }
    parsed = parse_string(element, format=format)
    parsed_dtype = parse_dtype(parsed)
    try:
        return conversion_map[parsed_dtype](parsed)
    except (KeyError, ValueError):
        err_msg = (f"[{error_trace()}] could not convert str to complex: "
                   f"{repr(element)}")
        raise ValueError(err_msg)


def _string_to_boolean(
    element: str,
    force: bool = False,
    ftol: float = 1e-6,
    format: str | None = None,
    return_type: type = bool
) -> bool:
    if pd.isnull(element):
        return pd.NA
    conversion_map = {
        int:
            partial(_integer_to_boolean, force=force, return_type=return_type),
        float:
            partial(_float_to_boolean, force=force, ftol=ftol,
                    return_type=return_type),
        complex:
            partial(_complex_to_boolean, force=force, ftol=ftol,
                    return_type=return_type),
        bool:
            lambda x: return_type(x),
        datetime:
            partial(_datetime_to_boolean, force=force, ftol=ftol,
                    return_type=return_type),
        timedelta:
            partial(_timedelta_to_boolean, force=force, ftol=ftol,
                    return_type=return_type)
    }
    parsed = parse_string(element, format=format)
    parsed_dtype = parse_dtype(parsed)
    try:
        return conversion_map[parsed_dtype](parsed)
    except (KeyError, ValueError):
        err_msg = (f"[{error_trace()}] could not convert str to bool: "
                   f"{repr(element)}")
        raise ValueError(err_msg)


def _string_to_datetime(
    element: str,
    force: bool = False,
    ftol: float = 1e-6,
    format: str | None = None,
    return_type: type = pd.Timestamp
) -> pd.Timestamp | datetime:
    if pd.isnull(element):
        return pd.NaT
    conversion_map = {
        int:
            partial(_integer_to_datetime, return_type=return_type),
        float:
            partial(_float_to_datetime, return_type=return_type),
        complex:
            partial(_complex_to_datetime, force=force, ftol=ftol,
                    return_type=return_type),
        bool:
            partial(_boolean_to_datetime, return_type(return_type)),
        datetime:
            lambda x: x if return_type == datetime else return_type(x),
        timedelta:
            partial(_timedelta_to_datetime, return_type=return_type)
    }
    parsed = parse_string(element, format=format)
    parsed_dtype = parse_dtype(parsed)
    try:
        return conversion_map[parsed_dtype](parsed)
    except (KeyError, ValueError):
        err_msg = (f"[{error_trace()}] could not convert str to datetime: "
                   f"{repr(element)}")
        raise ValueError(err_msg)


def _string_to_timedelta(
    element: str,
    force: bool = False,
    format: str | None = None,
    return_type: type = pd.Timedelta
) -> pd.Timedelta | timedelta:
    if pd.isnull(element):
        return pd.NaT
    conversion_map = {
        int:
            partial(_integer_to_timedelta, return_type=return_type),
        float:
            partial(_float_to_timedelta, return_type=return_type),
        complex:
            partial(_complex_to_timedelta, force=force,
                    return_type=return_type),
        bool:
            partial(_boolean_to_timedelta, return_type=return_type),
        datetime:
            partial(_datetime_to_timedelta, return_type=return_type),
        timedelta:
            lambda x: return_type(seconds=element.total_seconds())
    }
    parsed = parse_string(element, format=format)
    parsed_dtype = parse_dtype(parsed)
    try:
        return conversion_map[parsed_dtype](parsed)
    except (KeyError, ValueError):
        err_msg = (f"[{error_trace()}] could not convert str to timedelta: "
                   f"{repr(element)}")
        raise ValueError(err_msg)


def _boolean_to_integer(
    element: bool,
    return_type: type = int
) -> int:
    if pd.isnull(element):
        return np.nan
    return return_type(element)


def _boolean_to_float(
    element: bool,
    return_type: type = float
) -> float:
    if pd.isnull(element):
        return np.nan
    return return_type(element)


def _boolean_to_complex(
    element: bool,
    return_type: type = complex
) -> complex:
    if pd.isnull(element):
        return np.nan
    return return_type(element)


def _boolean_to_string(
    element: bool,
    return_type: type = str
) -> str:
    if pd.isnull(element):
        return pd.NA
    return return_type(element)


def _boolean_to_datetime(
    element: bool,
    return_type: type = pd.Timestamp
) -> pd.Timestamp | datetime:
    if pd.isnull(element):
        return pd.NaT
    return return_type.fromtimestamp(float(element), tz=timezone.utc)


def _boolean_to_timedelta(
    element: bool,
    return_type: type = pd.Timedelta
) -> pd.Timedelta | timedelta:
    if pd.isnull(element):
        return pd.NaT
    return return_type(seconds=float(element))


def _datetime_to_integer(
    element: pd.Timestamp | datetime,
    round: bool = True,
    force: bool = False,
    ftol: float = 1e-6,
    return_type: type = int
) -> int:
    if pd.isnull(element):
        return np.nan
    timestamp = to_utc(element).timestamp()
    rounded = np.round(timestamp)
    if round or abs(rounded - timestamp) < ftol:
        result = return_type(rounded)
    else:
        result = return_type(timestamp)
    if force or abs(result - timestamp) < ftol:
        return result
    err_msg = (f"[{error_trace()}] could not convert datetime to int without "
               f"losing information: {repr(element)}")
    raise ValueError(err_msg)


def _datetime_to_float(
    element: pd.Timestamp | datetime,
    return_type: type = float
) -> float:
    if pd.isnull(element):
        return np.nan
    return return_type(to_utc(element).timestamp())


def _datetime_to_complex(
    element: pd.Timestamp | datetime,
    return_type: type = complex
) -> complex:
    if pd.isnull(element):
        return np.nan
    return return_type(to_utc(element).timestamp())


def _datetime_to_string(
    element: pd.Timestamp | datetime,
    format: str | None = None,
    return_type: type = str
) -> str:
    if pd.isnull(element):
        return pd.NA
    if format is None:
        return return_type(to_utc(element).isoformat())
    return return_type(to_utc(element).strftime(format))


def _datetime_to_boolean(
    element: pd.Timestamp | datetime,
    force: bool = False,
    ftol: float = 1e-6,
    return_type: type = bool
) -> bool:
    if pd.isnull(element):
        return pd.NA
    timestamp = to_utc(element).timestamp()
    result = return_type(timestamp)
    if abs(result - timestamp) < ftol or force:
        return result
    err_msg = (f"[{error_trace()}] could not convert datetime to bool without "
               f"losing information: {repr(element)}")
    raise ValueError(err_msg)


def _datetime_to_timedelta(
    element: pd.Timestamp | datetime,
    return_type: type = pd.Timedelta
) -> pd.Timedelta | timedelta:
    if pd.isnull(element):
        return pd.NaT
    return return_type(seconds=to_utc(element).timestamp())


def _timedelta_to_integer(
    element: pd.Timedelta | timedelta,
    round: bool = True,
    force: bool = False,
    ftol: float = 1e-6,
    return_type: type = int
) -> int:
    if pd.isnull(element):
        return np.nan
    seconds = element.total_seconds()
    rounded = np.round(seconds)
    if round or abs(rounded - seconds) < ftol:
        result = return_type(rounded)
    else:
        result = return_type(seconds)
    if force or abs(result - seconds) < ftol:
        return result
    err_msg = (f"[{error_trace()}] could not convert timedelta to int without "
               f"losing information: {repr(element)}")
    raise ValueError(err_msg)


def _timedelta_to_float(
    element: pd.Timedelta | timedelta,
    return_type: type = float
) -> float:
    if pd.isnull(element):
        return np.nan
    return return_type(element.total_seconds())


def _timedelta_to_complex(
    element: pd.Timedelta | timedelta,
    return_type: type = complex
) -> complex:
    if pd.isnull(element):
        return np.nan
    return return_type(element.total_seconds())


def _timedelta_to_string(
    element: pd.Timedelta | timedelta,
    return_type: type = str
) -> str:
    if pd.isnull(element):
        return pd.NA
    return return_type(element)


def _timedelta_to_boolean(
    element: pd.Timedelta | timedelta,
    force: bool = False,
    ftol: float = 1e-6,
    return_type: type = bool
) -> bool:
    if pd.isnull(element):
        return pd.NA
    seconds = element.total_seconds()
    result = return_type(seconds)
    if abs(result - seconds) < ftol or force:
        return result
    err_msg = (f"[{error_trace()}] could not convert timedelta to bool: "
               f"{repr(element)}")
    raise ValueError(err_msg)


def _timedelta_to_datetime(
    element: pd.Timedelta | timedelta,
    return_type: type = pd.Timestamp
) -> pd.Timestamp | datetime:
    if pd.isnull(element):
        return pd.NaT
    return return_type.fromtimestamp(element.total_seconds(), tz=timezone.utc)


@cache
def to_integer(
    element: Any,
    round: bool = False,
    force: bool = False,
    ftol: float = 1e-6,
    format: str | None = None,
    return_type: type = int
) -> np.nan | int:
    if pd.isnull(element):
        return np.nan
    conversion_map = {
        int:
            lambda x: return_type(element),
        float:
            partial(_float_to_integer, round=round, force=force, ftol=ftol,
                    return_type=return_type),
        complex:
            partial(_complex_to_integer, round=round, force=force, ftol=ftol,
                    return_type=return_type),
        str:
            partial(_string_to_integer, round=round, force=force, ftol=ftol,
                    format=format, return_type=return_type),
        bool:
            partial(_boolean_to_integer, return_type=return_type),
        datetime:
            partial(_datetime_to_integer, round=round, force=force, ftol=ftol,
                    return_type=return_type),
        timedelta:
            partial(_timedelta_to_integer, round=round, force=force, ftol=ftol,
                    return_type=return_type),
        object:
            lambda x: return_type(int(x))
    }
    from_type = parse_dtype(type(element))
    try:
        return conversion_map[from_type](element)
    except (KeyError, ValueError) as err:
        err_msg = (f"[{error_trace()}] could not convert element to int: "
                   f"{repr(element)}")
        raise ValueError(err_msg) from err


@cache
def to_float(
    element: Any,
    force: bool = False,
    ftol: float = 1e-6,
    format: str | None = None,
    return_type: type = float
) -> np.nan | float:
    if pd.isnull(element):
        return np.nan
    conversion_map = {
        int:
            partial(_integer_to_float, return_type=return_type),
        float:
            lambda x: return_type(x),
        complex:
            partial(_complex_to_float, force=force, ftol=ftol,
                    return_type=return_type),
        str:
            partial(_string_to_float, force=force, ftol=ftol,
                    format=format, return_type=return_type),
        bool:
            partial(_boolean_to_float, return_type=return_type),
        datetime:
            partial(_datetime_to_float, return_type=return_type),
        timedelta:
            partial(_timedelta_to_float, return_type=return_type),
        object:
            lambda x: return_type(float(x))
    }
    from_type = parse_dtype(type(element))
    try:
        return conversion_map[from_type](element)
    except (KeyError, ValueError) as err:
        err_msg = (f"[{error_trace()}] could not convert element to float: "
                   f"{repr(element)}")
        raise ValueError(err_msg) from err


@cache
def to_complex(
    element: Any,
    format: str | None = None,
    return_type: type = complex
) -> np.nan | complex:
    if pd.isnull(element):
        return np.nan
    conversion_map = {
        int:
            partial(_integer_to_complex, return_type=return_type),
        float:
            partial(_float_to_complex, return_type=return_type),
        complex:
            lambda x: return_type(x),
        str:
            partial(_string_to_complex, format=format, return_type=return_type),
        bool:
            partial(_boolean_to_complex, return_type=return_type),
        datetime:
            partial(_datetime_to_complex, return_type=return_type),
        timedelta:
            partial(_timedelta_to_complex, return_type=return_type),
        object:
            lambda x: return_type(complex(x))
    }
    from_type = parse_dtype(type(element))
    try:
        return conversion_map[from_type](element)
    except (KeyError, ValueError) as err:
        err_msg = (f"[{error_trace()}] could not convert element to complex: "
                   f"{repr(element)}")
        raise ValueError(err_msg)


@cache
def to_boolean(
    element: Any,
    force: bool = False,
    ftol: float = 1e-6,
    format: str | None = None,
    return_type: type = bool
) -> pd.NA | bool:
    if pd.isnull(element):
        return pd.NA
    conversion_map = {
        int:
            partial(_integer_to_boolean, force=force, ftol=ftol,
                    return_type=return_type),
        float:
            partial(_float_to_boolean, force=force, ftol=ftol,
                    return_type=return_type),
        complex:
            partial(_complex_to_boolean, force=force, ftol=ftol,
                    return_type=return_type),
        str:
            partial(_string_to_boolean, force=force, ftol=ftol,
                    format=format, return_type=return_type),
        bool:
            lambda x: return_type(x),
        datetime:
            partial(_datetime_to_boolean, force=force, ftol=ftol,
                    return_type=return_type),
        timedelta:
            partial(_timedelta_to_boolean, force=force, ftol=ftol,
                    return_type=return_type),
        object:
            lambda x: return_type(bool(x))
    }
    from_type = parse_dtype(type(element))
    try:
        return conversion_map[from_type](element)
    except (KeyError, ValueError) as err:
        err_msg = (f"[{error_trace()}] could not convert element to bool: "
                   f"{repr(element)}")
        raise ValueError(err_msg) from err


@cache
def to_string(
    element: Any,
    format: str | None = None,
    return_type: type = str
) -> pd.NA | str:
    if pd.isnull(element):
        return pd.NA
    conversion_map = {
        int:
            partial(_integer_to_string, return_type=return_type),
        float:
            partial(_float_to_string, return_type=return_type),
        complex:
            partial(_complex_to_string, return_type=return_type),
        str:
            lambda x: return_type(x),
        bool:
            partial(_boolean_to_string, return_type=return_type),
        datetime:
            partial(_datetime_to_string, format=format,
                    return_type=return_type),
        timedelta:
            partial(_timedelta_to_string, return_type=return_type),
        object:
            lambda x: return_type(str(x))
    }
    from_type = parse_dtype(type(element))
    try:
        return conversion_map[from_type](element)
    except (KeyError, ValueError) as err:
        err_msg = (f"[{error_trace()}] could not convert element to string: "
                   f"{repr(element)}")
        raise ValueError(err_msg) from err


@cache
def to_datetime(
    element: Any,
    force: bool = False,
    ftol: float = 1e-6,
    format: str | None = None,
    func: Callable | None = None,
    return_type: type = pd.Timestamp
) -> pd.NaT | pd.Timestamp | datetime:
    if pd.isnull(element):
        return pd.NaT
    conversion_map = {
        int:
            partial(_integer_to_datetime, return_type=return_type),
        float:
            partial(_float_to_datetime, return_type=return_type),
        complex:
            partial(_complex_to_datetime, force=force, ftol=ftol,
                    return_type=return_type),
        str:
            partial(_string_to_datetime, force=force, ftol=ftol,
                    format=format, return_type=return_type),
        bool:
            partial(_boolean_to_datetime, return_type=return_type),
        datetime:
            lambda x: return_type.fromtimestamp(to_utc(x).timestamp(),
                                                timezone.utc),
        timedelta:
            partial(_timedelta_to_datetime, return_type=return_type)
    }
    from_type = parse_dtype(type(element))
    try:
        return conversion_map[from_type](element)
    except (KeyError, ValueError) as err:
        err_msg = (f"[{error_trace()}] could not convert element to datetime: "
                   f"{repr(element)}")
        raise ValueError(err_msg) from err


@cache
def to_timedelta(
    element: Any,
    force: bool = False,
    ftol: float = 1e-6,
    return_type: type = pd.Timedelta
) -> pd.NaT | pd.Timedelta:
    if pd.isnull(element):
        return pd.NaT
    conversion_map = {
        int:
            partial(_integer_to_timedelta, return_type=return_type),
        float:
            partial(_float_to_timedelta, return_type=return_type),
        complex:
            partial(_complex_to_timedelta, force=force, ftol=ftol,
                    return_type=return_type),
        str:
            partial(_string_to_timedelta, force=force, ftol=ftol,
                    return_type=return_type),
        bool:
            partial(_boolean_to_timedelta, return_type=return_type),
        datetime:
            partial(_datetime_to_timedelta, return_type=return_type),
        timedelta:
            lambda x: return_type(seconds=x.total_seconds())
    }
    from_type = parse_dtype(type(element))
    try:
        return conversion_map[from_type](element)
    except (KeyError, ValueError) as err:
        err_msg = (f"[{error_trace()}] could not convert element to timedelta: "
                   f"{repr(element)}")
        raise ValueError(err_msg) from err
