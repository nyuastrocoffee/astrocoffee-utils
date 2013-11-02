import time
import string
import gspread
import numpy as np
import gdata.calendar.client

def get_calender_events(username, password):
    """
    Get list of astrocoffee events, return next two dates
    """
    cc = gdata.calendar.client.CalendarClient(source='')
    cc.ClientLogin('nyuastrocoffee@gmail.com', 'nyuccpp2012', source='')

    today = time.strftime('%Y-%m-%d') 
    end_date = '-'.join([str(int(time.strftime('%Y'))+ 1),
                         time.strftime('%m-%d')])
    query = gdata.calendar.client.CalendarEventQuery(start_min=today, 
                                                     start_max=end_date)
    feed = cc.GetCalendarEventFeed(q=query)
    for i, event in zip(xrange(len(feed.entry)), feed.entry):
        if ((event.title.text == 'Astrocoffee') | \
                (event.title.text == 'Astrocoffee')):    
            events = [w.start[:10] for w in event.when]

    if events[0] == today:
        events = events[1:3]

    return events[:2]

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

    print get_calender_events(u, p)
