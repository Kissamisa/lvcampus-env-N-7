import subprocess
from colorama import Fore, Style, init

init(autoreset=True)

from fichier import check_docker,create_container

def test_check_docker(mocker):
    mocker.patch('subprocess.check_output', return_value=b'Docker version 20.10.8')
    check_docker()
    print(Fore.GREEN + "test_check_docker réussi.")
    
    mocker.patch('subprocess.check_output', side_effect=subprocess.CalledProcessError(1, 'docker'))
    check_docker()
    print(Fore.RED + "test_check_docker échoué (comme prévu).")
    
def test_create_container(monkeypatch):
    class FakeCompletedProcess:
        def __init__(self):
            self.stdout = b"fake_container_id"
    

    monkeypatch.setattr('subprocess.run', lambda *args, **kwargs: FakeCompletedProcess())
    

    inputs = iter(["ubuntu", "non"]) 
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))


    create_container()

  
    print("test_create_container réussi.")