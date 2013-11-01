import gspread
import numpy as np

def fetch_from_google_docs(username, password, docname):
    """
    Get the astrocoffee `database`
    """
    # connect
    gc = gspread.login(username + '@gmail.com', password)
    ws = gc.open(docname).sheet1

    # get the data
    db = np.array(ws.get_all_values())

    data = {}
    keys = db[0]
    for i in range(len(keys)):
        data[keys[i]] = db[1:, i]

    return data, keys

def insert_into_google_docs(username, password, docname, data):
    """
    Update the db.
    """
    # connect
    gc = gspread.login(username + '@gmail.com', password)
    ws = gc.open(docname)

if __name__ == '__main__':

    import os

    u = os.environ['AC_USER']
    p = os.environ['AC_PASS']
    d = os.environ['AC_DOC']

    d, k = fetch_from_google_docs(u, p, d)
    print d
