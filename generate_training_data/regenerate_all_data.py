import os
from subprocess import call

for root, dirs, files in os.walk("."):
    if root == '.':
        continue
    call('python ' + root + '/generate_data.py', shell=True)

