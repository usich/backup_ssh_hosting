import logging
import threading
import os
import pysftp
from config import zoo, vet_365
import datetime



class BackUp(threading.Thread):
    def __init__(self, host, port, path_local_rem, user, password, path_host, path_local, site_name):
        super().__init__()
        self.host = host
        self.port = port
        self.path_local_rem = path_local_rem
        self.user = user
        self.password = password
        self.path_host = path_host
        self.path_local = path_local
        self.error = False
        self.site_name = site_name


    def run(self):

        cnopts = pysftp.CnOpts()
        cnopts.hostkeys = None
        with pysftp.Connection(host=self.host, port=self.port, username=self.user, password=self.password,
                               cnopts=cnopts) as sftp:
            try:
                # sftp.cwd('/var/www/u0521190/data/www/bagira-vet.club/bitrix/backup')
                # directory_structure = sftp.listdir_attr()

                with sftp.cd(self.path_host):
                    pass
                os.system(fr'cd /d {self.path_local_rem}')
                os.system(fr'rmdir /s /q {self.path_local_rem}')
                os.system(fr'mkdir {self.path_local_rem}')

                sftp.get_d(self.path_host, self.path_local)
                sftp.execute('rm -rf ' + self.path_host)
            except Exception as ex:
                print(f'{ex}: {self.site_name}')

threadLock = threading.Lock()
thread = []
try:
    thread1 = BackUp(zoo.get('ip'), 22, r'D:\bitrixBackup\zoo', zoo.get('login'), zoo.get('pass'),
                     zoo.get('dir'), 'D://bitrixBackup/zoo', 'bagira-zoo')

    thread2 = BackUp(vet_365.get('ip'), 22, r'D:\bitrixBackup\vet', vet_365.get('login'), vet_365.get('pass'),
                     vet_365.get('dir_vet'), 'D://bitrixBackup/vet', 'bagira-vet')

    thread3 = BackUp(vet_365.get('ip'), 22, r'D:\bitrixBackup\365', vet_365.get('login'), vet_365.get('pass'),
                 vet_365.get('dir_365'), 'D://bitrixBackup/365', 'korm-365')

except OSError:
    print("Соединение прервано.")
except FileNotFoundError as ex:
    print('')

thread1.start()
thread2.start()
thread3.start()

thread.append(thread1)
thread.append(thread2)
thread.append(thread3)

for t in thread:
    t.join()

