#!/usr/bin/env python3

import sys
import argparse
import lynguine.util.talk as nt
import lynguine.util.yaml as ny

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("dependency",
                        type=str,
                        choices=[
                            "all",
                            "diagrams",
                            "inputs",
                            "bibinputs",
                            "slidediagrams",
                            "texdiagrams",
                            "docxdiagrams",
                            "snippets",
                        ],
                        help="The type of dependency that is required")
    parser.add_argument("filename",
                        type=str,
                        help="The filename where dependencies are being searched")

    parser.add_argument("-d", "--diagrams-dir", type=str, help="Directory to find the diagrams in")
    parser.add_argument("-S", "--snippets-path", type=str, help="Directory to find the snippets in")


    args = parser.parse_args()

    diagrams_dir = "/Users/neil/lawrennd/slides/diagrams"
    if args.diagrams_dir:
        diagrams_dir = args.diagrams_dir

    snippets_path = ".."
    if args.snippets_path:
        snippets_path = args.snippets_path

    if args.dependency == "all":
        try:
            # Check if posts: true is set
            fields = ny.header_fields(args.filename)
            posts_enabled = False
            try:
                posts_enabled = ny.header_field('posts', fields, ["_lamd.yml", "_config.yml"])
            except ny.FileFormatError:
                posts_enabled = False
            if posts_enabled:
                # Now check for postsdir
                iface = ny.Interface.from_file(["_lamd.yml", "_config.yml"], directory=".")
                if 'postsdir' not in iface:
                    print("Error: 'postsdir' is not defined in your _lamd.yml configuration file.")
                    print("Please add a 'postsdir' entry pointing to your posts directory.")
                    print("Example:")
                    print("postsdir: ../_posts")
                    sys.exit(1)
            listfiles = nt.extract_all(args.filename, user_file=["_lamd.yml", "_config.yml"])
        except ny.FileFormatError as e:
            print(f"Error: {e}")
            sys.exit(1)
        print(" ".join(listfiles))

    elif args.dependency == "diagrams":
        listfiles = nt.extract_diagrams(args.filename,
                                        diagrams_dir=diagrams_dir,
                                        snippets_path=snippets_path)
        print(" ".join(listfiles))

    elif args.dependency == "slidediagrams":
        listfiles = nt.extract_diagrams(args.filename,
                                        absolute_path=False,
                                        diagram_exts=["svg"],
                                        diagrams_dir=diagrams_dir,
                                        snippets_path=snippets_path)
        print(" ".join(listfiles))

    elif args.dependency == "texdiagrams":
        listfiles = nt.extract_diagrams(args.filename,
                                        absolute_path=False,
                                        diagram_exts=["pdf"],
                                        diagrams_dir=diagrams_dir,
                                        snippets_path=snippets_path)
        print(" ".join(listfiles))

    elif args.dependency == "docxdiagrams":
        listfiles = nt.extract_diagrams(args.filename,
                                        absolute_path=False,
                                        diagram_exts=["emf"],
                                        diagrams_dir=diagrams_dir,
                                        snippets_path=snippets_path)
        print(" ".join(listfiles))
        
    elif args.dependency == "inputs":    
        listfiles = nt.extract_inputs(args.filename, 
                                      snippets_path=snippets_path)
        if len(listfiles)>0:
            print(" ".join(listfiles))
        else:
            print("")

    elif args.dependency == "bibinputs":
        listfiles = nt.extract_bibinputs(args.filename)
        print(" ".join(listfiles))

    elif args.dependency == "snippets":
        listfiles = nt.extract_snippets(args.filename,
                                        absolute_path= False,
                                        snippets_path=snippets_path)
        print(" ".join(listfiles))

if __name__ == "__main__":
    sys.exit(main())
    
