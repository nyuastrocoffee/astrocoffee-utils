import time

def load_db(filename='astrocoffee_db.txt'):
    """
    load the 'db', which is just a text file with:
    First Last id last_presented gone_until status
    """
    # read in the file
    idx = []
    f = open(filename)
    lines = f.readlines()
    f.close()

    # db definition
    keys = ['firstname', 'lastname', 'id', 'last',
            'gone', 'status']
    Nkeys = len(keys)
    db = {key: [] for key in keys}

    # load db
    for l in lines:
        if l == '\n':
            continue
        l = l.split()
        assert len(l) == Nkeys
        for i in range(Nkeys):
            db[keys[i]].append(l[i])

    return db, keys
    
def assign_response(id, response, gone=None, filename='astrocoffee_db.txt'):
    """
    Assign response.
    """
    # load db file
    db, keys = load_db()

    # assign response
    if response == 'accept':
        db['status'][id] = 'Presenting'
    elif response == 'decline':
        db['status'][id] = 'Declined'
    else:
        db['status'][id] = 'Remove'

    # update gone data
    if gone is not None:
        db['gone'][id] = '20' + gone[4:] + gone[2:4] + gone[:2]

    write_db(db, keys)

def write_db(db, keys, filename='astrocoffee_db.txt'):
    # write db
    f = open(filename, 'w')
    for i in range(len(db[keys[0]])):
        line = ' '.join([db[k][i] for k in keys]) + '\n'
        f.write(line)
    f.close()

def reset_db():
    """
    Reset db for next astrocoffee.
    """
    # load db file
    db, keys = load_db()

    # current date as YYYYMMDD
    today = time.strftime('%Y%m%d')

    # check status, update last_presented, flag to remove
    idx = []
    for i in range(len(db[keys[0]])):
        # reset status
        status = db['status'][i]
        if status == 'Presenting':
            db['last'][i] = today
            db['status'][i] = 'None'
        elif status == 'Declined':
            db['status'][i] = 'None'
        elif status == 'Remove':
            idx.append(i)
            db['status'][i] = 'None'

        # check if the person is back, if gone
        try:
            if int(today) > int(db['gone'][i]):
                db['gone'][i] = 'None'
        except:
            pass

    # remove people, if desired
    if len(idx) != 0:
        for k in keys:
            for i in idx:
                db[k].pop(i)
        db['id'] = [str(i) for i in range(len(db[keys[0]]))]

    write_db(db, keys)

if __name__ == '__main__':

    db, k = load_db()
    print db,'\n'
    assign_response(3, 'accept')
    assign_response(1, 'decline')
    assign_response(0, 'remove')
    db, k = load_db()
    print db,'\n'
    reset_db()
    db, k = load_db()
    print db,'\n'
    
