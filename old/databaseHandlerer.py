from os import link

with open('links.txt', 'r', encoding='utf8') as f:
    for line in f:
        contents = line.strip()
        contentType = ''
        if contents.startswith('https') == True:
            contentType = 'link'
            linkOfItem = contents
        if contents.startswith('---') == True:
            contentType = 'divider'
        if contents.startswith('iPad') == True:
            contentType = 'name'
            nameOfItem = contents
        if contents.startswith('class') == True:
            contentType = 'class'
            classOfItem = contents
        print(contents, contentType)

