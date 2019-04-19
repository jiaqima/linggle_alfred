#!/usr/bin/python
# encoding: utf-8

import sys
import argparse
from workflow import Workflow

import urllib2
import json


def main(wf):
    parser = argparse.ArgumentParser()
    parser.add_argument('--query', dest='query', default='')
    args = parser.parse_args(wf.args)
    # itemlist = [v for v in args.query.strip().split(' ') if v]
    # token='%20'.join(itemlist)
    token = args.query.strip().replace(' ', '%20').replace('?', '%3F').replace(
        '/', '%2F')
    page = urllib2.urlopen(
        u'http://www.linggle.com/query/%s' % token, timeout=1000)
    if page.getcode() == 200:
        # wf.add_item('Yes')
        # wf.send_feedback()
        result = json.loads(page.read())

        if not result:
            wf.add_item('No results')
            wf.send_feedback()
        else:
            for item in result:
                wf.add_item(
                    title=' '.join(item['phrase']).replace(
                        '<strong>', '').replace('</strong>', ''),
                    subtitle=item['percent'] + ', ' + item['count_str'])
            wf.send_feedback()
    else:
        wf.add_item('404')
        wf.send_feedback()
    return 0


if __name__ == u"__main__":
    wf = Workflow()
    sys.exit(wf.run(main))
