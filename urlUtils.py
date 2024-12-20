from urllib.parse import urlparse

def extract_host(url: str) -> str:
    parsed_url = urlparse(url)
    return parsed_url.netloc  # Renvoie le host (nom de domaine ou IP avec port)
