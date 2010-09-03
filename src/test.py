##
# Copyright (c) 2006-2010 Apple Inc. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
##

"""
Class that encapsulates a single CalDAV test.
"""

from src.request import request
from src.xmlUtils import getYesNoAttributeValue
import src.xmlDefs

class test( object ):
    """
    A single test which can be comprised of multiple requests. The test can
    be run more than once, and timing information gathered and averaged across
    all runs.
    """
    __slots__  = ['manager', 'name', 'details', 'count', 'stats', 'ignore', 'require_features', 'description', 'requests']
    
    def __init__( self, manager ):
        self.manager = manager
        self.name = ""
        self.details = False
        self.count = 1
        self.stats = False
        self.ignore = False
        self.require_features = set()
        self.description = ""
        self.requests = []
    
    def missingFeatures(self):
        return self.require_features - self.manager.server_info.features

    def parseXML( self, node ):
        self.name = node.get(src.xmlDefs.ATTR_NAME, "")
        self.details = getYesNoAttributeValue(node, src.xmlDefs.ATTR_DETAILS)
        self.count = int(node.get(src.xmlDefs.ATTR_COUNT, 1))
        self.stats = getYesNoAttributeValue(node, src.xmlDefs.ATTR_STATS)
        self.ignore = getYesNoAttributeValue(node, src.xmlDefs.ATTR_IGNORE)

        for child in node.getchildren():
            if child.tag == src.xmlDefs.ELEMENT_REQUIRE_FEATURE:
                self.parseFeatures( child )
            elif child.tag == src.xmlDefs.ELEMENT_DESCRIPTION:
                self.description = child.text

        # get request
        self.requests = request.parseList( self.manager, node )

    def parseFeatures(self, node):
        for child in node.getchildren():
            if child.tag == src.xmlDefs.ELEMENT_FEATURE:
                self.require_features.add(child.text.encode("utf-8"))

    def dump( self ):
        print "\nTEST: %s" % self.name
        print "    description: %s" % self.description
        for req in self.requests:
            req.dump()
