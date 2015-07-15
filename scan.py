#! /usr/bin/env python
import sys
import argparse
import os.path

# Originally authored by Leigh Sheneman for the khmer-protocols
# project.  Transferred w/o change to literate-resting project by
# C. Titus Brown and updated thereafter as in the git log
# (see: github.com/dib-lab/literate-resting)


def parse_commands(fp, sourcename, verbose=False):
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
            if line.startswith('::') or line.startswith('.. ::'):
                yield '\n### code block at %s:%d\n\n' % (sourcename, line_no)
                incode = True
                continue
            elif line and not line.startswith('   '):
                incode = False
                continue

        if inshell and incode:
            if verbose:
                print 'extract', sourcename, line_no, (rawline,)
            yield rawline[3:]


def extract_commands(inpfile, output_fp, verbose=False):
    fp = open(inpfile)

    emitted = 0
    for line in parse_commands(fp, inpfile, verbose):
        output_fp.write(line)
        emitted += 1

    print >>sys.stderr, "Extracted %d lines from %s" % (emitted,
                                                        inpfile)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('rst_files', nargs='+')
    parser.add_argument('-v', '--verbose', default=False,
                        action='store_true')
    args = parser.parse_args()

    for filename in args.rst_files:
        output_name = os.path.basename(filename) + '.sh'
        output = open(output_name, 'w')
        extract_commands(filename, output, args.verbose)

if __name__ == '__main__':
    main()