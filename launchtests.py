import subprocess
import time
while 1:
    test=subprocess.call(['python','autotest.py'])
    print('RESULTS: %s'%test)
    subprocess.call(['notify-send',str(test)])
    time.sleep(30)
