import sys
import os
import datetime

import argparse
import numpy as np

import pandas as pd

import lynguine.access as access

from lynguine.config.context import Context
from lynguine.log import Logger
from lynguine.util.misc import remove_nan


cntxt = Context(name="lamd")
log = Logger(name=__name__, level=cntxt["logging"]["level"], filename=cntxt["logging"]["filename"])

SINCE_YEAR = None

def set_since_year(year):
    """Set the global SINCE_YEAR variable."""
    global SINCE_YEAR
    SINCE_YEAR = year

def get_since_year():
    """Get the global SINCE_YEAR variable."""
    global SINCE_YEAR
    return SINCE_YEAR


def file_type(filename):
    """Return the file type based on the filename extension."""
    _, ext = os.path.splitext(filename)
    return ext.lower()


## Preprocessors
def convert_datetime(df, columns):
    """Preprocessor to set datetime type on columns."""
    if type(columns) is not list:
        columns = [columns]
    for column in columns:
        if column in df.columns:
            df[column] = pd.to_datetime(df[column])
    return df


def convert_int(df, columns):
    """Preprocessor to set integer type on columns."""
    if type(columns) is not list:
        columns = [columns]
    for column in columns:
        if column in df.columns:
            df[column] = pd.to_numeric(df[column]).apply(lambda x: int(x) if not pd.isna(x) else pd.NA).astype("Int64")
    return df


def convert_string(df, columns):
    """Preprocessor to set string type on columns."""
    if type(columns) is not list:
        columns = [columns]
    for column in columns:
        if column in df.columns:
            df[column] = df[column].apply(lambda x: str(x) if not pd.isna(x) else pd.NA)
    return df


def convert_year_iso(df, column="year", month=1, day=1):
    """Preprocessor to set string type on columns."""

    def year_to_iso(field):
        """Convert a year field to an iso date using the provided month and day."""
        type_field = type(field)
        if type_field is int:  # Assume it is integer year
            log.debug(f'Returning "{type_field}" from form "{field}"')
            dt = datetime.datetime(year=field, month=month, day=day)
        elif type_field is str:
            try:
                year = int(field)  # Try it as string year
                log.debug(f'Returning "{type_field}" from form "{field}"')
                dt = datetime.datetime(year=year, month=month, day=day)
            except TypeError as e:
                log.debug(f'Returning "{type_field}" from form "{field}"')
                dt = datetime.datetime.strptime(field, "%Y-%m-%d")  # Try it as string YYYY-MM-DD
        elif type_field is datetime.date:
            log.debug(f'Returning "{type_field}" from form "{field}"')
            return field
        else:
            raise TypeError(f'Expecting type of int or str or datetime but found "{type_field}"')
        return dt

    df[column] = df[column].apply(year_to_iso)
    return df


## Augmentors
def addmonth(df, newcolumn="month", source="date"):
    """Add month column based on source date field."""
    df[newcolumn] = df[source].apply(lambda x: x.month_name() if x is not None else pd.NA)
    return df


def addyear(df, newcolumn="year", source="date"):
    """Add year column and based on source date field."""
    df[newcolumn] = df[source].apply(lambda x: x.year if x is not None else pd.NA)
    return df


def augmentmonth(df, newcolumn="month", source="date"):
    """Augment the  month column based on source date field."""
    for index, entry in df.iterrows():
        if pd.isna(df.loc[index, newcolumn]) and not pd.isna(df.loc[index, source]):
            df.loc[index, newcolumn] = df.loc[index, source].month_name()
    return df


def augmentyear(df, newcolumn="year", source="date"):
    """Augment the year column based on source date field."""
    for index, entry in df.iterrows():
        if pd.isna(df.loc[index, newcolumn]) and not pd.isna(df.loc[index, source]):
            df.loc[index, newcolumn] = df.loc[index, source].year
    return df


def augmentcurrency(df, newcolumn="amountstr", source="amount", sf=0):
    """Preprocessor to set integer type on columns."""
    fstr = f"{{0:,.{sf}f}}"
    df[newcolumn] = df[source].apply(lambda x: fstr.format(x))
    return df


def addsupervisor(df, column, supervisor):
    df[column] = df[column].fillna(supervisor)
    return df


## Sorters
def ascending(df, by):
    """Sort in ascending order"""
    return df.sort_values(by=by, ascending=True)


def descending(df, by):
    """Sort in descending order"""
    return df.sort_values(by=by, ascending=False)


## Filters
def recent(df, column="year"):
    """Filter on year of item"""
    return df[column] >= get_since_year()


def current(df, start="start", end="end", current=None):
    """Filter on whether item is current"""
    now = pd.to_datetime(datetime.datetime.now().date())
    within = (df[start] <= now) & (pd.isna(df[end]) | (df[end] >= now))
    if current is not None:
        return within | (~df[current].isna() & df[current])
    else:
        return within


def former(df, end="end"):
    """Filter on whether item is current"""
    now = pd.to_datetime(datetime.datetime.now().date())
    return df[end] < now


def onbool(df, column="current", invert=False):
    """Filter on whether column is positive (or negative if inverted)"""
    if invert:
        return ~df[column]
    else:
        return df[column]


def columnis(df, column, value):
    """Filter on whether item is equal to a given value"""
    return df[column] == value


def columncontains(df, column, value):
    """Filter on whether column contains a given value"""
    colis = columnis(df, column, value)
    return colis | df[column].apply(lambda x: (x == value).any() if type(x == value) is not bool else (x == value))
