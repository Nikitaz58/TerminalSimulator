
def log(string):
    print(string)

def cls():
    from sys import platform
    os.system('cls')
    if platform == 'win32' or platform == 'win64':
        os.system('cls')
    else:
        os.system('clear')


def r_disk(path, disk):
    if len(path) == 1:
        if path[0] == disk:
            return True
        else:
            return False
    else:
        return False


def cRezWord(word, word_system):
    c = False
    for i in word_system:
        if c == word:
            c = True
            break
    return c


import os
from time import sleep
from Terminal.core import plugin

class Terminal():
    def __init__(self, data, r_t, lang):
        cls()
        if lang == 'ru':
            from Terminal.localization import ru as lang
        elif lang == 'en':
            from Terminal.localization import en as lang
        else:
            from Terminal.localization import en as lang
        self.lang = lang
        log(lang.start_terminal)
        self.timer = 1
        sleep(self.timer)
        self.core_version = '1.2'
        self.r_t = r_t
        self.sys_path = os.path.join('Terminal','disk')
        self.path = ''

        self.warning = []
        self.word_system = ['system']

        log(lang.login_in_system)
        sleep(self.timer)
        Terminal.__loginsystem__(self, data)
        sleep(self.timer)
        print(self.lang.loading_plugins)
        cls()
        plugin.LoadPlugins()
        input(self.lang.press_enter)


    def __loginsystem__(self, data):
        print(self.lang.auth_user)
        sleep(self.timer)
        sleep(self.timer)
        self.user = 'User'
        if data['user'] is None:
            self.group = 'guest'
            self.warning.append(self.lang.user_login_in_guest)
            self.authorization = True
        else:
            user = os.path.join(self.sys_path, 'system', 'users', data['user'] + '.u')
            if os.path.exists(user):
                from hashlib import sha224
                from json import loads
                f = open(user)
                file = loads(f.read())
                if file['password'] == sha224(data['pass'].encode()).hexdigest():
                    self.group = file['group']
                    self.user = data['user']
                    self.warning.append(self.lang.user_login.format(self.user, file['group']))
                    self.authorization = True
                else:
                    self.warning.append(self.lang.wrong_password)
                    self.authorization = False
            else:
                self.group = 'guest'
                self.warning.append(self.lang.account_not_exists)
                self.authorization = True
        input(self.lang.press_enter)


    def __createdisk__(self):
        while 1:
            cls()
            print(self.lang.disk_name_future)
            s = input('{}@{}:~$ '.format(self.user, self.group))
            check = True
            if s == '' or s.strip() == '':
                continue
            for i in self.word_system:
                if i == s:
                    check = False
                    print(self.lang.name_reserved)
                    input(self.lang.press_enter)
            if check:
                print(self.lang.creating_disk)
                sleep(self.timer)
                sleep(self.timer)
                os.mkdir(os.path.join(self.sys_path, s))
                self.path = s
                print(self.lang.disk_create.format(s))
                break


    def run_disk(self):
        from Terminal.libs.prettytable.prettytable import PrettyTable
        while 1:
            cls()
            path = os.listdir(self.sys_path)
            if path == [] or r_disk(path, self.word_system[0]):
                print(self.lang.disk_not_exists_next_menucreate)
                input(self.lang.press_enter)
                Terminal.__createdisk__(self)
                break
            print(self.lang.available_disks)
            table = PrettyTable([self.lang.disks])
            for i in path:
                check = True
                for w in self.word_system:
                    if w == i:
                        check = False
                        break
                if check:
                    table.add_row([i])
            print(table)
            print(self.lang.enter_name_disk_on_connect)
            cmd = input('{}@{}:~$ '.format(self.user, self.group))
            if cmd == '' or cmd == ' ' or cmd == self.word_system[0]:
                continue
            check = False
            for i in path:
                if i == cmd:
                    check = True
                    break
            if check:
                cls()
                print(self.lang.connecting_disk.format(cmd))
                sleep(self.timer)
                sleep(self.timer)
                print(self.lang.connect_successfully)
                self.path = cmd
                print(self.lang.press_enter)
                break
            else:
                cls()
                print(self.lang.disk_name_not_exists.format(cmd))
                input(self.lang.press_enter)


    def run(self):
        sleep(self.timer)
        cls()
        from Terminal.libs.colorama import Fore
        while 1:
            cmd = input(Fore.LIGHTGREEN_EX + '{}@{}: \{} ~$ '.format(self.user, self.group, self.path) + Fore.WHITE)
            cls()
            Terminal.parser(self, cmd)


    def parser(self, cmd):
        if cmd == 'q':
            exit()
        elif cmd == '':
            pass
        elif cmd.strip() == 'help':
            Terminal.printHelp(self)
        elif cmd.strip() == 'cd':
            print('[Help]: cd {path}')
        elif cmd.strip() == 'apt':
            Terminal.printHelp_Apt(self)
        elif cmd.strip() == 'ls':
            path = os.path.join(self.sys_path, self.path)
            x = os.listdir(path)
            if x == []:
                print(self.lang.list_empty)
            else:
                print(self.lang.list_folders)
                for i in x:
                    if os.path.isdir(os.path.join(path, i)):
                        print('/' + i)
                print(self.lang.list_files)
                for i in x:
                    if os.path.isfile(os.path.join(path, i)):
                        print(i)
        elif cmd.strip() == 'mkdir':
            print(self.lang.folder_creation)
        else:
            if cmd.count(' ') > 0:
                if cmd.strip() == '':
                    pass
                else:
                    cmd = cmd.split()
                    for case in switch(cmd[0]):
                        if case('cd'):
                            if (cmd[1] == '\\' or cmd[1] == '/' or
                                cmd[1] == '.' or cmd[1] == '<' or cmd[1] == '>'):
                                continue
                            if cmd[1] == '..':
                                if self.path.count('\\') == 1:
                                    self.path = self.path.split('\\')[0]
                                elif self.path.count('\\') == 0:
                                    self.path = self.path
                                else:
                                    c = self.path.split('\\')
                                    self.path = ''
                                    for i in range(0, len(c)-1):
                                        self.path += c[i] + '\\'
                                    self.path = self.path[:len(self.path)-1]
                            else:
                                p = os.path.join(self.sys_path, self.path, cmd[1])
                                if os.path.exists(p):
                                    if os.path.isdir(p):
                                        self.path = os.path.join(self.path, cmd[1])
                                    else:
                                        print(self.lang.dir_not_exists)
                                else:
                                    print(self.lang.dir_not_exists)
                        elif case('mkdir'):
                            for i in range(1, len(cmd)):
                                if cmd[i] == self.word_system:
                                    print(self.lang.word_rez_system.format(cmd[i]))
                                else:
                                    if cmd[i].strip() == '':
                                        continue
                                    path = os.path.join(self.sys_path, self.path, cmd[i])
                                    if os.path.exists(path):
                                        if os.path.isdir(path):
                                            print(self.lang.dir_exists.format(cmd[i]))
                                            continue
                                    os.mkdir(path)
                                    print(self.lang.dir_created.format(cmd[i]))
                        elif case('apt'):
                            for cas in switch(cmd[1]):
                                if cas('list'):
                                    print(self.lang.list_plugins)
                                    for p in plugin.Plugins:
                                        print(p.Name)
                                elif cas('install'):
                                    if len(cmd) == 2:
                                        print('apt install {name}')
                                        continue
                                    c = False
                                    for i in cmd[2]:
                                        if i == '.':
                                            print('Используется запрещенный символ (\".\")')
                                            c = True
                                            break
                                    if c:
                                        continue
                                    path = os.path.join(self.sys_path, self.path, '{}.py'.format(cmd[2]))
                                    if os.path.exists(path):
                                        from shutil import copy2
                                        copy2(path, os.path.join(self.sys_path, 'system', 'plugins', '{}.py'.format(cmd[2])))
                                        print(self.lang.plugin_install_ok)
                                    else:
                                        print(self.lang.file_not_exists)
                                elif cas('create'):
                                    if len(cmd) == 2:
                                        print('apt create {name}')
                                        continue
                                    if (cmd[2] == '\\' or cmd[2] == '/' or
                                        cmd[2] == '.' or cmd[2] == '<' or cmd[2] == '>' or cmd[2][0] == '.' or
                                        cmd[2].strip() == '' or cmd[2] == '1' or cmd[2][0] == '2' or
                                        cmd[2][0] == '3' or cmd[2][0] == '4' or cmd[2][0] == '5' or cmd[2][0] == '6' or
                                        cmd[2][0] == '7' or cmd[2][0] == '8' or cmd[2][0] == '9' or cmd[2][0] == '0'):
                                        print(self.lang.name_exists_numbers)
                                        continue
                                    if os.path.exists(os.path.join(self.sys_path, 'system', 'plugins', '{}.py'.format(cmd[2]))):
                                        print(self.lang.plugin_exists)
                                    else:
                                        f = open(os.path.join(self.sys_path, self.path, '{}.py'.format(cmd[2])), 'w')
                                        string = '#Created by TerminalSimulator\n' \
                                                 'from Terminal.core.plugin import Plugin\n\n\n' \
                                                 'class {}(Plugin):\n' \
                                                 '\tName = \'{}\'\n\n' \
                                                 '\tdef OnLoad(self):\n' \
                                                 '\t\tprint(\'{} Loaded!\')\n\n' \
                                                 '\tdef OnCommand(self, cmd, args):\n' \
                                                 '\t\tif cmd == \'command_name\':\n\t\t\treturn True\n' \
                                                 '\t\telse:\n\t\t\treturn False'.format(cmd[2], cmd[2], cmd[2])
                                        f.write(string)
                                        f.close()
                                        print(self.lang.project_created)
                                elif cas('delete'):
                                    if len(cmd) == 2:
                                        print('delete {name}')
                                        continue
                                    path = os.path.join(self.sys_path, 'system', 'plugins', '{}.py'.format(cmd[2]))
                                    if os.path.exists(path):
                                        os.remove(path)
                                        print(self.lang.plugin_delete)
                                    else:
                                        print(self.lang.plugin_not_exists)

                                else:
                                    Terminal.printHelp_Apt(self)
                        else:
                            l = False
                            for p in plugin.Plugins:
                                l = p.OnCommand(cmd[0], cmd[1:])
                            if l == False:
                                print(self.lang.command_not_exist)
            else:
                s = cmd.split(' ')
                l = False
                for p in plugin.Plugins:
                    l = p.OnCommand(s[0], s[1:])
                if l == False:
                    print(self.lang.command_not_exist)


    def printHelp(self):
        for i in self.lang.print_help:
            print(i)


    def printHelp_Apt(self):
        for i in self.lang.print_apt:
            print(i)


    def getWarnings(self):
        for i in self.warning:
            log(i)
        self.warning.clear()


    def getData(self, string):
        list_data = {
            "auth": self.authorization,
            "group": self.group,
            "path": self.path
        }
        try:
            mult = list_data[string]
            return mult
        except KeyError as e:
            log('Undefined unit: {}'.format(e.args[0]))
            return False


class switch(object):
    def __init__(self, value):
        self.value = value  # значение, которое будем искать
        self.fall = False   # для пустых case блоков

    def __iter__(self):     # для использования в цикле for
        """ Возвращает один раз метод match и завершается """
        yield self.match
        raise StopIteration

    def match(self, *args):
        """ Указывает, нужно ли заходить в тестовый вариант """
        if self.fall or not args:
            # пустой список аргументов означает последний блок case
            # fall означает, что ранее сработало условие и нужно заходить
            #   в каждый case до первого break
            return True
        elif self.value in args:
            self.fall = True
            return True
        return False
