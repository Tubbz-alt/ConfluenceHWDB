#-*-Mode: Python;-*-
## @file
# @brief Information about particular pages, plus operations that compose or decompose pages.
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
# \$HeadURL: file:///afs/slac/g/reseng/svn/repos/hwdb/trunk/page.py $
#
# @par Credits:
# SLAC

# Python library.
import re, sys
from string import Template
from HTMLParser import HTMLParser
import urllib2

import cli

## @brief The short key used in URLs for the DAT group's Confluence space.
SPACE_KEY = "AIRTRACK"

## @brief URL for page ref by ID.
PAGE_URL_TEMPLATE = Template("https://confluence.slac.stanford.edu/pages/viewpage.action?pageId=$cid")

## @brief All hardware database pages are descendants of this one.
MASTER_PAGE = "Hardware database"

SITE_PARENT = "Hardware Sites"

## @brief Parent of blank ages.
BLANK_PARENT = "Unused HWDB pages"

## @brief The title for a newly formed page.
BLANK_TITLE_TEMPLATE = Template("HWDB $pageId")

class Field(object):
    def __init__(self, key, value="", link="", space=""):
        self.__key   = key
        self.__value = value
        self.__link  = link
        self.__space = space
        if not self.isValid():
            raise ValueError("Invalid Arguments to %s Field"%self.__key)

    def __str__(self):
        s = "%15s: "%self.__key
        if self.__value:
            s += self.__value
            s += " "
        if self.__space:
            s += self.__space+"/"
        if self.__link:
            s += self.__link
        return s
    
    def isValid(self):
        return True
        # While we still have blank pages with invalid fields
        # we can't apply this check.
        #return self.__key and (bool(self.__value)^bool(self.__link))

    def isBlank(self):
        if self.__value or self.__link or self.__space:
            return False
        return True

    def getKey(self):
        return self.__key

    def getValue(self):
        return self.__value

    def getLink(self):
        return self.__link

    def getSpace(self):
        return self.__space

    def update(self, value=None, link=None, space=None):
        if value: 
            self.__value = value
        if link:
            self.__link = link
        if space:
            self.__space = space

    def getMarkup(self, inline=False):
        if self.__link:
            value = self.__LINK_TEMPLATE.substitute({"type":self.__link,
                                                     "space":self.__space})
            value += " "+self.__value
        else:
            value = self.__value
        if not inline:
            return self.__FIELD_TEMPLATE.substitute({"KEY":self.__key, 
                                                     "VALUE":value})
        else:
            return self.__FIELD_TEMPLATE_INLINE.substitute({"KEY":self.__key, 
                                                            "VALUE":value})

    __FIELD_TEMPLATE = Template("""
    <ac:macro ac:name="section">
      <ac:rich-text-body>
        <p>
          <strong>$KEY:</strong> $VALUE
        </p>
      </ac:rich-text-body>
    </ac:macro>
    """)

    __FIELD_TEMPLATE_INLINE = Template("""
    <ac:macro ac:name="section">
      <ac:rich-text-body>
          <strong>$KEY:</strong> $VALUE
      </ac:rich-text-body>
    </ac:macro>
    """)

    __LINK_TEMPLATE = Template('<ac:link><ri:page ri:content-title="$type" ri:space-key="$space"/></ac:link>')

class InfoPanel:
    def __init__(self, fields):
        self.__fields = fields

    def __str__(self):
        s = ""
        for f in self.__fields:
            s += f+"\n"
        return s

    def getMarkup(self):
        markup = ""
        for f in self.__fields:
            markup += f.getMarkup()
        return self.__INFO_PANEL_TEMPLATE.substitute({"FIELDS":markup})

    __INFO_PANEL_TEMPLATE = Template(
 """
 <ac:macro ac:name="panel">
   <ac:parameter ac:name="borderStyle">solid</ac:parameter>
   <ac:rich-text-body>
     $FIELDS
   </ac:rich-text-body>
 </ac:macro>
 """)

class StatusPanel:
    def __init__(self, status):
        self.__status = status

    def __str__(self):
        return self.__status.__str__()

    def getMarkup(self):
        return self.__STATUS_PANEL_TEMPLATE.substitute({"FIELD":self.__status.getMarkup(inline=True)})
   
    __STATUS_PANEL_TEMPLATE = Template(
"""
<ac:macro ac:name="panel">
  <ac:parameter ac:name="bgColor">#d8eaff</ac:parameter>
  <ac:parameter ac:name="borderStyle">solid</ac:parameter>
  <ac:rich-text-body>
    <ac:macro ac:name="excerpt">
      <ac:parameter ac:name="">BLOCK</ac:parameter>
      <ac:parameter ac:name="atlassian-macro-output-type">BLOCK</ac:parameter>
      <ac:rich-text-body>
        $FIELD
      </ac:rich-text-body>
         </ac:macro>
  </ac:rich-text-body>
</ac:macro>
""")


class Properties(object): #Shows up as a table on the page
    def __init__(self, key=["Mating Board(s)", "Physical Location","Programming","Purchase Info","Fabricated By", "Testing", "Notes"],value=["-","-", "-", "-", "-","-", "-"], link="", space=""):
        self.__key   = key
        self.__value = value
        self.__link  = link
        self.__space = space
        if not self.isValid():
            raise ValueError("Invalid Arguments to %s Properties"%self.__key)

    def __str__(self):
        if self.__key:
            s += self.__key
            s += " "
        if self.__value:
            s += self.__value
            s += " "
        if self.__space:
            s += self.__space+"/"
        if self.__link:
            s += self.__link
        return s
    
    def isBlank(self):
        if self.__value or self.__link or self.__space:
            return False
        return True

    def isValid(self):
        return True
        # While we still have blank pages with invalid fields
        # we can't apply this check.
        #return self.__key and (bool(self.__value)^bool(self.__link))
    def getKey(self):
        return self.__key
    
    def getLKey(self):
        return len(self.__key)

    def getValue(self):
        return self.__value

    def getLValue(self):
        return len(self.__value)

    def getLink(self):
        return self.__link

    def getSpace(self):
        return self.__space

    def update(self, key=None, Kindex=0, value=None, Vindex=0, link=None, space=None):
        if key:
          if Kindex > 4: #For adding new entries
            self.__key.append(key)
          else: #For overwriting the defaults
            self.__key[Kindex]=key        
        if value:
          if Vindex > 4: #for adding new entries
            self.__value.append(value)
          else:   #For overwriting the defaults
            self.__value[Vindex]=value
        if link:
            self.__link = link
        if space:
            self.__space = space

    def getMarkup(self):
       
       Template_insert = ""
       for i in range(len(self.__key)): #turns the key/value objects into a string that can be inserted into the right place in the Template
        Template_insert = Template_insert + "<tr><td>" + self.__key[i] + "</td><td>" + self.__value[i] + "</td></tr>"
      

       PROPERTIES_TEMPLATE = self.__PROPERTIES_TEMPLATE1 + Template_insert + self.__PROPERTIES_TEMPLATE2
       return PROPERTIES_TEMPLATE
         
        
        
    __PROPERTIES_TEMPLATE1 = "<ac:structured-macro ac:macro-id=\"1dc754d0-d9b4-4309-9150-b4683060844a\" ac:name=\"details\" ac:schema-version=\"1\"><ac:rich-text-body><table><tbody><tr><td>HWDB Location</td><td><ac:structured-macro ac:macro-id=\"8242231c-7224-4df2-9536-63ceb7f114fd\" ac:name=\"parentpagelink\" ac:schema-version=\"1\" /></td></tr>"    
    
    __PROPERTIES_TEMPLATE2 = "<tr><td colspan=\"1\">Test Files</td><td colspan=\"1\"><ac:structured-macro ac:macro-id=\"7f63b545-91a2-4d3c-a4a0-bcca81689133\" ac:name=\"expand\" ac:schema-version=\"1\"><ac:rich-text-body><p><ac:structured-macro ac:macro-id=\"1635c6c0-7fd6-484c-a2b2-6e49eb7270c1\" ac:name=\"attachments\" ac:schema-version=\"1\"><ac:parameter ac:name=\"upload\">false</ac:parameter></ac:structured-macro></p></ac:rich-text-body></ac:structured-macro></td></tr></tbody></table><p>&nbsp;</p><p>&nbsp;</p></ac:rich-text-body></ac:structured-macro>"

    __LINK_TEMPLATE = Template('<ac:link><ri:page ri:content-title="$type" ri:space-key="$space"/></ac:link>')



class FieldParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.text = list()
        self.inSection = False
        self.inField = False
        self.fields = list()
        self.link = ""
        self.linkSpace = ""
        self.fieldmap = dict()

    def handle_starttag(self, tag, attrs):
        if tag == "ac:structured-macro" and ("ac:name", "section") in attrs:
            self.inSection = True
        elif self.inSection and tag == "ac:rich-text-body":
            self.inField = True
            self.link = None
            self.linkSpace = None
        elif tag == "ri:page" and self.inField:
            attrs = dict(attrs)
            self.link = attrs.get("ri:content-title","")
            self.linkSpace = attrs.get("ri:space-key","")

    def handle_data(self, data):
        if self.inField:
            # We keep all the data in an element since items such as
            # a non-breaking space are considered non-data items, i.e.,
            # "foo&nbsp;bar" contains two data items: "foo" and "bar".
            self.text.append(data)

    def handle_endtag(self, tag):
        if self.inSection and tag == "ac:structured-macro":
            self.inSection = False
        elif self.inSection and tag == "ac:rich-text-body":
            self.inField = False
            t = " ".join(self.text)
            mo = self.fieldRe.match(t)
            if mo:
                self.fields.append(mo.group(1))
                self.fieldmap[mo.group(1)] = Field(mo.group(1), 
                                                   mo.group(2),
                                                   self.link,
                                                   self.linkSpace)
            else:
                print "Bad field: %r" % t
            self.text = list()
            
    # A field should have two tokens separated by
    # either by a colon, whitespace or colon and whitespace.
    # The first token is the field name and the second is
    # the value.
    fieldRe = re.compile(r"\s*([^:\s]+):?\s*(.*)")

class Page:
    def __init__(self, pageSource=None):
        if pageSource:
            fp = FieldParser()
            fp.feed(pageSource)
            self.__fieldOrder = fp.fields
            self.__fieldMap   = fp.fieldmap
            self.__status = self.__fieldMap.pop("Status", None)
            self.__fieldOrder.remove("Status")
            self.__properties = Properties()

        else:
            self.__fieldOrder = []
            self.__fieldMap   = {}
            self.__status     = None
            self.__properties = Properties()

            
        if not self.__status:
            self.__status = Field("Status", " ")

    def __str__(self):
        s = ""
        for f in self.__fieldOrder:
            s += self.__fieldMap[f].__str__()+"\n"
        s+= self.__status.__str__()
        return s

    def isBlank(self):
        for f in self.__fieldMap.values():
            if not f.isBlank():
                return False
        return True

    def removeField(self, key):
        if key in self.__fieldOrder:
            self.__fieldOrder.remove(key)
            self.__fieldMap.pop(key)
            return True
        return False

    def getFieldOrder(self):
        return self.__fieldOrder
    
    def getFieldMap(self):
        return self.__fieldMap

    def getStatus(self):
        return self.__status

    def setStatus(self, value):
        self.__status.update(value = value)

    def addField(self, field, force=False):
        if field.getKey() not in self.__fieldMap:
            self.__fieldMap[field.getKey()] = field
            self.__fieldOrder.append(field.getKey())
            return True
        elif force:
            self.__fieldMap[field.getKey()] = field
            return True
        else:
            print "Page already contains field: %s"%field.getKey()
            return False
    
    def buildProperty(self):
      label = None
      value = None
      Lindex = 0
      Vindex = 0
      print "<enter> to end property keys, . to abort this page"
      while True:
          label = raw_input("Label: ").strip()
          if label == ".":
              raise AbortPage
          if label == "":
              break
          elif label == "Location":
              value = "<ac:structured-macro ac:macro-id=\"8242231c-7224-4df2-9536-63ceb7f114fd\" ac:name=\"parentpagelink\" ac:schema-version=\"1\" />"
              self.__properties.update(label,Lindex, value, Vindex)
              Lindex += 1
              Vindex += 1
          else:
            value = raw_input("Corresponding Value (<enter> for none): ").strip()
            if value == ".":
               raise AbortPage
            if value =="":
              value = "-"
            try:
              self.__properties.update(label,Lindex, value, Vindex)
              Lindex += 1
              Vindex += 1
            except ValueError:
              pass  
      return True            
       
    def addProperty(self,key, value):
      print self.__properties.getLKey()+2
      print self.__properties.getLValue()+2 
      self.__properties.update(key,self.__properties.getLKey()+2,value,self.__properties.getLValue()+2)
      return True
    
    def getMarkup(self):
        fields = []
        for f in self.__fieldOrder:
            fields.append(self.__fieldMap.get(f))
        info = InfoPanel(fields)
        status = StatusPanel(self.__status)
       
        
        return info.getMarkup() + status.getMarkup() + self.__properties.getMarkup()

    __ATTACHMENT_TEMPLATE = """
<ac:macro ac:name="attachments">
  <ac:parameter ac:name="upload">false</ac:parameter>
</ac:macro>
"""

def pageFromId(cid):
    source = cli.getPageSource(cid)
    return Page(source)

class PageInfoParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.pageId    = None
        self.pageTitle = None
        self.shortURL  = None
        self.dest      = None

    def handle_starttag(self, tag, attrs):
        m=dict(attrs)
        if "meta" == tag:
            if m.get("name")=="ajs-page-id":
                self.pageId = m["content"]
            elif m.get("name")=="ajs-page-title":
                self.pageTitle = m["content"]
        elif "link" == tag:
            if m.get("rel")=="shortlink":
                self.shortURL = m["href"]
        elif "input" == tag:
            if m.get("name") == "os_destination":
                self.dest = m["value"]

## @brief Extract a page ID from a string.
#
# The string may be either a series of decimal digits or 
# the URL of a page.
# returns None if neither form is seen.
def extractPageId(ref):
    cid = extractPageIdFromURL(ref)
    if cid: 
        return cid
    return extractPageIdFromText(ref)

def extractPageIdFromText(text):
    pages = cli.getContentList('"'+text+'"')
    if not pages:
        print >> sys.stderr, "No Pages Found"
        return None
    else:
        hwdb_pages = []
        for p in pages:
            ancestors = cli.getPageList(cid=p["Id"], ancestors=True)
            if SITE_PARENT in [t["Title"] for t in ancestors]:
                hwdb_pages.append(p)
    if len(hwdb_pages) == 1:
        return hwdb_pages[0]["Id"]

    print >> sys.stderr, "Search Text returned %i Pages"%len(hwdb_pages)
    if len(hwdb_pages):
        for i in range(len(hwdb_pages)):
            print "%2i: %s"%(i, hwdb_pages[i]["Title"])
        try:
            i = int(raw_input("Please choose the correct page: "))
        except KeyboardInterrupt:
            raise
        except:
            i = None
            
        while i not in range(len(hwdb_pages)):
            try:
                i = int(raw_input("Try again: "))
            except KeyboardInterrupt:
                raise
            except:
                i = None

        return hwdb_pages[i]["Id"]                                  
        
    return None

def extractInfoFromURL(url):
    try:
        req = urllib2.Request(url)

        if req.get_type() != "https": return None 
        if req.get_host() != "confluence.slac.stanford.edu": return None
        selector = req.get_selector()
        if not selector or selector == '/': return None
    except ValueError:
        return None

    idp = PageInfoParser()
    # renderRequest returns a string that is not parsable by HTMLParser
    # unless I remove a hidden field "{0}" 
    content = cli.renderRequest(selector)
    content = content.replace('"{0}"', "")
    try: 
        idp.feed(content)
    except:
        print >>sys.stderr, "Couldn't retrieve page in URL %s"%url
        return None

    # For some reason, short URLs don't render if password protected,
    # but they do report the page ID (via the destination) so we can
    # then use that to render again. 
    if idp.dest and not (idp.pageId or idp.pageTitle or idp.shortURL):
        content = cli.renderRequest(idp.dest)
        content = content.replace('"{0}"', "")
        idp.feed(content)

    return idp
        
def extractPageIdFromURL(url):

    info = extractInfoFromURL(url)
    if info:
        return info.pageId
    return None
    
def extractPageTitle(url):
    info = extractInfoFromURL(url)
    if info:
        return info.pageTitle
    return None

def extractPageShortURL(url):
    info = extractInfoFromURL(url)
    if info:
        return info.shortURL
    return None

def askForPageId():
   
    while True:
        ans = raw_input("URL, Page ID, ESN, Asset Tag, MAC, SLAC ID etc.: ")
        if not ans:
            continue

        cid = extractPageId(ans)
        if cid is None:
            print "-ERROR- Could not find a page ID in that."
        else:
            return cid
