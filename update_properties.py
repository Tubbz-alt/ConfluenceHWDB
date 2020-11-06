#!/bin/env python

import getpass, sys, re, argparse, subprocess
from HTMLParser import HTMLParser
from string import Template

import cli, page
  
def updateProperty(cid):      
    p = page.pageFromId(cid)

    print 80*"*"
    print cli.getPageTitle(cid)
    print 80*"*"
    print p
    print 80*"*"
    while True:
      TypeChange = raw_input("Enter <0> to initialize, <1> to add new properties, <2> to change an existing property, <3> to remove a property, <.> to abort:" ).strip()
    
      if TypeChange == ".":
        raise AbortPage
    
      if TypeChange == "0":
        p.buildProperty()
        return cli.storePage(p.getMarkup(), cid=cid)    
    
      if TypeChange == "1":
        print "<enter> to end property additions, . to abort this page"
        while True:
          NewLabel = raw_input("New Label: ").strip()
          if NewLabel == ".":
            raise AbortPage
          if NewLabel == "":
            break
          try:
            NewValue = raw_input("Corresponding Value (<enter> for none): ").strip()
            if NewValue == ".":
              raise AbortPage
            if NewValue =="":
              break
            try:
              p.addProperty(NewLabel, NewValue)
              return cli.storePage(p.getMarkup(), cid=cid)            
            except ValueError:
              pass  
          except ValueError:
            pass

      if TypeChange == "2":
        try:
          for i in range(len(p.__properties.__key)):
           print "<" + i +"> "+  p.__properties.__key[i]
          while true:
            LabelChange = raw_input("To change a category name, select the corresponding <#>: ").strip()
            if LabelChange == ".":
             raise AbortPage
            if LabelChange == " ":
              break
            try:
             NewLabel = raw_input("New Label: ").strip()
             p.__properties.__key[i] = NewLabel
             for j in range(len(p.__properties.__value)):
              print "<"+j+"> "+p.__properties.__value[j] 
              ValueChange = raw_input("To change a category name, select the corresponding <#>: ").strip()
              if ValueChange == ".":
                raise AbortPage
              if ValueChange == " ":
                break
              try:
               NewValue = raw_input("New Value: ").strip()
               p.__properties.__key[j] = NewValue   
              except ValueError:
                pass
            except ValueError:
              pass
        except ValueError:
           pass
      
      if TypeChange == "3":
        try:
         for i in range(len(p.__properties.__key)):
          print "<"+i+"> "+p.__properties._key[i]
         while true:
           RemoveIndex = raw_input("To remove a category, select the corresponding <#>: ").strip()
           if RemoveIndex == ".":
            raise AbortPage
           if RemoveIndex == " ":
            break
           try:
            del p.__properties.__key[RemoveIndex]
            del p.__properties.__value[RemoveIndex]   
           except ValueError:
            pass
        except ValueError:
          pass
      
    print 80*"*"
    print cli.getPageTitle(cid)
    print 80*"*"
    print p
    print 80*"*"

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

        if args.page:
            cid = page.extractPageId(args.page)
            if not cid:
                return False
        else:
            while True:
                    cid = page.askForPageId()
                    break

        return updateProperty(cid)

    except KeyboardInterrupt:
        print
    return False


if __name__ == "__main__":

    desc = """ 
This program is used to update/add/remove fields from the properties table in the 
Hardeware Database. 
"""
    epilog = """
Parameters that are not supplied on the command line will be prompted for.

The LABEL is used for the key of the field (column 1).

The VALUE is plain text that corresponds to the LABEL (column 2).

The KEYWORD for searching for a page can be the pageId, URL, Short URL, 
AssetTag, Page Title, or other identifying content. It may need to be quoted. 
"""

    parser = argparse.ArgumentParser(description=desc,
                                     epilog=epilog,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument("-l", "--label", metavar="LABEL",
                        help="The label to add to column 1")

    valink_group = parser.add_mutually_exclusive_group()
    valink_group.add_argument("-v", "--value",
                              help="The value to add to column 2")
    

    parser.add_argument("-s", "--space",
                        help="Confluence space to find link in. Defaults to %s"%page.SPACE_KEY, 
                        default=page.SPACE_KEY)

    parser.add_argument("-p", "--page",
                        help="Search term for HWDB page", 
                        metavar="KEYWORD")

    args = parser.parse_args()

    sys.exit(main(args))
    
