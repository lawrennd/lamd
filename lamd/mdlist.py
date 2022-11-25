#!/usr/bin/env python3

import sys
import os
import datetime

import argparse
import numpy as np

import pandas as pd
import liquid as pl

import ndlpy.data as nd

publications_since_year = 2000
meetings_since_year = 2022
talks_since_year = 2020

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
            df[column] = pd.to_numeric(df[column], downcast="integer")
    return df

def convert_string(df, columns):
    """Preprocessor to set string type on columns."""
    if type(columns) is not list:
        columns = [columns]
    for column in columns:
        if column in df.columns:
            df[column] = df[column].apply(lambda x: str(x) if not pd.isna(x) else pd.NA)
    return df

def convert_new_year_day(df, columns):
    """Preprocessor to set string type on columns."""
    if type(columns) is not list:
        columns = [columns]
    for column in columns:
        if column in df.columns:
            df[column] = df[column].apply(lambda x: str(x) + "-01-01" if not pd.isna(x) else pd.NA)
    return df

def convert_new_year_eve(df, columns):
    """Preprocessor to set string type on columns."""
    if type(columns) is not list:
        columns = [columns]
    for column in columns:
        if column in df.columns:
            df[column] = df[column].apply(lambda x: str(x) + "-12-31" if not pd.isna(x) else pd.NA)
            print(df[column])
    return df


## Augmentors
def monthname(df, source="date", month_column="month_name", year_column="year"):
    """Add month_name column and year column based on source field."""
    df[year_column] = df[source].apply(lambda x: x.year if x is not None else pd.NA)
    df[month_column] = df[source].apply(lambda x: x.month_name() if x is not None else pd.NA)
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
def recent(df, since_year, column="year"):
    """Filter on year of item"""
    try:
        return df[column]>=since_year
    except TypeError as err:
        for index, entry in df[column].items():
            try:
                entry>=since_year
            except:
                print(index, entry, type(entry))
                raise(err)
        raise(err)

def current(df, start="start", end="end"):
    """Filter on whether item is current"""
    now = pd.to_datetime(datetime.datetime.now().date())
    return ((df[start] <= now) & (df[end] >= now))

def former(df, end="end"):
    """Filter on whether item is current"""
    now = pd.to_datetime(datetime.datetime.now().date())
    return ((df[end] < now))

def columnis(df, column, value):
    """Filter on whether item is equal to a given value"""
    return ((df[column]==value))

def columncontains(df, column, value):
    """Filter on whether column contains a given value"""
    return (df[column].apply(pd.Series)==value).any(1)


cvlists={
    "talks": {
        "preprocessor": {
            "f": convert_datetime,
            "args": {
                "columns": "date",
            },    
        },
        "sorter": {
            "f": descending,
            "args": {
                "by": "date",
            },
        },
        "augmentor": {
            "f": monthname,
            "args": {
                "source": "date",
            },
        },
        "filter": {
            "f": recent,
            "args": {
                "since_year": talks_since_year,
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
        "sorter": {
            "f": descending,
            "args": {
                "by": "date",
            },
        },
        "filter": {
            "f": recent,
            "args": {
                "since_year": publications_since_year,
                "column": "year",
            },
        },
        "listtemplate": "listpaper",
    },
    "grants": {
        "preprocessor": [
            {
                "f": convert_new_year_day,
                "args": {
                    "columns": ["start"],
                },
            },
            {
                "f": convert_new_year_eve,
                "args": {
                    "columns": ["end"],
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
            "f": recent,
            "args": {
                "since_year": meetings_since_year,
                "column": "year",
            },
        },
        "listtemplate": "listmeeting",
    },
    "students": {
        "preprocessor": [
            # {
            #     "f": convert_new_year_day,
            #     "args": {
            #         "columns": ["start"],
            #     },
            # },
            # {
            #     "f": convert_new_year_eve,
            #     "args": {
            #         "columns": ["end"],
            #     },
            # },
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
                "by": ["start", "end"],
            },
        },
        "augmentor": {
            "f": addsupervisor,
            "args": {
                "supervisor": "ndl21",
                "column": "supervisor",
            },
        },
        "filter": {
            "f": current,
            "args": {
                "start": "start",
                "end": "end",
            },
        },
        "filter": {
            "f": columnis,
            "args": {
                "column": "position",
                "value": "PhD Student",
            },
        },
        "filter": {
            "f": columncontains,
            "args": {
                "column": "supervisor",
                "value": "ndl21",
            },
        },
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

    parser.add_argument('-m', '--meetings-since-year', type=int, 
                        help="The year from which to include entries")

    parser.add_argument('-p', '--publications-since-year', type=int, 
                        help="The year from which to include entries")

    parser.add_argument('-t', '--talks-since-year', type=int, 
                        help="The year from which to include entries")

    parser.add_argument('file', type=str, nargs='+',
                        help="The file names to read in")


    args = parser.parse_args()
    now = pd.to_datetime(datetime.datetime.now().date())
    now_year = now.year

    if args.meetings_since_year:
        meetings_since_year=datetime.date(year=args.meetings_since_year, month=1, day=1)
    else:
        meetings_since_year = now_year - 5

    if args.talks_since_year:
        talks_since_year=datetime.date(year=args.talks_since_year, month=1, day=1)
    else:
        talks_since_year = now_year - 5
        
    df = pd.DataFrame(nd.loaddata(args.file))
    text = ''


    if args.listtype in cvlists:
        for op in ["preprocessor", "sorter", "augmentor"]:
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
                try:
                    filt = (filt & newfilt)
                except TypeError as err:
                    for index, entry in filt.items():
                        try:
                            entry and newfilt[index]
                        except:
                            raise(err)
                    
        listtemplate = cvlists[args.listtype]["listtemplate"]
        for index, entry in df.iterrows():
            if filt[index]:
                text += env.get_template(listtemplate + ext).render(**entry)
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
