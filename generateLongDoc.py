#! /usr/bin/env python3.4
# -*- coding: UTF-8 -*-

import re, yaml, os, datetime
from os.path import isfile, isdir

folders = ["overview", "content", "templates", "taxonomies", "extras", "tutorials"]

def writeFile(path, content):
  f = open(path, "w")
  f.write(content)
  f.close()
  
titleRe = re.compile(r'^title: (.*)')
weightRe = re.compile(r'^weight: (.*)')
dividerRe = re.compile(r'^---')
linksBeforeRe = re.compile(r'\[(.*?)\]\(\/(.*?)\/(.*?)\/?\)', re.S)
  
for folder in folders:
    documents = {}
    for mdfile in os.listdir(folder):
        mdFilePath = folder + "/" + mdfile
        
        dividerCount = 0
        content = ""
        md = open(mdFilePath, 'r')
        for line in iter(md.readline, ''):
            if dividerCount == 2:
                content = content + line
            else:        
                m = re.match(titleRe, line)
                if m: title = m.group(1)
                    
                m = re.match(weightRe, line)
                if m: weight = m.group(1)

                m = re.match(dividerRe, line)
                if m: dividerCount = dividerCount + 1

        # fix internal links
        content = re.sub(linksBeforeRe, r'[\1](#\2.\3.md)', content)
                
        # add title, named anchor, content (indexed by weight)
        documents[int(weight)] = '<a name="%s.%s"></a>\n\n#%s\n\n%s' % (folder, mdfile, title, content)
        
    for key in sorted(documents):
        print(documents[key])


