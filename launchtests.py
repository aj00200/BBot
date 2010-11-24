#! /usr/bin/python
import subprocess
import time
while 1:
    test=subprocess.call(['python','autotest.py'])
    print('RESULTS: %s'%test)
    if test==0:
        icon='gtk-dialog-info'
    else:
        icon='gtk-dialog-warning'
    try:
        subprocess.call(['notify-send','Error Code: %s'%str(test),'--icon=%s'%icon])
    except:
        pass
    time.sleep(30)
