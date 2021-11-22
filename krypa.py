# TODO:
# Make so it doesn't only check the root of input. Make it recursive.
# This can be done by saving the results into an array and than go throu the array.

# Also check for more error than 404 since that is just for testing

# -----

# Automaticly search websites for directories and files
# Need wordlist, get one from internet, it's a great place!

# Only checks root input

import sys
import requests
import time

class Website:
    def __init__(self, url, wordlistfile):
        self.url = url
        self.wordlistfile = wordlistfile

def main(argv):
    website = Website(sys.argv[1], sys.argv[2])

    recursive = ''
    okaysites = [''] # Save found sites

    # Check if recursive is 1 or something else, if not 1 give it 0
    if len(sys.argv) >= 4:
        if sys.argv[3] == '1':
            recursive = 1
        else:
            recursive = 0

    wordlist = [''] # All words from wordlistfile

    website.url = checkUrlAndFile(website) # Check for errors in URL typing

    # Save all words to wordlist array
    with open(website.wordlistfile, 'r') as  f:
        for line in f.readlines():
            wordlist.append(line.replace('\n', ''))

    currenttime = time.time() # starttime for scan

    okaysites = runSites(website, wordlist, okaysites) # Check for hidden files and directories for first time
    
    # If recursive is choosen (argv[3] == 1)
    if recursive == 1:
        for i in range(2, len(okaysites)):
            temp = okaysites[i] + '/' # Take URL of found site and add /
            tempsite = Website(temp, argv[2])
            runSites(tempsite, wordlist, okaysites) # Run again with new site

    currenttime = time.time() - currenttime # New time after all searches
    print('Time: ', round(currenttime, 2), 's')

def runSites(Website, wordlist, okaysites):
    for i in range(0, len(wordlist)):
        s = Website.url + wordlist[i] # Check site + wordlist. https://example.com/api <-- Example
        r = requests.get(s) # Make a HTTP requst

        print(chr(27) + "[2J") # Make the output a bit prettier

        # URL "found" (not found, 404 only) add to array
        if r.status_code != 404:
            okaysites.append(s)

        # Print out the found URLs
        for x in okaysites:
            print(x)

        print(i+1 , ' of ' , len(wordlist))
    
    return okaysites

def checkUrlAndFile(Website):
    # Check if wordlist exists
    try:
        open(Website.wordlistfile)
    except:
        print('File not found!')
        sys.exit(1)

    try:
        # Add a / in the end of URL
        if Website.url[-1] != '/':
            Website.url = Website.url + '/'

        # Add http or https to URL
        if Website.url.find('http://', 0, 7) == -1 and Website.url.find('https://', 0, 8) == -1:
            print('Did not find HTTP, adding for you. Running in 2 sec again.')
            Website.url = 'http://' + Website.url
            time.sleep(2)

        print('Here')
        requests.get(Website.url)
    except:
        print('Failed to find website!')
        sys.exit(2)

    return Website.url

if __name__ == '__main__':
    # Check so program got an input, tell how it works
    if len(sys.argv) < 3:
        print('How to use:\npython krypa.py WEBSITE WORDLIST N')
        sys.exit(1)
    main(sys.argv[1:])