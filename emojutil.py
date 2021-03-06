"""
Extract the full list of emoji and names from the Unicode Consortium and
apply as much formatting as possible so the codes can be dropped into the
emoji registry file.
Written and run with Python3.  Not tested on Python2 and definitely not
intended for production use.
http://www.unicode.org/Public/emoji/1.0/full-emoji-list.html
"""


import requests
from bs4 import BeautifulSoup
from collections import OrderedDict


url = 'http://www.unicode.org/emoji/charts/emoji-list.html'


response = requests.get(url)
response.raise_for_status()
soup = BeautifulSoup(response.text, "html.parser")

# with open('utils/content.html') as f:
#     soup = BeautifulSoup(f.read())

header = [
    'Count', 'Code', 'Sample', 'Name'
]
omit = [1199, 1207, 1203, 2602, 1440, 2248, 2249, ]
output = {}
for row in soup.find('table').find_all('tr'):
    cols = row.find_all('td')
    cols = [e.text.strip() for e in cols]
    try:
        if not cols[3][0].isalnum():
            continue
        if cols[1].find('U+200D')!=-1:
            if cols[3].find('kiss')!=-1:
                pass
            elif cols[3].find('couple with heart')!=-1:
                pass
            elif cols[3].find('eye in speech bubble')!=-1:
                pass
            elif cols[3].find('rainbow flag')!=-1:
                pass
            elif cols[3].find('family')!=-1 and int(cols[0])>=1222:
                #print(cols[0], '\t', cols[1], '\t', cols[3])
                continue
            elif cols[3].find('family')==-1:
                #print(cols[0], '\t', cols[1], '\t', cols[3])
                continue
        
        if cols[3].find('keycap')!=-1:
                continue
        
        if int(cols[0]) in omit:
            continue

    except IndexError:
        pass
    
    d = OrderedDict(zip(header, [e.strip() for e in cols]))
    
    if d:
        _code = []
        for c in d['Code'].split(' '):
            if len(c) is 6:
                _code.append(c.replace('+', '0000'))
            else:
                _code.append(c.replace('+', '000'))
        code = ','.join(_code)
        name = d['Name'].replace(' ', '_') \
                        .replace(':', '') \
                        .replace(',', '') \
                        .replace('“', '') \
                        .replace('”', '') \
                        .strip()

        #Replace the next line with the one below it if you want
        #a txt file formated as a proper OrderedDict. 
        #Note: You will also need to adjust the print statement
        char = code.replace('U', '') \
                    .replace(' ',',')
                
        #char = "u'" + code.replace('U', '\\U') + "'"

        output[name] = char

with open('emojinumcodes', 'w') as txt:
    for name in sorted(output.keys()):
        txt.write("{0}\n".format(output[name]))
        #print("    u':%s:': %s" % (name, output[name]))
