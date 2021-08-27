# Automaticly search websites for directories and files
# Need wordlist, get one from internet, it's a great place!

# Only checks root folder

import sys
import requests
import time

def main(argv):
    website = sys.argv[1]
    wordlistfile = sys.argv[2]

    try:
        open(wordlistfile)
    except:
        print('File not found!')
        sys.exit(1)

    try:
        if website[-1] != '/':
            website = website + '/'

        if website.find('http://', 0, 7) == -1 and website.find('https://', 0, 8) == -1:
            print('Did not find HTTP, adding for you. Running in 2 sec again.')
            website = 'http://' + website
            time.sleep(2)

        requests.get(website)
    except:
        print('Failed to find website!')
        sys.exit(2)

    wordlist = ['']
    okaysites = ['']
    with open(wordlistfile, 'r') as  f:
        for line in f.readlines():
            wordlist.append(line.replace('\n', ''))

    for i in range(0, len(wordlist)):
        s = website + wordlist[i]
        r = requests.get(s)

        print(chr(27) + "[2J")

        if r.status_code != 404:
            okaysites.append(s)

        for x in okaysites:
            print(x)

        print(i , ' of ' , len(wordlist))

if __name__ == '__main__':
    main(sys.argv[1:])