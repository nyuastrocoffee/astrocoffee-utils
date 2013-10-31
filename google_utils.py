import gdata.docs
import gdata.docs.service
import gdata.spreadsheet.service

import numpy as np

def fetch_from_google_docs(username, password, docname):
    """
    Get the astrocoffee `database`
    """
    # client parameters
    gd_client = gdata.spreadsheet.service.SpreadsheetsService()
    gd_client.email = username
    gd_client.password = password
    gd_client.source = 'payne.org-example-1'

    # login
    gd_client.ProgrammaticLogin()

    # query the db
    q = gdata.spreadsheet.service.DocumentQuery()
    q['title'] = docname
    q['title-exact'] = 'true'
    feed = gd_client.GetSpreadsheetsFeed(query=q)
    spreadsheet_id = feed.entry[0].id.text.rsplit('/',1)[1]
    feed = gd_client.GetWorksheetsFeed(spreadsheet_id)
    worksheet_id = feed.entry[0].id.text.rsplit('/',1)[1]

    # get the data
    keys = np.array(['name', 'email', 'last-presented', 'gone-until', 'going-on'])
    rows = gd_client.GetListFeed(spreadsheet_id, worksheet_id).entry
    names = np.array([i.custom[keys[0]].text.strip() for i in rows])
    emails = np.array([i.custom[keys[1]].text.strip() for i in rows])
    last = np.array([i.custom[keys[2]].text.strip() for i in rows])
    gone = np.array([i.custom[keys[3]].text.strip() for i in rows])
    going = np.array([i.custom[keys[4]].text.strip() for i in rows])

    data = np.array([names, emails, last, gone, going])

    return data, keys


if __name__ == '__main__':
    import sys

    u = sys.argv[1]
    p = sys.argv[2]
    d = sys.argv[3]

    d, k = fetch_from_google_docs(u, p, d)
    print d
