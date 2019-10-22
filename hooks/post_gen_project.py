import subprocess


# *Initialise git repo for newly created project
subprocess.call(['git', 'init'])
subprocess.call(['git', 'add', '*'])
subprocess.call(['git', 'commit', '-m', 'Initial commit'])

# ?Automate remote repo creation?