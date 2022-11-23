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



def main():
    ext = ".liquid"
    env = load_template_env(ext=ext)
    
    parser = argparse.ArgumentParser()
    parser.add_argument("listtype",
                        type=str,
                        choices=['talks', 'grants', 'meetings',
                                 'extalks', 'teaching', 'exteaching', 'students',
                                 'exstudents', 'pdras', 'expdras', 'exgrants'],
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
        since_year=datetime.date(year=args.since_year, month=1, day=1)
    else:
        since_year = now_year - 5
        
    df = pd.DataFrame(nd.loaddata(args.file))
    if args.listtype in ['pdras', 'expdras', 'students', 'exstudents', 'grants', "exgrants", "teaching", "exteaching"]:
        df = addcolumns(df, ['start', 'end'])
        df['end'] = pd.to_datetime(df['end'])
        df['start'] = pd.to_datetime(df['start'])
        
    if args.listtype in ['pdras', 'expdras', 'students', 'exstudents']:

        # it's a person of some form, check if they are current
        df = addcolumns(df, ['visitor',
                             'student', 'pdra', 'supervisor'])

        df = df.rename(columns={'current': 'current_y_n'})
        mask = ((df['current_y_n'])
                | (df['start'][df['start'].notna()] < now)
                & (df['end'][df['end'].notna()] > now))
        df['current'] = mask
        
        df['supervisor'] = df['supervisor'].fillna('ndl21')
        mask = (df['supervisor'].apply(pd.Series)=='ndl21').any(1)
        df['ndlsupervise'] = mask

    df = df.replace({np.nan:None})
    text = ''


    
    if args.listtype=="talks":
        df['date'] = pd.to_datetime(df['date'])
        df = df.sort_values(by=['date'], ascending=False)
        for index, entry in df.iterrows():
            entry['year'] = entry['date'].year
            entry['month_name'] = entry['date'].month_name()
            if entry['year']>=since_year:
                text +=  env.get_template("talk" + ext).render(**entry)
                text += "\n"

    elif args.listtype=='grants':
        df = df.sort_values(by=['start','end'], ascending=False)
        for index, entry in df.iterrows():
            if "end" not in entry or entry["end"] is None or entry['end']>=now:
                text +=  env.get_template("grant" + ext).render(**entry)
                text += "\n"

    elif args.listtype=='exgrants':
        df = df.sort_values(by=['start','end'], ascending=False)
        for index, entry in df.iterrows():
            if entry['end']<now:
                text +=  env.get_template("grant" + ext).render(**entry)
                text += "\n"

    elif args.listtype=='teaching':
        df = df.sort_values(by=['start','end', 'semester'], ascending=False)
        for index, entry in df.iterrows():
            if "end" not in entry or entry["end"] is None or entry['end']>=now:
                text +=  env.get_template("teaching" + ext).render(**entry)
                text += "\n"
                
    elif args.listtype=='exteaching':
        df = df.sort_values(by=['start','end'], ascending=False)
        for index, entry in df.iterrows():
            if "end" in entry and entry["end"] is not None and entry['end']<now:
                text +=  env.get_template("teaching" + ext).render(**entry)
                text += "\n"
                
    elif args.listtype=='meetings':
        df = df.sort_values(by=['year'], ascending=False)
        for index, entry in df.iterrows():
            if entry['year']>=since_year:
                text += env.from_string("* {{title}} at {{place}}, {{month}} {{year}}").render(**entry)
                if len(entry['coorganisers'])>0:
                    text += env.from_string(" with {{coorganisers}}.\n").render(**entry)
                else:
                    text += ".\n"

    elif args.listtype=='students':        
        df = df.sort_values(by=['start'], ascending=False)
        for index, entry in df.iterrows():
            if entry['current'] and entry['ndlsupervise'] and entry['student']:                text += env.get_template("student" + ext).render(**entry)

    elif args.listtype=='pdras':
        df = df.sort_values(by=['start'], ascending=False)
        for index, entry in df.iterrows():
            if entry['current'] and entry['ndlsupervise'] and entry['pdra']:
                text +=  env.get_template("pdra" + ext).render(**entry)

    elif args.listtype=='exstudents':
        df = df.sort_values(by=['end'], ascending=False)
        for index, entry in df.iterrows():
            if not entry['current'] and entry['ndlsupervise'] and entry['student']:
                text += env.get_template("student" + ext).render(**entry)

    elif args.listtype=='expdras':
        df = df.sort_values(by=['end'], ascending=False)
        for index, entry in df.iterrows():
            if not entry['current'] and entry['ndlsupervise'] and entry['pdra']:
                text +=  env.get_template("pdra" + ext).render(**entry)

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
        
def load_template_env(ext=".liquid"):
    """Load in the templates to be used for lists."""
    # Having trouble getting the template_path to contain multiple pats, so just providing one for the moment. See https://jg-rp.github.io/liquid/api/fileextensionloader
    template_path = [
        os.path.join(os.path.dirname(__file__), "templates"),
    ]
    env = pl.Environment(loader=pl.loaders.FileExtensionLoader(search_path=":".join(template_path), ext=ext))
    return env

if __name__ == "__main__":
    sys.exit(main())
