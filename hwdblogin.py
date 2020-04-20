#!/bin/env python
#-*-Mode: Python;-*-
## @file
# @brief Obtain a Confluence login token, prompting for a Confluence password
# for the current user using getpass so that it isn't echoed.  Prints
# the login token on stdout. Tokens are good for 60 minutes as long
# as you don't leave it unused for as long as 20 minutes.
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
# 2013/03/28
#
# @par Last commit:
# \$Date: 2017-08-04 14:29:49 -0700 (Fri, 04 Aug 2017) $ by \$Author: ruckman $.
#
# @par Revision number:
# \$Revision: 13682 $
#
# @par Location in repository:
# \$HeadURL: file:///afs/slac/g/reseng/svn/repos/hwdb/trunk/hwdblogin.py $
#
# @par Credits:
# SLAC

# Standard Python library.
import getpass, sys

# HWDB software.
import cli, page

def main():
    rc = cli.login(getpass.getuser(),
                   getpass.getpass("Confluence password for %s: " % getpass.getuser()),
                   page.SPACE_KEY)
    print cli.getToken()
    return 0

if __name__ == "__main__":
    try:
        sys.exit(main())
    except cli.AuthFailure, err:
        sys.exit(err.rc)
