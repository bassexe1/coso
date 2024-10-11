import base64

# Lista de URLs que quieres encriptar
urls = [
    "https://linux.multitheftauto.com/dl/multitheftauto_linux_x64.tar.gz",
    "https://linux.multitheftauto.com/dl/baseconfig.tar.gz",
    "https://mirror.multitheftauto.com/mtasa/resources/mtasa-resources-latest.zip"
]

# Encriptar las URLs
encoded_urls = [base64.b64encode(url.encode()).decode() for url in urls]

# Imprimir las URLs encriptadas
for encoded in encoded_urls:
    print(encoded)
