import subprocess
p = subprocess.run("conda update conda", capture_output=True)
if p.stderr:
    if "SSLError" in str(p.stderr):
        print("Found SSLError")
        # Fix inside-firewall-SSLError
        subprocess.run("conda config --set ssl_verify false")
        subprocess.run("conda update conda", shell=True)
        # TODO Incorporate this script in the normal conda update script
        # TODO Carefully make ssl_verify true at end of base + project scripts
