#!/bin/env python

import getpass, sys, re, argparse
from HTMLParser import HTMLParser
from string import Template

import cli, page, fields
    
def add_macs(cid, idx=0, macs=[], force=False, dryrun=False):
        
    p = page.pageFromId(cid)

    print 80*"*"
    print cli.getPageTitle(cid)
    print 80*"*"
    print p
    print 80*"*"

    mac_fields = []
    if macs:
        for mac in macs:
            try:
                mac_fields.append(fields.MACField(idx, mac))
                idx += 1
            except ValueError:
                return False
    else:
       try:
            i=0
            print "<enter> to end MAC additions, . to abort this page"
            while True:
                NewMAC = raw_input("MAC ADDRESS: ").strip()
                if NewMAC == ".":
                  raise AbortPage
                if NewMAC == "":
                  break          
                else:
                    if i==0:
                        MACval = "MAC " + str(i) + ": " + NewMAC
                    else:
                        MACval = MACval + "<br>" + "MAC " + str(i) + ": " + NewMAC + "</br>"
                    i=i+1   
            p.addProperty("MAC Addresses", MACval)
        except fields.AbortPage:
            print "Page Aborted"
            return False

    print 80*"*"
    print cli.getPageTitle(cid)
    print 80*"*"
    print p
    print 80*"*"

    if dryrun:
        print "Dry Run, not writing to HWDB"
        return True

    return cli.storePage(p.getMarkup(), cid=cid)

def main(args):

    while True:
        try:
            pwd = getpass.getpass("Confluence password for %s: "\
                                      % getpass.getuser())
            rc = cli.login(getpass.getuser(), pwd, page.SPACE_KEY)
            break
        except cli.AuthFailure:
            pass

    if args.page:
        cid = page.extractPageId(args.page)
        if not cid:
            return False
    else:
        while True:
            try:
                cid = page.askForPageId()
                break
            except fields.AbortPage:
                print
                print "-ERROR- Page aborted."
            except KeyboardInterrupt:
                return False

    return add_macs(cid=cid, idx=args.idx, macs=args.macs,
                    force=args.force, dryrun=args.dryrun)

if __name__ == "__main__":

    desc = """ 
This program is used to update/add MAC address fields to the 
Hardeware Database. The MAC format will be checked to be 
consistent with the format UU:VV:WW:XX:YY:ZZ.
"""
    epilog = """
Parameters that are not supplied on the command line will be prompted for.

The IDX is the index of the first MAC address to be added/updated. MAC 
address fields in the HWDB have the form MAC%idx. IDX will default to 0.

The KEYWORD for searching for a page can be the pageId, URL, Short URL, 
AssetTag, Page Title, or other identifying content. It may need to be quoted. 
"""

    parser = argparse.ArgumentParser(description=desc,
                                     epilog=epilog,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument("-m", "--macs", metavar="MAC", nargs="+",
                        help="List of MAC addresses to assign")
    parser.add_argument("-i", "--idx", type=int, default=0,
                        help="Index of first MAC adress")

    parser.add_argument("-p", "--page",
                        help="Search term for HWDB page", 
                        metavar="KEYWORD")
    parser.add_argument("-f", "--force", help="Allow overwriting of existing values",
                        action="store_true")
    parser.add_argument("-d", "--dryrun", action="store_true",
                        help="Do not save new page to HWDB")

    args = parser.parse_args()

    sys.exit(main(args))
