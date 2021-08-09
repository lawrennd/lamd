#!/usr/bin/env python3
# Markdown Preprocessor for talks.
# Requries gpp (the generic preprocessor) to be installed https://math.berkeley.edu/~auroux/software/gpp.html.

import sys
import os

import argparse
import frontmatter as fm

import ndlpy.yaml as ny

INCLUDE = os.path.join(os.path.dirname(__file__), "macros")

def main():

    parser = argparse.ArgumentParser()

    parser.add_argument("filename", type=str,
                        help="Input filename")

    parser.add_argument("-o", "--output", type=str,
                        help="Output filename")

    parser.add_argument("--no-header", default=False, action='store_true',
                        help="Whether to search for a header in the input file (default False).")

    parser.add_argument("-B", "--include-before-body", type=str,
                        help="File to include before body.")

    parser.add_argument("-A", "--include-after-body", type=str,
                        help="File to include after body.")

    parser.add_argument("-t", "--to", type=str,
                        choices=['pptx', 'html', 'docx', 'ipynb', 'svg', 'tex', 'python'],
                        help="Target output file format")

    parser.add_argument("-w", "--whitespace", default=True, action='store_true',
                        help="Whether to remove whitespace from gpp files.")

    parser.add_argument("-I", "--include-path", type=str,
                        help="include diractories")

    parser.add_argument("-F", "--format", type=str,
                       choices=['notes', 'slides', 'code'],
                       help="Target output file contents")

    parser.add_argument("-c", "--code", type=str, default='none',
                        choices=['none', 'sparse', 'ipynb', 'diagnostic', 'plot', 'full'],
                        help="Which parts of the code to include.")

    parser.add_argument("-e", "--exercises", default=False, action='store_true',
                       help="Whether to include exercises")

    parser.add_argument("-a", "--assignment", default=False, action='store_true',
                       help="Whether notes are an assignment or not")

    parser.add_argument("-d", "--diagrams-dir", type=str,
                        help="Directory to find the diagrams in")

    parser.add_argument("-s", "--scripts-dir", type=str,
                        help="Directory to find the javascript in")

    parser.add_argument("-W", "--write-diagrams-dir", type=str,
                        help="Directory to write diagrams in for code")

    parser.add_argument("-D", "--draft", default=False, action='store_true',
                       help="Whether this is a draft version (default False)")

    parser.add_argument("-E", "--edit-links", default=False, action='store_true',
                       help="Whether to show edit links (default False)")

    parser.add_argument("-r", "--replace-notation", default=False, action='store_true',
                        help="Whether to replace the latex macros in the files, or to retain them for later processing (default is False, retain them)")

    parser.add_argument("-x", "--extract-material", type=str, default='all',
                        choices=['all', 'reading', 'references', 'exercises'],
                        help="Extract a subset of the material, e.g. reading matter, the references, etc.")

    args = parser.parse_args()

    url = ny.defaults['url'] + ny.defaults['baseurl']
    diagrams_dir =  url + ny.defaults['diagramdir']
    scripts_dir = ny.defaults['scriptdir']
    write_diagrams_dir = ny.defaults['writediagramdir']
    if args.diagrams_dir:
        diagrams_dir = args.diagrams_dir

    if args.scripts_dir:
        scripts_dir = args.scripts_dir

    if args.write_diagrams_dir:
        write_diagrams_dir = args.write_diagrams_dir

    arglist = ['+n', '-U "\\\\" "" "{" "}{" "}" "{" "}" "#" ""']
    if args.to:
        arglist.append('-D{to}=1'.format(to=args.to.upper()))
    if args.format:
        arglist.append('-D{format}=1'.format(format=args.format.upper()))
    if args.exercises:
        arglist.append('-DEXERCISES=1')
    if args.assignment:
        arglist.append('-DASSIGNMENT=1')
    if args.edit_links:
        arglist.append('-DEDIT=1')
    if args.draft:
        arglist.append('-DDRAFT=1')

    if args.extract_material is not None and args.code != 'all':
        pass

    if args.code is not None and args.code != 'none':
        arglist.append('-DCODE=1')
        if args.code == 'ipynb':
            arglist.append('-DDISPLAYCODE=1')
            arglist.append('-DPLOTCODE=1')
            arglist.append('-DHELPERCODE=1')
            arglist.append('-DMAGICCODE=1')
        elif args.code == 'diagnostic':
            arglist.append('-DDISPLAYCODE=1')
            arglist.append('-DHELPERCODE=1')
            arglist.append('-DPLOTCODE=1')
            arglist.append('-DMAGICCODE=1')
        elif args.code == 'full':
            arglist.append('-DDISPLAYCODE=1')
            arglist.append('-DHELPERCODE=1')
            arglist.append('-DPLOTCODE=1')
            arglist.append('-DMAGICCODE=1')
        if args.code == 'plot':
            arglist.append('-DHELPERCODE=1')
            arglist.append('-DPLOTCODE=1')

    arglist.append('-DdiagramsDir={diagrams_dir}'.format(diagrams_dir=diagrams_dir))
    arglist.append('-DscriptsDir={scripts_dir}'.format(scripts_dir=scripts_dir))
    arglist.append('-DwriteDiagramsDir={write_diagrams_dir}'.format(write_diagrams_dir=write_diagrams_dir))

    arglist.append('-I.')
    if args.include_path:
        arglist.append('-I{include}'.format(include=args.include_path))
    arglist.append("-I{macro_dir}".format(macro_dir=INCLUDE))
    if args.output:
        arglist.append('-o {}'.format(args.output))

    filelist = []
    if args.include_before_body:
        with open(args.include_before_body, 'r') as fd:
            before_text = fd.read()
    else:
        before_text = ''

        
    if args.replace_notation:
        before_text += '\n\n'
        with open('../_includes/talk-notation.tex', 'r') as fd:
            before_text += fd.read()

    # Read in talk-macros.gpp which loads in the other macro files.
    with open(os.path.join(INCLUDE, 'talk-macros.gpp')) as f:
        before_text += f.read()
            

    if args.include_after_body:
        with open(args.include_after_body, 'r') as fd:
            after_text = fd.read()
    else:
        after_text = ''

    default_file = '_config.yml'

    if os.path.isfile(default_file):
        with open(default_file, 'r') as f:
            writepost = fm.load(f)
    else:
        writepost = fm.loads("")
        
    if args.no_header:
        with open(args.filename) as f:
            writepost.content = f.read()
            
    else:
        with open(args.filename) as f:
            post = fm.load(f)
        writepost.metadata.update(post.metadata)
        writepost.content = post.content

    writepost.content = before_text + writepost.content + after_text
        
    tmp_file, ext = os.path.splitext(args.filename)
    tmp_file += '.gpp.markdown'
    
    with open(tmp_file,'wb') as fd:
        fm.dump(writepost, fd, sort_keys=False, default_flow_style=False)


    runlist = ['gpp'] + arglist + [tmp_file]
    print(' '.join(runlist))
    os.system(' '.join(runlist))

if __name__ == "__main__":
    sys.exit(main())
