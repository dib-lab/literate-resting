#! /usr/bin/env python
import urlparse
import json
import urllib
import argparse
import tempfile
import subprocess
import os
import glob

def parse_github_url(url):
    o = urlparse.urlparse(url)
    path = o.path
    path = path.split('/')

    assert o.hostname.endswith('github.com')
    if not path[0]:
        path.pop(0)
    org = path.pop(0)
    repo = path.pop(0)
    if len(path) == 1 and path[0] == '':
        branch = 'master'
        location = '/'
    elif len(path) >= 2 and path[0] == 'tree':
        path.pop(0)
        branch = path.pop(0)

        if len(path):
            location = '/' + '/'.join(path)
        else:
            location = '/'
    else:
        assert 0, path

    return org, repo, branch, location


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
    config = json.loads(json_str)
    return config


def load_config_from_github(org, repo, branch, location):
    url = "https://raw.githubusercontent.com/{}/{}/{}{}/literate-resting.json".format(org, repo, branch, location)
    fp = urllib.urlopen(url)
    data = fp.read()
    return load_config(data)


def test_load_config_from_github_1():
    conf = load_config_from_github('dib-lab', 'khmer-protocols', 'ctb',
                                   '/mrnaseq/')
    print conf
    assert conf['prefix'] == 'eel-pond'
    assert conf['filesGlob'] == '[1-3]*.rst'
    assert conf['format'] == 'reST'


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('github_url')
    args = parser.parse_args()

    url = args.github_url
    
    print 'looking at github url', url
    org, repo, branch, location = parse_github_url(url)

    print 'loading config from', org, repo, branch, location
    conf = load_config_from_github(org, repo, branch, location)

    workdir = tempfile.mkdtemp()
    
    clone_url = 'http://github.com/{}/{}.git'.format(org, repo)
    subprocess.call(['git', 'clone', clone_url, 'repo', '-b', branch],
                    cwd=workdir)
    fileglob = os.path.join(workdir, 'repo', location.lstrip('/'),
                            conf['filesGlob'])
    print fileglob
    files = glob.glob(fileglob)
    print files


if __name__ == '__main__':
    main()
