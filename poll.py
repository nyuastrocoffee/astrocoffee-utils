import os
import string
import random

def render_question(dst_dir, ext, dn, dd, mn):
    """
    Insert date, and write the html.
    `dn`: Name of presentation day (e.g., 'Tuesday')
    `dd`: Number of presentation day (e.g., '3')
    `mn`: Name of month (e.g., 'October')
    """
    f = open('./reference_html/ask.html')
    l = f.readlines()
    f.close()

    # magic number 10
    line = l[10].split('-')
    l[10] = line[0] + dn + ', ' + mn + ' ' + dd + line[-1]

    # magic number -3                                                                                                  
    for i in range(3):
        line = l[-3 - i].split('-')
        l[-3 - i] = line[0] + ext + line[-1]
        print l[-3 - i]
    assert 0
    
    f = open(dst_dir + 'accept_' + ext + '.html', 'w')
    f.write(''.join(l))
    f.close()

def render_accept(dst_dir, ext, dn, dd, mn):
    """
    Insert date, and write the html.                                                                                  
    `dn`: Name of presentation day (e.g., 'Tuesday')                                                                  
    `dd`: Number of presentation day (e.g., '3')                                                                      
    `mn`: Name of month (e.g., 'October')                                                                             
    """
    f = open('./reference_html/accept.html')
    l = f.readlines()
    f.close()

    # magic number 9                                                                                                  
    line = l[9].split('-')
    l[9] = line[0] + dn + ', ' + mn + ' ' + dd + line[-1]

    # magic number -7                                                                               
    line = l[-7].split('.')
    l[-7] = line[0] + '_' + ext + '.' + ''.join(line[1:])

    f = open(dst_dir + 'accept_' + ext + '.html', 'w')
    f.write(''.join(l))
    f.close()


if __name__ == '__main__':
    
    DST_DIR = os.environ['AC_DIR']

    N = 32
    ext = ''.join(random.choice(string.ascii_letters + string.digits) for x in range(N))
    os.system('touch answer_' + ext + '.txt')
    os.system('chmod a+w answer_' + ext + '.txt')

    render_question(DST_DIR, ext, 'Tuesday', '3', 'October')
    render_accept(DST_DIR, ext, 'Tuesday', '3', 'October')
    print ext, DST_DIR
