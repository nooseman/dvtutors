#!c:\users\jackm\desktop\tutor\flask\scripts\python.exe
# EASY-INSTALL-ENTRY-SCRIPT: 'awsebcli==3.10.5','console_scripts','eb'
__requires__ = 'awsebcli==3.10.5'
import re
import sys
from pkg_resources import load_entry_point

if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    sys.exit(
        load_entry_point('awsebcli==3.10.5', 'console_scripts', 'eb')()
    )
