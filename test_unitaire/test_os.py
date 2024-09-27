from colorama import Fore, Style, init
import os
import sys

init(autoreset=True)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from fichier import detect_os

def test_detect_os(mocker):
    mocker.patch('platform.system', return_value='Windows')
    os_type = detect_os()
    assert os_type == 'Windows'
    print(Fore.GREEN + "test_detect_os réussi.")