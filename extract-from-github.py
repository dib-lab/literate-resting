#! /usr/bin/env python
"""
Use literate-resting to extract Docker container build/execute instructions
from khmer-protocols (or other repos hosted on github).

Some config info is specified in the literate-resting.json file at the
root of the path you specify.

Usage:

   ./extract-from-github.py https://github.com/dib-lab/khmer-protocols/tree/ctb/mrnaseq

and then look in output/, especially 'build.sh'.

For more info, see:

   https://github.com/dib-lab/literate-resting/blob/master/docker/README.rst

To test:

% nosetests extract-from-github.py
"""
import sys
import urlparse
import json
import urllib
import argparse
import tempfile
import subprocess
import os
import stat
import glob

from scanner import scan, scantag


def parse_github_url(url):
    """
    Extract org/repo/branch/location from given URL (assumed to be github.com).
    """
    o = urlparse.urlparse(url)
    path = o.path
    path = path.split('/')

    assert o.hostname.endswith('github.com')

    if not path[0]:                     # first element of path often empty?
        path.pop(0)
    org = path.pop(0)
    repo = path.pop(0)
    if len(path) == 1 and path[0] == '': # this is a root URL => master branch.
        branch = 'master'
        location = '/'
    elif len(path) >= 2 and path[0] == 'tree': # this is NOT a root URL.
        path.pop(0)
        branch = path.pop(0)

        if len(path):
            location = '/' + '/'.join(path)
        else:
            location = '/'
    else:                               # unable to figure out format of URL :)
        assert 0, path

    return org, repo, branch, location


### some simple tests to run with 'nosetests'


def test_parse_github_url_1():
    url = 'https://github.com/dib-lab/khmer-protocols/'
    org, repo, branch, location = parse_github_url(url)
    assert org == 'dib-lab'
    assert repo == 'khmer-protocols'
    assert branch == 'master'
    assert location == '/'


def test_parse_github_url_2():
    url = 'https://github.com/dib-lab/khmer-protocols/tree/63384b1c42496aeeab50253f43c3b5a2addab98a/mrnaseq'
    org, repo, branch, location = parse_github_url(url)
    assert org == 'dib-lab'
    assert repo == 'khmer-protocols'
    assert branch == '63384b1c42496aeeab50253f43c3b5a2addab98a'
    assert location == '/mrnaseq'


def test_parse_github_url_3():
    url = 'https://github.com/dib-lab/khmer-protocols/tree/ctb/mrnaseq'
    org, repo, branch, location = parse_github_url(url)
    assert org == 'dib-lab'
    assert repo == 'khmer-protocols'
    assert branch == 'ctb'
    assert location == '/mrnaseq'


def load_config(json_str):
    """
    Load in the JSON config file.
    """
    config = json.loads(json_str)
    return config


def load_config_from_github(org, repo, branch, location):
    """
    Grab the JSON config file from github, named 'literate-resting.json'.
    """
    url = "https://raw.githubusercontent.com/{}/{}/{}{}/literate-resting.json".format(org, repo, branch, location)
    fp = urllib.urlopen(url)
    data = fp.read()
    return load_config(data)


### more tests, to run with 'nosetests'.


def test_load_config_from_github_1():
    conf = load_config_from_github('dib-lab', 'khmer-protocols', 'ctb',
                                   '/mrnaseq/')
    print conf
    assert conf['prefix'] == 'eel-pond'
    assert conf['filesGlob'] == '[1-3]*.rst'
    assert conf['format'] == 'reST'


def build_dockerdir(inp_filename, outdirname):
    """
    Extract Dockerfile and entrypoint info from the reST files.
    """
    print >>sys.stderr, 'building Dockerfile for {} in {}'.format(
        os.path.basename(inp_filename), outdirname)

    # extract the docker-specific commands in .rst files => Dockerfile
    fp = open(inp_filename)
    docker_cmds = list(scantag.parse_commands(fp,
                                              os.path.basename(inp_filename),
                                              'docker'))

    # extract the commands in .rst files => shell scripts
    fp = open(inp_filename)
    script_cmds = list(scan.parse_commands(fp,
                                           os.path.basename(inp_filename),
                                           show_hidden=False))

    # name the entrypoint script 
    entrypoint_script = os.path.basename(inp_filename) + '.sh'

    # write out the Dockerfile (which needs to know the entrypoint script name)
    dockerfp = open(os.path.join(outdirname, 'Dockerfile'), 'w')
    dockerfp.write("""\
FROM diblab/kp-base
{}
COPY {} /home
CMD ["/home/{}"]
""".format("".join(docker_cmds),
           entrypoint_script,
           entrypoint_script))
    dockerfp.close()

    # write out the entrypoint script for the docker machine
    entrypoint_fullname = os.path.join(outdirname, entrypoint_script)
    entryfp = open(entrypoint_fullname, 'w')
    entryfp.write("#! /bin/bash\n")
    entryfp.write("".join(script_cmds))
    entryfp.close()

    # chmod +x it
    st = os.stat(entrypoint_fullname)
    os.chmod(entrypoint_fullname, st.st_mode | stat.S_IEXEC)


def main():
    """
    Run the thing, do the stuff.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-o', '--output-dir', type=str, default='output',
                        help='directory for the output')
    parser.add_argument('--local-repo', type=str, default=None,
                        help='local copy of repo for testing & speed')
    parser.add_argument('github_url',
                        help='URL of the protocol.')
    args = parser.parse_args()

    url = args.github_url
    
    print 'looking at github url:'
    print '\t', url
    org, repo, branch, location = parse_github_url(url)

    # this is technically not required at this point; we could just use
    # the config from the cloned repo, which we get below. but it's fun.
    print 'loading config from', org, repo, branch, location
    conf = load_config_from_github(org, repo, branch, location)
    if branch == 'master':
        docker_tag = 'latest'
    else:
        docker_tag = branch

    workdir = tempfile.mkdtemp()

    if args.local_repo:
        clone_url = args.local_repo
    else:
        clone_url = 'http://github.com/{}/{}.git'.format(org, repo)

    # clone the repo:
    subprocess.call(['git', 'clone', clone_url, 'repo', '-b', branch],
                    cwd=workdir)

    # grab the reST files to wrap:
    fileglob = os.path.join(workdir, 'repo', location.lstrip('/'),
                            conf['filesGlob'])
    print 'looking for', conf['filesGlob'], 'in repo'
    files = glob.glob(fileglob)

    # build the output location:
    output_path = args.output_dir
    try:
        os.mkdir(output_path)
    except OSError:
        pass

    # create the directories for the docker stuff, & write build associated
    # Dockerfile and entrypoint scripts.
    output_list = []
    for filename in files:
        ident = os.path.basename(filename)
        if ident.endswith('.rst'):
            ident = ident[:-4]

        output_dir = os.path.join(output_path, 'docker-' + ident)
        try:
            os.mkdir(output_dir)
        except OSError:
            pass
        build_dockerdir(filename, output_dir) # create Dockerfile & entrypoint

        # keep track of what we built
        output_list.append((ident, 'docker-' + ident))

    # create the build commands for the Docker images.
    build_sh = os.path.join(output_path, 'build.sh')
    build_fp = open(build_sh, 'w')
    print >>build_fp, 'set -x'
    for ident, dirname in output_list:
        tagname = '{}/{}:{}'.format(conf['prefix'], ident, docker_tag)
        print >>build_fp, 'docker build -t {} {}'.format(tagname, dirname)
    build_fp.close()

    # chmod +x build.sh
    st = os.stat(build_sh)
    os.chmod(build_sh, st.st_mode | stat.S_IEXEC)

    print >>sys.stderr, '\nBuild commands in:', build_sh, '\n'


if __name__ == '__main__':
    main()
