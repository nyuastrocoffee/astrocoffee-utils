import numpy as np
from google_utils import *

def get_presenters_to_ask(desired_date, username, password, docname):

    # current data, unpack
    data, keys = fetch_from_google_docs(username, password, docname)
    key_names = ['name', 'email', 'last-presented', 'gone-until', 'going-on']
    for i in range(len(key_names)):
        assert key_names[i] == keys[i], 'fix yo api'
    names = data[0]
    emails = data[1]
    last = data[2]
    gone = data[3]
    going = data[4]

    # how many are needed, get rid of those who've gone
    N_needed = 2
    for i in range(going.size):
        if going[i] == 'None':
            continue
        if int(going[i]) < desired_date:
            going[i] = 'None'
        if going[i] == np.str(desired_date):
            N_needed -= 1

    # check to see if any gone folks are back
    for i in range(gone.size):
        if gone[i] == 'None':
            continue
        if int(gone[i]) <= desired_date:
            gone[i] = 'None'

    # get dates, assess weights, draw needed
    eligible = (gone == 'None') & (going == 'None')
    ind = np.argsort(last[eligible].astype(np.int))
    drawn_names = names[eligible][ind][:N_needed]
    drawn_emails = emails[eligible][ind][:N_needed]

    return drawn_names, drawn_emails

if __name__ == '__main__':

    import sys

    u = sys.argv[1]
    p = sys.argv[2]
    d = sys.argv[3]

    dd = 20131105
    get_presenters_to_ask(dd, u, p, d)
