#! /usr/bin/env python
import sys
import argparse
import os.path
from scanner.scan import extract_commands
import os
import stat


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('rst_files', nargs='+')
    parser.add_argument('-v', '--verbose', default=False,
                        action='store_true')
    parser.add_argument('-x', '--hide-hidden', default=False,
                        action='store_true')
    parser.add_argument('-o', '--output', metavar="output",
                        type=argparse.FileType('wb'),
                        default=None, dest='output')
    args = parser.parse_args()

    if args.output:
        args.output.write('#! /bin/bash\n')

    for filename in args.rst_files:
        output = args.output
        if not output:
            output_name = os.path.basename(filename) + '.sh'
            output = open(output_name, 'w')
            output.write('#! /bin/bash\n')

            st = os.stat(output_name)
            os.chmod(output_name,
                     st.st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)

        extract_commands(filename, output, args.verbose, not args.hide_hidden)
        

if __name__ == '__main__':
    main()
