#!/usr/bin/env python3

import sys
import os
import datetime

import argparse
import numpy as np

import pandas as pd
import liquid as pl

import ndlpy.data as nd

since_year = 2001

name_template = "{%if url %}[{%endif%}{{given}} {%if prefix%}{{prefix}} {%endif%}{{family}}{%if suffix %} {{suffix}}{%endif%}{%if url %}]({{ url }}){%endif%}"
place_template = "{%if place %}, {{ place }}{%endif%}"

templates = {
    'pdra' : pl.Template("* " + name_template + place_template + "\n"),
    'grant' : pl.Template("* {{title}}, {{currency}}{{amount}}, from {{start}} to {{end}} funded by {{funders}} {{number}} {{description}}\n"),
    'student' : pl.Template("* " + name_template + place_template + "\n"),
    'talk' : pl.Template("* {{title}}, *{{venue}}*, {{month_name}}, {{year}}\n"),
}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("listtype",
                        type=str,
                        choices=['talks', 'grants', 'meetings',
                                 'extalks', 'teaching', 'students',
                                 'exstudents', 'pdras', 'expdras', 'exgrants'],
                        help="The type of output markdown list")

    parser.add_argument("-o", "--output", type=str,
                        help="Output filename")

    parser.add_argument('-s', '--since-year', type=int, 
                        help="The year from which to include entries")

    parser.add_argument('file', type=str, nargs='+',
                        help="The file names to read in")


    args = parser.parse_args()
    now = datetime.datetime.now()
    now_year = now.year 

    if args.since_year:
        since_year=now_year
    else:
        since_year = now_year - 5
        
    df = pd.DataFrame(nd.loaddata(args.file))
    if args.listtype in ['pdras', 'expdras', 'students', 'exstudents']:

        # it's a person of some form, check if they are current
        df = addcolumns(df, ['start', 'end', 'visitor',
                             'student', 'pdra', 'supervisor'])
        df['end'] = pd.to_datetime(df['end'])
        df['start'] = pd.to_datetime(df['start'])

        df = df.rename(columns={'current': 'current_y_n'})
        mask = ((df['current_y_n'][df['current_y_n'].notna()] == 'Y')
                | (df['start'][df['start'].notna()] < now)
                & (df['end'][df['end'].notna()] > now))
        df['current'] = mask

        df = df.rename(columns={'pdra': 'pdra_y_n'})
        mask = (df['pdra_y_n'][df['pdra_y_n'].notna()] == 'Y')
        df['pdra'] = mask

        df = df.rename(columns={'student': 'student_y_n'})
        mask = (df['student_y_n'][df['student_y_n'].notna()] == 'Y')
        print(df['student_y_n'])
        df['student'] = mask
        
        df['supervisor'] = df['supervisor'].fillna('ndl21')
        mask = (df['supervisor'].apply(pd.Series)=='ndl21').any(1)
        df['ndlsupervise'] = mask
        print(df)

    text = ''


    
    if args.listtype=="talks":
        df['date'] = pd.to_datetime(df['date'])
        df = df.sort_values(by=['date'], ascending=False)
        for index, entry in df.iterrows():
            entry['year'] = entry['date'].year
            entry['month_name'] = entry['date'].month_name()
            if entry['year']>=since_year:
                text +=  templates['talk'].render(**entry)

    elif args.listtype=='grants':
        df = df.sort_values(by=['start','end'], ascending=False)
        for index, entry in df.iterrows():
            if int(entry['end'])>=now_year:
                text +=  templates['grant'].render(**entry)

    elif args.listtype=='exgrants':
        df = df.sort_values(by=['start','end'], ascending=False)
        for index, entry in df.iterrows():
            if int(entry['end'])<now_year:
                text +=  templates['grant'].render(**entry)
                
    elif args.listtype=='meetings':
        df = df.sort_values(by=['year'], ascending=False)
        for index, entry in df.iterrows():
            if int(entry['year'])>=since_year:
                text +=  pl.Template("* {{title}} at {{place}}, {{month}} {{year}}").render(**entry)
                if len(entry['coorganisers'])>0:
                    text += pl.Template(" with {{coorganisers}}.\n").render(**entry)
                else:
                    text += ".\n"

    elif args.listtype=='students':        
        df = df.sort_values(by=['start'], ascending=False)
        for index, entry in df.iterrows():
            if entry['current'] and entry['ndlsupervise'] and entry['student']:                text += templates['student'].render(**entry)

    elif args.listtype=='pdras':
        df = df.sort_values(by=['start'], ascending=False)
        for index, entry in df.iterrows():
            if entry['current'] and entry['ndlsupervise'] and entry['pdra']:
                text +=  templates['pdra'].render(**entry)

    elif args.listtype=='exstudents':
        df = df.sort_values(by=['end'], ascending=False)
        for index, entry in df.iterrows():
            if not entry['current'] and entry['ndlsupervise'] and entry['student']:
                text += templates['student'].render(**entry)

    elif args.listtype=='expdras':
        df = df.sort_values(by=['end'], ascending=False)
        for index, entry in df.iterrows():
            if not entry['current'] and entry['ndlsupervise'] and entry['pdra']:
                text +=  templates['pdra'].render(**entry)

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
        
if __name__ == "__main__":
    sys.exit(main())
