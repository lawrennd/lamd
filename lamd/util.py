import datetime
import os
from typing import Any, List, Optional, Union

import pandas as pd
from lynguine.config.context import Context
from lynguine.log import Logger

cntxt = Context(name="lamd")
log = Logger(name=__name__, level=cntxt["logging"]["level"], filename=cntxt["logging"]["filename"])

SINCE_YEAR: Optional[int] = None


def set_since_year(year: int) -> None:
    """Set the global SINCE_YEAR variable."""
    global SINCE_YEAR
    SINCE_YEAR = year


def get_since_year() -> Optional[int]:
    """Get the global SINCE_YEAR variable."""
    global SINCE_YEAR
    return SINCE_YEAR


def file_type(filename: str) -> str:
    """Return the file type based on the filename extension."""
    _, ext = os.path.splitext(filename)
    return ext.lower()


# Preprocessors
def convert_datetime(df: pd.DataFrame, columns: Union[str, List[str]]) -> pd.DataFrame:
    """Preprocessor to set datetime type on columns."""
    if isinstance(columns, str):
        columns = [columns]
    for column in columns:
        if column in df.columns:
            df[column] = pd.to_datetime(df[column])
    return df


def convert_int(df: pd.DataFrame, columns: Union[str, List[str]]) -> pd.DataFrame:
    """Preprocessor to set integer type on columns."""
    if isinstance(columns, str):
        columns = [columns]
    for column in columns:
        if column in df.columns:
            df[column] = pd.to_numeric(df[column]).apply(lambda x: int(x) if not pd.isna(x) else pd.NA).astype("Int64")
    return df


def convert_string(df: pd.DataFrame, columns: Union[str, List[str]]) -> pd.DataFrame:
    """Preprocessor to set string type on columns."""
    if isinstance(columns, str):
        columns = [columns]
    for column in columns:
        if column in df.columns:
            df[column] = df[column].apply(lambda x: str(x) if not pd.isna(x) else pd.NA)
    return df


def convert_year_iso(df: pd.DataFrame, column: str = "year", month: int = 1, day: int = 1) -> pd.DataFrame:
    """Preprocessor to set string type on columns."""

    def year_to_iso(field: Union[int, str, datetime.date]) -> datetime.date:
        """Convert a year field to an iso date using the provided month and day."""
        if isinstance(field, int):
            log.debug(f'Returning "int" from form "{field}"')
            return datetime.date(year=field, month=month, day=day)
        elif isinstance(field, str):
            try:
                year = int(field)  # Try it as string year
                log.debug(f'Returning "str" from form "{field}"')
                return datetime.date(year=year, month=month, day=day)
            except ValueError:
                log.debug(f'Returning "str" from form "{field}"')
                dt = datetime.datetime.strptime(field, "%Y-%m-%d")  # Try it as string YYYY-MM-DD
                return dt.date()
        elif isinstance(field, datetime.date):
            log.debug(f'Returning "datetime.date" from form "{field}"')
            return field
        else:
            raise TypeError(f'Expecting type of int or str or datetime but found "{type(field)}"')

    df[column] = df[column].apply(year_to_iso)
    return df


# Augmentors
def addmonth(df: pd.DataFrame, newcolumn: str = "month", source: str = "date") -> pd.DataFrame:
    """Add month column based on source date field."""
    df[newcolumn] = df[source].apply(lambda x: x.month_name() if x is not None else pd.NA)
    return df


def addyear(df: pd.DataFrame, newcolumn: str = "year", source: str = "date") -> pd.DataFrame:
    """Add year column and based on source date field."""
    df[newcolumn] = df[source].apply(lambda x: x.year if x is not None else pd.NA)
    return df


def augmentmonth(df: pd.DataFrame, newcolumn: str = "month", source: str = "date") -> pd.DataFrame:
    """Augment the  month column based on source date field."""
    for index, entry in df.iterrows():
        if pd.isna(df.loc[index, newcolumn]) and not pd.isna(df.loc[index, source]):
            df.loc[index, newcolumn] = df.loc[index, source].month_name()
    return df


def augmentyear(df: pd.DataFrame, newcolumn: str = "year", source: str = "date") -> pd.DataFrame:
    """Augment the year column based on source date field."""
    for index, entry in df.iterrows():
        if pd.isna(df.loc[index, newcolumn]) and not pd.isna(df.loc[index, source]):
            df.loc[index, newcolumn] = df.loc[index, source].year
    return df


def augmentcurrency(df: pd.DataFrame, newcolumn: str = "amountstr", source: str = "amount", sf: int = 0) -> pd.DataFrame:
    """Preprocessor to set integer type on columns."""
    fstr = f"{{0:,.{sf}f}}"
    df[newcolumn] = df[source].apply(lambda x: fstr.format(x))
    return df


def addsupervisor(df: pd.DataFrame, column: str, supervisor: str) -> pd.DataFrame:
    df[column] = df[column].fillna(supervisor)
    return df


# Sorters
def ascending(df: pd.DataFrame, by: Union[str, List[str]]) -> pd.DataFrame:
    """Sort in ascending order"""
    return df.sort_values(by=by, ascending=True)


def descending(df: pd.DataFrame, by: Union[str, List[str]]) -> pd.DataFrame:
    """Sort in descending order"""
    return df.sort_values(by=by, ascending=False)


# Filters
def recent(df: pd.DataFrame, column: str = "year") -> pd.Series:
    """Filter on year of item"""
    return df[column] >= get_since_year()


def current(df: pd.DataFrame, start: str = "start", end: str = "end", current: Optional[str] = None) -> pd.Series:
    """Filter on whether item is current"""
    now = pd.to_datetime(datetime.datetime.now().date())
    within = (df[start] <= now) & (pd.isna(df[end]) | (df[end] >= now))
    if current is not None:
        return within | (~df[current].isna() & df[current])
    else:
        return within


def former(df: pd.DataFrame, end: str = "end") -> pd.Series:
    """Filter on whether item is current"""
    now = pd.to_datetime(datetime.datetime.now().date())
    return df[end] < now


def onbool(df: pd.DataFrame, column: str = "current", invert: bool = False) -> pd.Series:
    """Filter on whether column is positive (or negative if inverted)"""
    if invert:
        return ~df[column]
    else:
        return df[column]


def columnis(df: pd.DataFrame, column: str, value: Any) -> pd.Series:
    """Filter on whether item is equal to a given value"""
    return df[column] == value


def columncontains(df: pd.DataFrame, column: str, value: Any) -> pd.Series:
    """Filter on whether column contains a given value"""
    colis = columnis(df, column, value)
    return colis | df[column].apply(lambda x: (x == value).any() if type(x == value) is not bool else (x == value))
