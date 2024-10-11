import requests
import os
import base64
import tarfile
import zipfile

# Función para decodificar la URL encriptada
def decode_url(encoded_url):
    return base64.b64decode(encoded_url).decode()

# Función para descargar un archivo
def download_file(url, dest_path):
    print(f"Descargando desde {url}...")
    response = requests.get(url)

    if response.status_code == 200:
        with open(dest_path, 'wb') as f:
            f.write(response.content)
        print(f"Descarga completa: {dest_path}")
    else:
        print(f"Error al descargar {url}. Código de estado: {response.status_code}")

# Función para extraer un archivo tar.gz
def extract_tar_gz(tar_gz_path, extract_path):
    print(f"Extrayendo {tar_gz_path}...")
    with tarfile.open(tar_gz_path, 'r:gz') as tar:
        tar.extractall(path=extract_path)
    print(f"Extracción completa: {extract_path}")

# Función para extraer un archivo zip
def extract_zip(zip_path, extract_path):
    print(f"Extrayendo {zip_path}...")
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_path)
    print(f"Extracción completa: {extract_path}")

# Función principal para instalar y ejecutar el servidor
def main():
    # Leer las URLs desde el archivo de configuración
    with open('config.txt', 'r') as file:
        urls = [decode_url(line.strip()) for line in file.readlines()]

    # Descargar el servidor MTA
    tar_gz_path = "multitheftauto_linux_x64.tar.gz"
    download_file(urls[0], tar_gz_path)
    
    # Extraer el servidor MTA
    extract_tar_gz(tar_gz_path, ".")

    # Descargar la configuración base
    base_config_path = "baseconfig.tar.gz"
    download_file(urls[1], base_config_path)

    # Extraer la configuración base
    extract_tar_gz(base_config_path, ".")

    # Mover la configuración extraída al directorio correcto
    print("Moviendo archivos de configuración al directorio de muerte por defecto...")
    os.system("mv baseconfig/* multitheftauto_linux_x64/mods/deathmatch/")
    
    # Descargar recursos adicionales
    resources_zip_path = "mtasa-resources-latest.zip"
    download_file(urls[2], resources_zip_path)

    # Extraer recursos adicionales
    extract_zip(resources_zip_path, ".")

    # Cambiar al directorio de instalación del servidor MTA
    os.chdir("multitheftauto_linux_x64")
    print("Cambiando al directorio de instalación del servidor MTA...")

    # Iniciar el servidor MTA
    print("Iniciando el servidor MTA...")
    os.system("./multitheftauto_server")  # Cambia esto al comando correcto para iniciar el servidor

if __name__ == "__main__":
    main()
