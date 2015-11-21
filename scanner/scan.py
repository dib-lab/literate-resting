import sys

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


