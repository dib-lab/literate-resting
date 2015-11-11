#! /usr/bin/env python
import sys
import argparse
import os.path

def parse_commands(fp, sourcename, tagname, verbose=False):
    tagline = '.. %s::' % (tagname,)

    if verbose:
        print 'tagline is:', (tagline,)

    incode = False
    for line_no, rawline in enumerate(fp):
        line = rawline.rstrip()
        if verbose:
            print 'examine', sourcename, line_no, incode, (rawline,)

        if line.startswith(tagline):
            yield '\n### tag block at %s:%d\n\n' % (sourcename, line_no)
            incode = True
            continue
        elif line and not line.startswith('   '):
            incode = False
            continue

        if incode:
            if verbose:
                print 'extract', sourcename, line_no, (rawline,)
            yield rawline[3:]


def extract_commands(inpfile, output_fp, tagname, verbose=False):
    fp = open(inpfile)
    
    emitted = 0
    for line in parse_commands(fp, inpfile, tagname, verbose):
        output_fp.write(line)
        emitted += 1

    print >>sys.stderr, "Extracted %d lines from %s" % (emitted,
                                                        inpfile)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('tagname')
    parser.add_argument('rst_files', nargs='+')
    parser.add_argument('-v', '--verbose', default=False,
                        action='store_true')
    parser.add_argument('-o', '--output', metavar="output",
                        type=argparse.FileType('wb'),
                        default=None, dest='output')
    args = parser.parse_args()

    for filename in args.rst_files:
        if not args.output:
            output_name = os.path.basename(filename) + '.sh'
            output = open(output_name, 'w')
        else:
            output = args.output

        extract_commands(filename, output, args.tagname, args.verbose)

if __name__ == '__main__':
    main()
