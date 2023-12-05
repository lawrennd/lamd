#!/usr/bin/env python3

import sys
import os
import datetime

import argparse
import numpy as np

import pandas as pd
import liquid as pl

import ndlpy.data as nd

import ndlpy.access as access

import ndlpy.context as context
from ndlpy.log import Logger
from ndlpy.util import remove_nan

global SINCE_YEAR

cntxt = context.Context(name="lamd")
log = Logger(
    name=__name__,
    level=cntxt["logging"]["level"],
    filename=cntxt["logging"]["filename"]
)



def set_since_year(year):
    global SINCE_YEAR
    SINCE_YEAR=year

def get_since_year():
    global SINCE_YEAR
    return SINCE_YEAR

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
            df[column] = pd.to_numeric(df[column]).apply(lambda x: int(x) if not pd.isna(x) else pd.NA).astype('Int64')
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
        if type_field is int: # Assume it is integer year
            log.debug(f"Returning \"{type_field}\" from form \"{field}\"")
            dt = datetime.datetime(year=field, month=month, day=day)
        elif type_field is str: 
            try:
                year = int(field) # Try it as string year
                log.debug(f"Returning \"{type_field}\" from form \"{field}\"")
                dt = datetime.datetime(year=year, month=month, day=day)
            except TypeError as e:
                log.debug(f"Returning \"{type_field}\" from form \"{field}\"")
                dt = datetime.datetime.strptime(field, "%Y-%m-%d") # Try it as string YYYY-MM-DD
        elif type_field is datetime.date:
            log.debug(f"Returning \"{type_field}\" from form \"{field}\"")
            return field
        else:
            raise TypeError(f"Expecting type of int or str or datetime but found \"{type_field}\"")
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
    fstr=f"{{0:,.{sf}f}}"
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
    return df[column]>=get_since_year()

def current(df, start="start", end="end", current=None):
    """Filter on whether item is current"""
    now = pd.to_datetime(datetime.datetime.now().date())
    within = ((df[start] <= now) & (pd.isna(df[end]) | (df[end] >= now)))
    if current is not None:
        return (within | (~df[current].isna() & df[current]))
    else:
        return within

def former(df, end="end"):
    """Filter on whether item is current"""
    now = pd.to_datetime(datetime.datetime.now().date())
    return (df[end] < now)

def onbool(df, column="current", invert=False):
    """Filter on whether column is positive (or negative if inverted)"""
    if invert:
        return ~df[column]
    else:
        return df[column]

def columnis(df, column, value):
    """Filter on whether item is equal to a given value"""
    return (df[column]==value)

def columncontains(df, column, value):
    """Filter on whether column contains a given value"""
    colis = columnis(df, column, value)
    return (colis | df[column].apply(lambda x: (x==value).any() if type(x==value) is not bool else (x==value)))


cvlists={
    "talks": {
        "preprocessor": [
            {
                "f": convert_datetime,
                "args": {
                    "columns": "date",
                },    
            },
        ],
        "sorter": {
            "f": descending,
            "args": {
                "by": "date",
            },
        },
        "augmentor": [
            {
                "f": addmonth,
                "args": {
                    "source": "date",
                },
            },
            {
                "f": addyear,
                "args": {
                    "source": "date",
                },
            },
        ],
        "filter": {
            "f": recent,
            "args": {
                "column": "year",
            },
        },
        "listtemplate": "listtalk",
    },
    "publications": {
        "preprocessor": [
            {
                "f": convert_datetime,
                "args": {
                    "columns": ["date", "published"],
                },
            },
            {
                "f": convert_int,
                "args": {
                    "columns": "year",
                },
            },
        ],
        "augmentor": [
            {
                "f": augmentmonth,
                "args": {
                    "source": "published",
                    "newcolumn": "month",
                },
            },
            {
                "f": augmentyear,
                "args": {
                    "source": "published",
                    "newcolumn": "year",
                },
            },
        ],
        "sorter": {
            "f": descending,
            "args": {
                "by": ["year", "published"],
            },
        },
        "filter": {
            "f": recent,
            "args": {
                "column": "year",
            },
        },
        "listtemplate": "listpaper",
    },
    "grants": {
        "preprocessor": [
            {
                "f": convert_year_iso,
                "args": {
                    "column": "start",
                    "month": 1,
                    "day": 1,
                },
            },
            {
                "f": convert_year_iso,
                "args": {
                    "column": "end",
                    "month": 12,
                    "day": 31,
                },
            },
            {
                "f": convert_datetime,
                "args": {
                    "columns": ["start", "end"],
                },
            },
            {
                "f": convert_int,
                "args": {
                    "columns": "amount",
                },
            },
        ],
        "augmentor": [
            {
                "f": augmentcurrency,
                "args": {
                    "source": "amount",
                    "newcolumn": "amountstr",
                },
            },
        ],
        "sorter": {
            "f": descending,
            "args": {
                "by": ["start", "end"],
            },
        },
        "filter": {
            "f": current,
            "args": {
                "start": "start",
                "end": "end",
            },
        },
        "listtemplate": "listgrant",
    },
    "teaching":{
        "preprocessor": [
            {
                "f": convert_datetime,
                "args": {
                    "columns": ["start", "end"],
                },
            },
        ],
        "sorter": {
            "f": descending,
            "args": {
                "by": ["start", "end", "semester"],
            },
        },
        "filter": {
            "f": current,
            "args": {
                "start": "start",
                "end": "end",
            },
        },
        "listtemplate": "listteaching",
    },
    "meetings":{
        "preprocessor": [
            {
                "f": convert_int,
                "args": {
                    "columns": ["year"],
                },
            },
        ],
        "sorter": {
            "f": descending,
            "args": {
                "by": ["year"],
            },
        },
        "filter": {
            "f": recent,
            "args": {
                "column": "year",
            },
        },
        "listtemplate": "listmeeting",
    },
    "students": {
        "preprocessor": [
            {
                "f": convert_datetime,
                "args": {
                    "columns": ["start", "end"],
                },
            },
        ],
        "sorter": {
            "f": descending,
            "args": {
                "by": ["start"],
            },
        },
        "augmentor": {
            "f": addsupervisor,
            "args": {
                "supervisor": "ndl21",
                "column": "supervisor",
            },
        },
        "filter": [
            {
                "f": current,
                "args": {
                    "current": "current",
                    "start": "start",
                    "end": "end",
                },
            },
            {
                "f": columnis,
                "args": {
                    "column": "position",
                    "value": "PhD Student",
                },
            },
            {
                "f": columncontains,
                "args": {
                    "column": "supervisor",
                    "value": "ndl21",
                },
            },
        ],
        "listtemplate": "liststudent",
    },
}
cvlists["exgrants"] = cvlists["grants"].copy()
cvlists["exgrants"]["filter"] = {
    "f": former,
    "args": {
        "end": "end",
        }
    }

cvlists["exteaching"] = cvlists["teaching"].copy()
cvlists["exteaching"]["filter"] = {
    "f": former,
    "args": {
        "end": "end",
    }
}

cvlists["exstudents"] = cvlists["students"].copy()
del cvlists["exstudents"]["augmentor"]
cvlists["exstudents"]["filter"] = [
    {
        "f": onbool,
        "args": {
            "column": "current",
            "invert": True,
        },
    },
    {
        "f": onbool,
        "args": {
            "column": "student",
        },
    },
]
cvlists["pdras"] = cvlists["students"].copy()
cvlists["pdras"]["listtemplate"] = "listpdra"
cvlists["pdras"]["filter"] = [
    {
        "f": current,
        "args": {
            "current": "current",
            "start": "start",
            "end": "end",
        },
    },
    {
        "f": columnis,
        "args": {
            "column": "position",
            "value": "Research Associate",
        },
    },
    {
        "f": columncontains,
        "args": {
            "column": "supervisor",
            "value": "ndl21",
        },
    },
]

cvlists["expdras"] = cvlists["pdras"].copy()
del cvlists["expdras"]["augmentor"]
del cvlists["expdras"]["sorter"]
cvlists["expdras"]["filter"] = [
    {
        "f": onbool,
        "args": {
            "column": "current",
            "invert": True,
        },
    },
]


def main():
    ext = ".md"
    env = load_template_env(ext=ext)
    parser = argparse.ArgumentParser()
    parser.add_argument("listtype",
                        type=str,
                        choices=['talks', 'grants', 'meetings',
                                 'extalks', 'teaching', 'exteaching', 'students',
                                 'exstudents', 'pdras', 'expdras', 'exgrants',
                                 'publications', 'journal', 'book', "conference"],
                        help="The type of output markdown list")

    parser.add_argument("-o", "--output", type=str,
                        help="Output filename")

    parser.add_argument('-s', '--since-year', type=int, 
                        help="The year from which to include entries")

    parser.add_argument('file', type=str, nargs='+',
                        help="The file names to read in")


    args = parser.parse_args()
    now = pd.to_datetime(datetime.datetime.now().date())
    now_year = now.year

    if args.since_year:
        set_since_year(args.since_year)
    else:
        set_since_year(now_year - 5)
    if type(args.file) is list:
        data = []
        for filename in args.file:
            new_data = access.read_file(filename)
            typ = type(new_data)
            if typ is list:
                data += new_data
            elif typ is dict:
                data.append(new_data)
            else:
                raise ValueError(f"data loaded from \"{filename}\" is of invalid type \"{typ}\".")
        df = pd.DataFrame(data)
    elif type(args.file) is str:
        data = access.read_file(args.file)
        df = pd.DataFrame(data)
    text = ''


    if args.listtype in cvlists:
        for op in ["preprocessor", "augmentor", "sorter"]:
            if op in cvlists[args.listtype]:
                calls = cvlists[args.listtype][op]
                if type(calls) is not list:
                    calls = [calls]
                for call in calls:
                    df = call["f"](df, **call["args"])
        filt = pd.Series(True, index=df.index)
        if "filter" in cvlists[args.listtype]:
            calls = cvlists[args.listtype]["filter"]
            if type(calls) is not list:
                calls = [calls]    
            for call in calls:
                newfilt = call["f"](df, **call["args"])
                filt = (filt & newfilt)
                    
        listtemplate = cvlists[args.listtype]["listtemplate"]
        for index, entry in df.iterrows():
            if not pd.isna(filt[index]) and filt[index]:
                kwargs = remove_nan(entry.to_dict())
                text += env.get_template(listtemplate + ext).render(**kwargs)
                text += "\n"

               

    # elif args.listtype=='pdras':
    #     df = df.sort_values(by=['start'], ascending=False)
    #     for index, entry in df.iterrows():
    #         if entry['current'] and entry['ndlsupervise'] and entry['pdra']:
    #             text +=  env.get_template("pdra" + ext).render(**entry)

    # elif args.listtype=='exstudents':
    #     df = df.sort_values(by=['end'], ascending=False)
    #     for index, entry in df.iterrows():
    #         if not entry['current'] and entry['ndlsupervise'] and entry['student']:
    #             text += env.get_template("student" + ext).render(**entry)

    # elif args.listtype=='expdras':
    #     df = df.sort_values(by=['end'], ascending=False)
    #     for index, entry in df.iterrows():
    #         if not entry['current'] and entry['ndlsupervise'] and entry['pdra']:
    #             text +=  env.get_template("pdra" + ext).render(**entry)

    # elif args.listtype in ["publication", "journal", "book", "conference"]:
    #     df = df.sort_values(by=["date"], ascending=False)
        
    if args.output is not None:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(text)
    else:
        print(text)

# def remove_nan(dictionary):
#     """Delete missing entries from dictionary"""
#     dictionary2 = dictionary.copy()
#     for key, entry in dictionary.items():
#         if type(entry) is dict:
#             dictionary2[key] = remove_nan(entry)
#         else:
#             isna = pd.isna(entry)
#             if type(isna) is bool and isna:
#                 del(dictionary2[key])
#     return dictionary2
                
 
def addcolumns(df, columns):
    """Add empty column to data frame"""
    for column in columns:
        if column not in df.columns:
            df[column]=np.nan

    return df
        
def load_template_env(ext=".md"):
    """Load in the templates to be used for lists."""
    # Having trouble getting the template_path to contain multiple pats, so just providing one for the moment. See https://jg-rp.github.io/liquid/api/fileextensionloader
    template_path = [
        os.path.join(os.path.dirname(__file__), "templates"),
    ]
    env = pl.Environment(loader=pl.loaders.FileExtensionLoader(search_path=template_path, ext=ext))
    return env



if __name__ == "__main__":
    sys.exit(main())
