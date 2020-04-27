#!/bin/env python

import getpass, sys, re, argparse, subprocess
from HTMLParser import HTMLParser
from string import Template

import cli, page, fields

def add_label(cid, 
              label="",):
    
    p = page.pageFromId(cid)

    print 80*"*"
    print cli.getPageTitle(cid)
    print 80*"*"
    print p
    print 80*"*"

    if label: 
      cli.addLabel (label, cid)
    else:
      label = raw_input("Page Tag: ").strip()
      cli.addLabel (label, cid)
    return cli.storePage(p.getMarkup(), cid=cid)

def main(args):
    try:
        while True:
            try:
                pwd = getpass.getpass("Confluence password for %s: "\
                                          % getpass.getuser())
                rc = cli.login(getpass.getuser(), pwd, page.SPACE_KEY)
                break
            except cli.AuthFailure:
                pass

        cid = page.extractPageId(args.page)
            if not cid:
                return False

        return add_label(cid=cid, 
                         label=args.tag)

    except fields.AbortPage:
        print
        print "-ERROR- Page aborted."
    except KeyboardInterrupt:
        print
    return False


if __name__ == "__main__":

    desc = """ 
This program is used to update/add an arbitrary field to the 
Hardeware Database. 
"""
    epilog = """
Parameters that are not supplied on the command line will be prompted for.

The LABEL is used for the key of the field.

The VALUE is plain text that will be displayed right of the label.

The LINK and SPACE can be specified in place of the label if a link 
is desired. The SPACE will default to The Hardware Tracking Space.

The KEYWORD for searching for a page can be the pageId, URL, Short URL, 
AssetTag, Page Title, or other identifying content. It may need to be quoted. 
"""

    parser = argparse.ArgumentParser(description=desc,
                                     epilog=epilog,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument("-t", "--tag", metavar="LABEL",
                        help="The label to add")


    args = parser.parse_args()

    sys.exit(main(args))
    
