import os
import string
import random

from calendar import day_name, month_name, weekday

def render(dst_dir, ext, date, kind):
    """
    Insert date and hashed ext, write the html.
    """
    files = ['ask.html', 'accept.html', 'decline.html', 'decline.php', 'remove.html']
    inserts = [(date, ext, ext, ext), (date, ext), (date, ext, ext), (ext), (ext)]
    assert kind in files

    f = open('./reference_html/' + kind)
    html = f.read()
    f.close()

    for i in range(len(files)):
        if kind == files[i]:
            insert = inserts[i]
    html = html % insert
    
    if kind == 'ask.html':
        f = open(dst_dir + ext + '.html', 'w')
    else:
        f = open(dst_dir + ext + '_' + kind, 'w')
    f.write(html)
    f.close()

    os.system('touch ' + dst_dir + 'answer_' + ext + '.txt')
    os.system('chmod a+w ' + dst_dir +'answer_' + ext + '.txt')

def poll(dst_dir, ext, next_date, following_date):
    """
    Build all the html
    """
    kinds = ['ask.html', 'accept.html', 'decline.html', 'decline.php', 'remove.html'] 
    for i in range(len(kinds)):
        if kinds[i] == 'decline.html':
            date = following_date
        else:
            date = next_date
        try:
            y = int(date[:4])
            m = int(date[4:6])
            d = int(date[6:])
            pretty_date = day_name[weekday(y, m, d)]
            pretty_date += ' '.join([',', month_name[m], str(d)])
        except:
            pretty_date = date

        render(dst_dir, ext, pretty_date, kinds[i])
    
    return pretty_date

if __name__ == '__main__':
    
    DST_DIR = os.environ['AC_DIR']

    N = 32
    ext = ''.join(random.choice(string.ascii_letters + string.digits) for x in range(N))

    date = 'Tuesday, October 7'
    render(DST_DIR, ext, date, 'ask.html')
    render(DST_DIR, ext, date, 'accept.html')
    date = 'Friday, October 11'
    render(DST_DIR, ext, date, 'decline.html')
    render(DST_DIR, ext, date, 'decline.php')
    render(DST_DIR, ext, date, 'remove.html')
