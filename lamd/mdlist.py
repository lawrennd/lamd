#!/usr/bin/env python3

from .utils import *
from ndlpy import access
from ndlpy.util import remove_nan
from ndlpy.liquid import load_template_env

from referia import assess

from ndlpy import settings as st

global SINCE_YEAR

def set_since_year(year):
    global SINCE_YEAR
    SINCE_YEAR=year

def get_since_year():
    global SINCE_YEAR
    return SINCE_YEAR

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

    # Load in the settings specified for the relevant list type.
    settings = st.Settings(user_file="cvlists.yml", field=args.listtype)
    
    if args.since_year:
        set_since_year(args.since_year)
    else:
        set_since_year(now_year - 5)


    # Set up the allocation based on command line.
    settings["alllocation"] = {}
    settings["allocation"]["filename"] = args.file
    if type(args.file) is list:
        data = []
        settings["allocation"]["type"] = "list"
        data = assess.Data(settings)
        
    elif type(args.file) is str:
        settings["allocation"]["type"] = "auto"
        data = assess.Data(settings)

    settings["cache"] = # Set up cache 
    text = ""

    for op in ["preprocessor", "augmentor", "sorter"]:
        if op in settings["lists"][args.listtype]:
                comp = settings["lists"][args.listtype][op]
                if op in settings["compute"]:
                    if type(comp) is not list:
                        comp = [comp]    
                    settings["compute"][op] += comp
                else:
                    settings["compute"][op] = comp
                    
        if "filter" in settings["lists"][args.listtype]:
            filt = settings["lists"][args.listtype]["filter"]:
            if "filter" in settings:
                if type(filt) is not list:
                    filt = [filt]
                settings["filter"] += filt
            else:
                settings["filter"] = filt
            
        data.preprocess()
                        
        listtemplate = settings["lists"][args.listtype]["listtemplate"]
        for index, entry in df.iterrows():
            if not pd.isna(filt[index]) and filt[index]:
                kwargs = remove_nan(entry.to_dict())
                text += env.get_template(listtemplate + ext).render(**kwargs)
                text += "\n"

               

        
    if args.output is not None:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(text)
    else:
        print(text)


if __name__ == "__main__":
    sys.exit(main())
