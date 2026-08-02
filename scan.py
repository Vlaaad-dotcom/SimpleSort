import plistlib
import pathlib
import logging
import subprocess
import sys
from subprocess import SubprocessError, CalledProcessError

home = pathlib.Path.home()
plist_path = home / "Library/LaunchAgents" / "com.vlad.simplesort.plist"

def create_process():
    data = {
        'Label': 'com.vlad.simplesort',
        'ProgramArguments': [
            f'{home}/PycharmProjects/SimpleSort/.venv/bin/python',
            f'{home}/PycharmProjects/SimpleSort/main.py'
        ],
        'WatchPaths': [
            f'{home}/Downloads'
        ],
        'StandardOutPath': f'{home}/Library/Logs/SimpleSort.log',
        'StandardErrorPath':f'{home}/Library/Logs/SimpleSort.err',
        'RunAtLoad': True,
        'ThrottleInterval': 30,

    }

    log_dir = home / "Library" / "Logs"
    try:
        log_dir.mkdir(parents=True, exist_ok=True)
    except PermissionError:
        raise
    logging.basicConfig(
        level=logging.INFO,
        filename=f'{home}/Library/Logs/SimpleSort.log',
        format='%(asctime)s - %(levelname)s - %(message)s',
    )
    try:
        with open(plist_path, 'wb') as f:
            plistlib.dump(data, f, fmt=plistlib.FMT_XML)
    except PermissionError:
        logging.critical('Не могу загрузить логику в процесс')
        sys.exit(1)

def log():
    if plist_path.is_file():
        logging.info(f'Plist создан: {plist_path}')
        print(f'Plist создан: {plist_path}')
    else:
        raise FileNotFoundError(f"Plist не найден: {plist_path}")
    result = subprocess.run(["launchctl", "load", str(plist_path)]
    ,capture_output=True,text=True)
    if result.returncode != 0:
        raise SubprocessError(f"Процесс загрузки слежения не запустился:{result.stderr}")
    if result.returncode == 0:
        logging.info('Plist загружен успешно')
        print('Plist загружен успешно')
        logging.info('Агент запущен')
        print('Агент запущен')

def runtime():
    try:
        subprocess.run(["launchctl", "unload", str(plist_path)],
                       stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL, check=True)
        subprocess.run(["launchctl", "load", str(plist_path)],capture_output=True,text=True,check=True)
        subprocess.run(["launchctl", "start", "com.vlad.simplesort"],capture_output=True,text=True,check=True)
    except CalledProcessError as e:
        logging.critical(f"Не могу работать с процессами:{e.stderr}")
        sys.exit(1)
create_process()
log()
runtime()