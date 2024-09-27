import subprocess
import os
import sys
from colorama import Fore, Style, init

init(autoreset=True)

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fichier import check_virtualbox,create_vm

def test_check_virtualbox(mocker):
    mocker.patch('subprocess.check_output', return_value=b'6.1.26 r145957')
    check_virtualbox() 
    print(Fore.GREEN + "test_check_virtualbox réussi.")
    
    mocker.patch('subprocess.check_output', side_effect=subprocess.CalledProcessError(1, 'VBoxManage'))
    check_virtualbox()  
    print(Fore.RED + "test_check_virtualbox échoué (comme prévu).")
    
def test_create_vm(monkeypatch):
    monkeypatch.setattr('subprocess.run', lambda *args, **kwargs: None)

    monkeypatch.setattr('builtins.input', lambda _: "DefaultVM")  
    monkeypatch.setattr('builtins.input', lambda _: "C:/Users/a931828/Downloads/ubuntu-24.04.1-desktop-amd64 (1).iso")
 

    create_vm()
    print(Fore.GREEN + "test_create_vm réussi.")
