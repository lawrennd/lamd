#!/usr/bin/env python3

from .utils import *
from lynguine import access
from lynguine.util.misc import remove_nan
from lynguine.util.liquid import load_template_env

from referia import assess

from lynguine.config.interface import Interface

"""
This script generates markdown lists for various academic content types (publications, talks, grants, etc.)
from structured data files. It processes the input data according to specified settings and outputs
formatted markdown text.
"""

global SINCE_YEAR

def set_since_year(year):
    """Set the global year filter for entries.
    
    :param year: The year from which to include entries
    :type year: int
    """
    global SINCE_YEAR
    SINCE_YEAR = year

def get_since_year():
    """Get the current global year filter.
    
    :return: The year from which entries are included
    :rtype: int
    """
    global SINCE_YEAR
    return SINCE_YEAR

def main():
    """Main function to process and generate markdown lists.
    
    Handles command line arguments, loads data, processes it according to specified
    settings, and outputs formatted markdown text either to a file or stdout.
    
    :return: None
    :rtype: None
    """
    # Set up template environment for markdown
    ext = ".md"
    env = load_template_env(ext=ext)

    # Configure command line argument parser
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

    # Load interface configuration for the specified list type
    interface = Interface.from_file(user_file="cvlists.yml")[args.listtype]
    
    # Set the year filter - either from command line or default to 5 years ago
    if args.since_year:
        set_since_year(args.since_year)
    else:
        set_since_year(now_year - 5)


    # Configure data allocation based on input files
    interface["input"] = {}

    # Extract most common starting directory from file paths
    file_dirs = [os.path.dirname(os.path.abspath(f)) for f in args.file]
    common_prefix = os.path.commonpath(file_dirs)
    
    interface["input"]["base_directory"] = common_prefix


    # Remove common prefix from file paths
    args.file = [os.path.relpath(f, common_prefix) for f in args.file]
    interface["input"]["directory"] = "."
    if len(args.file) == 1:
        interface["input"]["filename"] = args.file[0]
        interface["input"]["type"] = "auto"
    else:
        interface["input"]["filename"] = args.file
        interface["input"]["type"] = "list"
    
    data = assess.data.CustomDataFrame.from_flow(interface)


    #settings["cache"] = # Set up cache 
    text = ""

    # Process the data through different operations (preprocessor, augmentor, sorter)
    for op in ["preprocessor", "augmentor", "sorter"]:
        if op in settings["lists"][args.listtype]:
            # Add operation to compute settings
            comp = settings["lists"][args.listtype][op]
            if op in settings["compute"]:
                if type(comp) is not list:
                    comp = [comp]    
                settings["compute"][op] += comp
            else:
                settings["compute"][op] = comp
    
    # Handle filters if specified
    if "filter" in settings["lists"][args.listtype]:
        filt = settings["lists"][args.listtype]["filter"]
        if "filter" in settings:
            if type(filt) is not list:
                filt = [filt]
            settings["filter"] += filt
        else:
            settings["filter"] = filt
        
    # Preprocess the data
    data.preprocess()
                    
    # Generate markdown text using the specified template
    listtemplate = settings["lists"][args.listtype]["listtemplate"]
    for index, entry in df.iterrows():
        if not pd.isna(filt[index]) and filt[index]:
            kwargs = remove_nan(entry.to_dict())
            text += env.get_template(listtemplate + ext).render(**kwargs)
            text += "\n"

    # Output the generated markdown
    if args.output is not None:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(text)
    else:
        print(text)


if __name__ == "__main__":
    sys.exit(main())
