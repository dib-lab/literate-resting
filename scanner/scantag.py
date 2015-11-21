import sys

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


