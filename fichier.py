import platform
import subprocess

def detect_os():
    os_type = platform.system()
    print(f"Le système d'exploitation détecté est : {os_type}")
    return os_type

def check_virtualbox():
    try:
        version = subprocess.check_output(["VBoxManage", "--version"]).decode("utf-8").strip()
        print(f"VirtualBox est installé. Version : {version}")
    except subprocess.CalledProcessError:
        print("VirtualBox n'est pas installé. Téléchargez-le ici: https://www.virtualbox.org/wiki/Downloads")

def check_docker():
    try:
        version = subprocess.check_output(["docker", "--version"]).decode("utf-8").strip()
        print(f"Docker est installé. Version : {version}")
    except subprocess.CalledProcessError:
        print("Docker n'est pas installé. Téléchargez-le ici: https://desktop.docker.com/win/stable/Docker%20Desktop%20Installer.exe")

def create_vm():
    vm_name = input("Entrez le nom de la VM : ")
    iso_path = input("Entrez le chemin de l'ISO Linux : ")

    try:
        subprocess.run(["VBoxManage", "createvm", "--name", vm_name, "--register"], check=True)
        subprocess.run(["VBoxManage", "modifyvm", vm_name, "--cpus", "2"], check=True)
        subprocess.run(["VBoxManage", "createhd", "--filename", f"{vm_name}.vdi", "--size", "10240"], check=True)  # 10 Go
        subprocess.run(["VBoxManage", "storagectl", vm_name, "--name", "SATA Controller", "--add", "sata"], check=True)
        subprocess.run(["VBoxManage", "storageattach", vm_name, "--storagectl", "SATA Controller", "--port", "0", "--device", "0", "--type", "hdd", "--medium", f"{vm_name}.vdi"], check=True)
        subprocess.run(["VBoxManage", "storageattach", vm_name, "--storagectl", "SATA Controller", "--port", "1", "--device", "0", "--type", "dvddrive", "--medium", iso_path], check=True)

        print(f"La VM '{vm_name}' a été créée avec succès avec 2 CPUs et l'ISO {iso_path} attaché.")
    except subprocess.CalledProcessError as e:
        print(f"Erreur lors de la création de la VM : {e}")

def create_container():
    container_type = input("Quel type de conteneur voulez-vous créer (Ubuntu, Debian, RockyLinux, Fedora, Python, MariaDB) ? ").strip().lower()
    
    images = {
        "ubuntu": "ubuntu:latest",
        "debian": "debian:latest",
        "rockylinux": "rockylinux:latest",
        "fedora": "fedora:latest",
        "python": "python:latest",
        "mariadb": "mariadb:latest"
    }
    
    if container_type not in images:
        print("Type de conteneur non reconnu.")
        return
    
    volume_choice = input("Voulez-vous attacher un volume persistant ? (oui/non) : ").strip().lower()
    volume_option = ""
    
    if volume_choice == "oui":
        volume_path = input("Entrez le chemin du volume à attacher : ")
        volume_option = f"-v {volume_path}:{volume_path}"

    try:
        result = subprocess.run(f"docker run -dit {volume_option} {images[container_type]}", shell=True, check=True, capture_output=True)
        container_id = result.stdout.decode().strip()
        print(f"Conteneur {container_type} créé avec succès. ID du conteneur : {container_id}")

        status_result = subprocess.run(f"docker ps -a --filter id={container_id}", shell=True, check=True, capture_output=True)
        print(f"Statut du conteneur : {status_result.stdout.decode().strip()}")

        logs_result = subprocess.run(f"docker logs {container_id}", shell=True, check=True, capture_output=True)
        print(f"Logs du conteneur :\n{logs_result.stdout.decode()}")

    except subprocess.CalledProcessError as e:
        print(f"Erreur lors de la création du conteneur : {e}")
        
def menu():
    choice = input("Voulez-vous créer une VM (1) ou un conteneur Docker (2)? ")
    if choice == '1':
        create_vm()
    elif choice == '2':
        create_container()
    else:
        print("Choix non valide. Veuillez entrer 1 ou 2.")

if __name__ == "__main__":
    detect_os()
    check_virtualbox()
    check_docker()
    menu()
