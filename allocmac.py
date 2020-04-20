#!/bin/env python
#-*-Mode: Python;-*-
## @file
# @brief Allocate a free MAC address and print it to stdout.
# @verbatim
#                               Copyright 2014
#                                    by
#                       The Board of Trustees of the
#                    Leland Stanford Junior University.
#                           All rights reserved.
# @endverbatim
#
# @par Facility:
# DAT
#
# @author
# Stephen Tether <tether@slac.stanford.edu>
#
# @par Date created:
# 2014/03/28
#
# @par Last commit:
# \$Date: 2017-08-04 14:29:49 -0700 (Fri, 04 Aug 2017) $ by \$Author: ruckman $.
#
# @par Revision number:
# \$Revision: 13682 $
#
# @par Location in repository:
# \$HeadURL: file:///afs/slac/g/reseng/svn/repos/hwdb/trunk/allocmac.py $
#
# @par Credits:
# SLAC

# Python standard library
import getpass, optparse, sys

# HWDB software.
import macaddr

DEFAULT_MACFILE = "/afs/slac/g/reseng/hwdb/macfile"

def main(macfile):
    allocated = macaddr.allocate(1, macfile)
    if not allocated:
        print >>sys.stderr, "allocmac.py: Out of MAC addresses!"
        return 2
    print allocated[0]
    return 0

if __name__ == "__main__":
    p = optparse.OptionParser("allocmac.py --macfile MACFILE")
    p.add_option("--macfile",  metavar="MACFILE",
                 help="Optional. The file containing information on MAC address allocation.",
                 default=DEFAULT_MACFILE)
    opts, args = p.parse_args()
    sys.exit(main(opts.macfile))
