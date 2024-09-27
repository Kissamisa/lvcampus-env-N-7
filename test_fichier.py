import subprocess
import pytest
from colorama import Fore, Style, init

init(autoreset=True)

from fichier import detect_os, check_virtualbox, check_docker, create_vm, create_container

def test_detect_os(mocker):
    mocker.patch('platform.system', return_value='Windows')
    os_type = detect_os()
    assert os_type == 'Windows'
    print(Fore.GREEN + "test_detect_os réussi.")
    
def test_check_virtualbox(mocker):
    mocker.patch('subprocess.check_output', return_value=b'6.1.26 r145957')
    check_virtualbox() 
    print(Fore.GREEN + "test_check_virtualbox réussi.")
    
    mocker.patch('subprocess.check_output', side_effect=subprocess.CalledProcessError(1, 'VBoxManage'))
    check_virtualbox()  
    print(Fore.RED + "test_check_virtualbox échoué (comme prévu).")

def test_check_docker(mocker):
    mocker.patch('subprocess.check_output', return_value=b'Docker version 20.10.8')
    check_docker()
    print(Fore.GREEN + "test_check_docker réussi.")
    
    mocker.patch('subprocess.check_output', side_effect=subprocess.CalledProcessError(1, 'docker'))
    check_docker()
    print(Fore.RED + "test_check_docker échoué (comme prévu).")

def test_create_vm(monkeypatch):
    monkeypatch.setattr('subprocess.run', lambda *args, **kwargs: None)

    monkeypatch.setattr('builtins.input', lambda _: "DefaultVM")  
    monkeypatch.setattr('builtins.input', lambda _: "C:/Users/a931828/Downloads/ubuntu-24.04.1-desktop-amd64 (1).iso")
 

    create_vm()
    print(Fore.GREEN + "test_create_vm réussi.")
    
def test_create_container(monkeypatch):
    class FakeCompletedProcess:
        def __init__(self):
            self.stdout = b"fake_container_id"
    

    monkeypatch.setattr('subprocess.run', lambda *args, **kwargs: FakeCompletedProcess())
    

    inputs = iter(["ubuntu", "non"]) 
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))


    create_container()

  
    print("test_create_container réussi.")



if __name__ == "__main__":
    pytest.main()
 