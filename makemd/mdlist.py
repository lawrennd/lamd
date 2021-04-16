#!/usr/bin/env python3

import sys
import os
import datetime

import argparse
import pandas as pd

import ndlpy.data as nd

since_year = 2001

templates =
{
    'pdra' : "* {given} {family}\n",
    'grant' : "* {title}, {currency}{amount}, from {start} to {end} funded by {funders} {number} {description}\n",
    'student' : "* {given} {family}\n",
    'talk' : "* {title}, *{venue}*, {month_name}, {year}\n"
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
    text = ''

    if args.listtype=="talks":
        df['date'] = pd.to_datetime(df['date'])
        df = df.sort_values(by=['date'], ascending=False)
        for index, entry in df.iterrows():
            entry['year'] = entry['date'].year
            entry['month_name'] = entry['date'].month_name()
            if entry['year']>=since_year:
                text +=  template['talk'].format(**entry)
    elif args.listtype=='grants':
        df = df.sort_values(by=['start','end'], ascending=False)
        for index, entry in df.iterrows():
            if int(entry['end'])>=now_year:
                text +=  template['grant'].format(**entry)

    elif args.listtype=='meetings':
        df = df.sort_values(by=['year'], ascending=False)
        for index, entry in df.iterrows():
            if int(entry['year'])>=since_year:
                text +=  "* {title} at {place}, {month} {year}".format(**entry)
                if len(entry['coorganisers'])>0:
                    text += " with {coorganisers}.\n".format(**entry)
                else:
                    text += ".\n"

    elif args.listtype=='students':
        df['date'] = pd.to_datetime(df['start'])

        df = df.sort_values(by=['start'], ascending=False)
        df = df.fillna(False)
        for index, entry in df.iterrows():
            if (not entry['visitor']
                and entry['student']
                and (entry['supervisor']=='ndl21'
                     or isinstance(entry['supervisor'], list)
                and 'ndl21' in entry['supervisor']):
                text += templates['pdra'].format(**entry)

    elif args.listtype=='pdras':
        df['date'] = pd.to_datetime(df['start'])
        
        df = df.sort_values(by=['start'], ascending=False)
        df = df.fillna(False)
        for index, entry in df.iterrows():
            if (not entry['visitor']
                and not entry['student']
                and (entry['supervisor']=='ndl21'
                     or isinstance(entry['supervisor'], list)
                and 'ndl21' in entry['supervisor']):
                text +=  templates['pdra'].format(**entry)

    elif args.listtype=='exgrants':
        df = df.sort_values(by=['start','end'], ascending=False)
        for index, entry in df.iterrows():
            if int(entry['end'])<now_year:
                text +=  templates['grant'].format(**entry)

    elif args.listtype=='exstudents':
        df['date'] = pd.to_datetime(df['start'])

        df = df.sort_values(by=['end'], ascending=False)
        df = df.fillna(False)
        for index, entry in df.iterrows():
            if (not entry['visitor']
                and entry['student']
                and (entry['supervisor']=='ndl21'
                     or isinstance(entry['supervisor'], list)
                and 'ndl21' in entry['supervisor']):
                text +=  template['student'].format(**entry)

    elif args.listtype=='expdras':
        df['date'] = pd.to_datetime(df['start'])
        
        df = df.sort_values(by=['start'], ascending=False)
        df = df.fillna(False)
        for index, entry in df.iterrows():
            if not entry['visitor']
                and not entry['student']
                and (entry['supervisor']=='ndl21'
                     or isinstance(entry['supervisor'], list)
                and 'ndl21' in entry['supervisor']):
                text += template['pdra'].format(**entry)

    print(args.output)
    if args.output is not None:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(text)
    else:
        print(text)

if __name__ == "__main__":
    sys.exit(main())
