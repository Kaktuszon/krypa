# TODO:
# Make so it doesn't only check the root of input. Make it recursive.
# This can be done by saving the results into an array and than go throu the array.

# Automaticly search websites for directories and files
# Need wordlist, get one from internet, it's a great place!

# Only checks root input

import sys
import requests
import time

def main(argv):
    website = sys.argv[1]
    wordlistfile = sys.argv[2]

    wordlist = [''] # All words from wordlist
    okaysites = [''] # All sites with a valid URL


    # Check if wordlist exists
    try:
        open(wordlistfile)
    except:
        print('File not found!')
        sys.exit(1)

    try:
        # Add a / in the end of URL
        if website[-1] != '/':
            website = website + '/'

        # Add http or https to URL
        if website.find('http://', 0, 7) == -1 and website.find('https://', 0, 8) == -1:
            print('Did not find HTTP, adding for you. Running in 2 sec again.')
            website = 'http://' + website
            time.sleep(2)

        requests.get(website)
    except:
        print('Failed to find website!')
        sys.exit(2)

    # Save all words to wordlist array
    with open(wordlistfile, 'r') as  f:
        for line in f.readlines():
            wordlist.append(line.replace('\n', ''))

    for i in range(0, len(wordlist)):
        s = website + wordlist[i] # Check site + wordlist. https://example.com/api <-- Example
        r = requests.get(s) # Make a HTTP requst

        print(chr(27) + "[2J") # Make the output a bit prettier

        # URL "found" (not found, 404 only) add to array
        if r.status_code != 404:
            okaysites.append(s)

        # Print out the found URLs
        for x in okaysites:
            print(x)

        print(i , ' of ' , len(wordlist))

if __name__ == '__main__':
    # Check so program got an input, tell how it works
    if(len(sys.argv)) <3:
        print('How to use:\npython krypa.py WORDLIST WEBSITE')
        sys.exit(1)
    main(sys.argv[1:])