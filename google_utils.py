import string
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
    ws = gc.open(docname).sheet1

    # flattened list
    keys = ['name', 'email', 'last-presented', 'gone-until', 'going-on']
    db = [keys]
    Nrows = len(data[keys[0]])
    for i in range(Nrows):
        db.append([data[k][i] for k in keys])
    db = np.array(db).ravel()

    # list of cells
    end_letter = string.ascii_uppercase[len(keys) - 1]
    end_number = str(Nrows + 1)
    cell_list = ws.range(''.join(['A1:', end_letter, end_number]))

    # fill in cells
    for i, c in enumerate(cell_list):
        c.value = db[i]

    # update cells
    ws.update_cells(cell_list)

if __name__ == '__main__':

    import os

    u = os.environ['AC_USER']
    p = os.environ['AC_PASS']
    d = os.environ['AC_DOC']
    
    data, k = fetch_from_google_docs(u, p, d)
    
    insert_into_google_docs(u, p, d, data)
