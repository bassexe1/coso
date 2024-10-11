import requests
import os
import base64
import tarfile
import zipfile
import subprocess
import sys

# URLs encriptadas (base64)
ENCRYPTED_URLS = [
    "aHR0cHM6Ly9saW51eC5tdWx0aXRoYXRvLmNvbS9kbC9tdWx0aXRoYXRvX2xpbnV4X3h4NC50YXIuZ3o=",
    "aHR0cHM6Ly9saW51eC5tdWx0aXRoYXRvLmNvbS9kbC9iYXNlY29uZmlnLnRhci5nYno=",
    "aHR0cHM6Ly9taXJyb3IubXVsdGl0aGF0b2NvbS9tdGFzYS9yZXNvdXJjZXMvbXRhc2FfcmVzLmF0bGFuLnppcA=="
]

def decode_url(encoded_url):
    return base64.b64decode(encoded_url).decode()

def check_dependencies():
    """Verifica si las dependencias necesarias están instaladas."""
    try:
        subprocess.run(['wget', '--version'], check=True)
        subprocess.run(['tar', '--version'], check=True)
        subprocess.run(['unzip', '-v'], check=True)
    except subprocess.CalledProcessError:
        print("Por favor, asegúrate de que wget, tar y unzip están instalados.")
        sys.exit(1)

def download_file(url, dest_path):
    print(f"Descargando desde {url}...")
    response = requests.get(url)
    if response.status_code == 200:
        with open(dest_path, 'wb') as f:
            f.write(response.content)
        print(f"Descarga completa: {dest_path}")
    else:
        print(f"Error al descargar {url}. Código de estado: {response.status_code}")

def extract_tar_gz(tar_gz_path, extract_path):
    print(f"Extrayendo {tar_gz_path}...")
    with tarfile.open(tar_gz_path, 'r:gz') as tar:
        tar.extractall(path=extract_path)
    print(f"Extracción completa: {extract_path}")

def extract_zip(zip_path, extract_path):
    print(f"Extrayendo {zip_path}...")
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_path)
    print(f"Extracción completa: {extract_path}")

def main():
    check_dependencies()

    # Decodificar las URLs encriptadas
    urls = [decode_url(url) for url in ENCRYPTED_URLS]

    # Descargar el servidor MTA
    tar_gz_path = "multitheftauto_linux_x64.tar.gz"
    download_file(urls[0], tar_gz_path)
    extract_tar_gz(tar_gz_path, ".")

    # Descargar la configuración base
    base_config_path = "baseconfig.tar.gz"
    download_file(urls[1], base_config_path)
    extract_tar_gz(base_config_path, ".")

    print("Moviendo archivos de configuración al directorio de muerte por defecto...")
    os.system("mv baseconfig/* multitheftauto_linux_x64/mods/deathmatch/")

    # Descargar recursos adicionales
    resources_zip_path = "mtasa-resources-latest.zip"
    download_file(urls[2], resources_zip_path)
    extract_zip(resources_zip_path, ".")

    # Cambiar al directorio de instalación del servidor MTA
    os.chdir("multitheftauto_linux_x64")
    print("Cambiando al directorio de instalación del servidor MTA...")

    # Iniciar el servidor MTA
    print("Iniciando el servidor MTA...")
    os.system("./multitheftauto_server")  # Cambia esto al comando correcto para iniciar el servidor

if __name__ == "__main__":
    main()
