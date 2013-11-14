import numpy as np
from google_utils import *

def get_presenters_to_ask(desired_date, username, password, docname, N_needed=2):
    """
    Return a ranked list of names and emails, along with the database.
    """
    # current data, unpack
    data, keys = fetch_from_google_docs(username, password, docname)
    key_names = ['name', 'email', 'last-presented', 'gone-until', 'going-on']
    for i in range(len(key_names)):
        assert key_names[i] == keys[i], 'fix yo api'
    names = data[keys[0]]
    emails = data[keys[1]]
    last = data[keys[2]]
    gone = data[keys[3]]
    going = data[keys[4]]
    
    # how many are needed, get rid of those who've gone
    going_names = np.array([])
    going_emails = np.array([])
    for i in range(going.size):
        if going[i] == 'None':
            continue
        if int(going[i]) < desired_date:
            going[i] = 'None'
        if going[i] == np.str(desired_date):
            going_names = np.append(going_names, names[i])
            going_emails = np.append(going_emails, emails[i])
            N_needed -= 1

    # check to see if any gone folks are back
    for i in range(gone.size):
        if gone[i] == 'None':
            continue
        if int(gone[i]) <= desired_date:
            gone[i] = 'None'

    # get dates, assess weights, draw needed
    eligible = (gone == 'None') & (going == 'None')
    if any(eligible):
        year = float(time.strftime('%Y')) * 10000.
        names = names[eligible]
        emails = emails[eligible]
        last = last[eligible].astype(np.float) - year

        # weight metric, update?
        w = np.random.rand(len(names)) / (last - last.min() + 1)
        ind = np.argsort(w)[::-1]
        going_names = np.append(going_names, names[ind])
        going_emails = np.append(going_emails, emails[ind])

    return going_names, going_emails, data

if __name__ == '__main__':

    import os

    u = os.environ['AC_USER']
    p = os.environ['AC_PASS']
    d = os.environ['AC_DOC']

    dd = 20131121
    print get_presenters_to_ask(dd, u, p, d)
