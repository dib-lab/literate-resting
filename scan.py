#! /usr/bin/env python
import sys
import argparse
import os.path

# Originally designed by CTB, Michael Crusoe, and Leigh Sheneman for
# the khmer-protocols project.  An initial shell script implementation was
# implemented by Leigh, and then transferred w/o change to
# literate-resting project by C. Titus Brown and updated thereafter as
# in the git log (see: github.com/dib-lab/literate-resting).  This is a
# Python rewrite.


def parse_commands(fp, sourcename, verbose=False, show_hidden=True):
    inshell = False
    incode = False

    for line_no, rawline in enumerate(fp):
        line = rawline.rstrip()
        if line.startswith('.. shell start'):
            inshell = True
            continue
        elif line.startswith('.. shell stop'):
            inshell = False
            incode = False
            continue
        elif inshell:
            if verbose:
                print 'examine', sourcename, line_no, incode, (rawline,)

            if line.startswith('::'):
                yield '\n### code block at %s:%d\n\n' % (sourcename, line_no)
                incode = True
                hidden = False
                continue
            elif line.startswith('.. ::') and show_hidden:
                yield '\n### hidden code block at %s:%d\n\n' % (sourcename,
                                                                line_no)
                incode = True
                hidden = True
                continue
            elif line and not line.startswith('   '):
                incode = False
                hidden = False
                continue

        if inshell and incode:
            if verbose:
                print 'extract', sourcename, line_no, (rawline,)
            if not hidden or show_hidden:
                yield rawline[3:]


def extract_commands(inpfile, output_fp, verbose=False, show_hidden=True):
    fp = open(inpfile)

    emitted = 0
    for line in parse_commands(fp, inpfile, verbose, show_hidden):
        output_fp.write(line)
        emitted += 1

    print >>sys.stderr, "Extracted %d lines from %s" % (emitted,
                                                        inpfile)


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

    for filename in args.rst_files:
        if not args.output:
            output_name = os.path.basename(filename) + '.sh'
            output = open(output_name, 'w')
        else:
            output = args.output

        extract_commands(filename, output, args.verbose, not args.hide_hidden)

if __name__ == '__main__':
    main()
