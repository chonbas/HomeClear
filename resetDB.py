import sys, os, os.path, subprocess
from subprocess import PIPE

if os.path.isfile("data-dev.sqlite"):
    os.remove("data-dev.sqlite")
p = subprocess.Popen(["python","manage.py", "shell"], stdin=PIPE)
p.communicate(input="db.create_all()\ndb.session.commit()\na=Inject()\na.injectData()\n")
p.terminate()
p.kill()
