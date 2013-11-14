#
# Run utils to get speakers, update database
#
import time

from get_presenters import *
from google_utils import *
from email_utils import *
from poll import *

def get_extention(N=32):
    return ''.join(random.choice(string.ascii_letters + string.digits) for x in range(N))

def react_to_answer(username, password, docname, db, name, answer, next):
    """
    Update the database, according to the response.
    """
    try:
        assert name in db['name']
    except:
        return db

    ind = (db['name'] == name)

    if answer[0] == 'accept':
        db['last-presented'][ind] = next
        db['going-on'][ind] = next
    if answer[0] == 'gone':
        date = answer[1]
        date = ''.join(['20', date[4:], date[2:4], date[:2]])
        db['gone-until'][ind] = date
        db['going-on'][ind] = 'None'
    if answer[0] == 'willgo':
        date = answer[1]
        date = ''.join(['20', date[4:], date[2:4], date[:2]])
        db['gone-until'][ind] = date
        db['going-on'][ind] = date
        db['last-presented'][ind] = date
    if answer[0] == 'remove':
        ind = np.where(db['name'] != name)[0]
        keys = db.keys()
        for k in keys:
            db[k] = db[k][ind]
        
    insert_into_google_docs(username, password, docname, db)
    return db

# account info
username = os.environ['AC_USER']
password = os.environ['AC_PASS']
docname = os.environ['AC_DOC']
dst_dir = os.environ['AC_DIR']
home_dir = os.environ['HOME']
base_url = 'http://cosmo.nyu.edu/astrocoffee/'

# get dates of next two astrocoffee discussions
next_date, following_date = get_calender_events(username, password)

# get the names of people to ask
names, emails, db = get_presenters_to_ask(int(next_date), username, password, docname)

# general astrocoffee email list
f = open(dst_dir + 'astrocoffee_utils/astrocoffee_email_list.txt')
email_list = ', '.join(f.read().split())
f.close()

# launch the poll, soo much spaghetti.
Nspeakers = 2
sleep = 5 * 60
subject = 'You are needed for Astrocoffee!'
message = dst_dir + 'astrocoffee-utils/poll_message.txt'

N = Nspeakers
exts = [get_extention() for i in range(N)]
inds = [i for i in range(N)]
start = time.time()
next = inds[-1]

print names
print next_date, following_date

if N > 0:
    while True:

        # wait for a bit
        time.sleep(sleep)

        # if over max time, stop
        if (time.time() - start > max_time):
            break

        # add new url and name to list if necessary
        if (len(exts) != N) & (next + 1 < len(names)):
            exts.append(get_extention())
            next += 1
            inds.append(next)

        # check over url list
        ext_pop = []
        for i, ind in enumerate(inds):
            
            # does the html exist?
            if os.path.isfile(dst_dir + exts[i] + '.html'):

                # read answer file, react
                f = open(''.join([dst_dir, 'answer_', exts[i], '.txt']))
                answer = f.read().split()
                f.close()
                if len(answer) > 0:
                    db = react_to_answer(username, password, docname, db, 
                                         names[ind], answer, next_date)
                    ext_pop.append(i)
                    print names[ind], answer
                    if answer[0] == 'accept':
                        print names[ind], answer
                        N -= 1

            # create html, send email, if needed
            else:
                date = poll(dst_dir, exts[i], next_date, following_date)
                send_email(emails[ind], date, ''.join([base_url, exts[i], '.html']), 
                           username, password, subject, message)

        # get rid of people who answered
        for i in range(len(ext_pop)):
            exts.pop(ext_pop[i])
            inds.pop(ext_pop[i])

        current_date = time.strftime('%Y%m%d')

        # if it is 4pm the day before, send out cancellation.
        if (current_date == str(int(next_date) - 1)) & (time.strftime('%H') == '16'):

            subject = 'No Astrocoffee tomorrow, unless YOU want to present.'
            message = dst_dir + 'astrocoffee-utils/gonna_cancel.txt'
            send_email(email_list, date, None, username, password, subject, message)

        # if it is the day of, send reminder email
        if current_date == next_date:
            
            subject = 'Reminder: Astrocoffee today at 11am'
            message = dst_dir + 'astrocoffee-utils/reminder.txt'
            send_email(email_list, date, None, username, password, subject, message)

            # update cronjob
            job = ' '.join(['15', '11', time.strftime('%d'), time.strftime('%m'),
                            '* . $HOME/.bashrc;', dst_dir + 'astrocoffee.py > log.txt\n'])
            os.chdir(home_dir)
            f = open('cronfile', 'w')
            f.write(job)
            f.close()
            os.system('crontab -r; crontab cronfile')
            break

# clean up the files
os.system(''.join(['rm ', dst_dir, '*html;', 'rm ', dst_dir, '*txt;'
                   'rm ', dst_dir, '*php']))
