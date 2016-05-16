import time
import subprocess
import sys


pipes = []
command = [sys.executable, './logView.py']
pipe = subprocess.Popen(command, stdin=subprocess.PIPE)
pipes.append(pipe)
pipe.stdin.close()

pipe = pipes.pop()

status = True
i = 0

while i < 60:
    time.sleep(1)
    i += 1

if status:
    pipe.wait()
else:
    pipe.kill()
