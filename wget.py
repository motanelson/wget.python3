
import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
print("\033c\033[43;30m\n")
def mini_wget(url):
    # 1. Fazer download da página
    resp = requests.get(url)
    resp.raise_for_status()
    html = resp.text

    # 2. Carregar no BeautifulSoup
    soup = BeautifulSoup(html, "html.parser")

    # 3. Procurar todas as imagens
    for img in soup.find_all("img"):
        src = img.get("src")
        if not src:
            continue

        # 4. Resolver URL completa da imagem
        img_url = urljoin(url, src)

        # 5. Extrair apenas o nome do ficheiro
        filename = os.path.basename(urlparse(img_url).path)
        if not filename:  # caso a URL termine com "/"
            continue

        # 6. Fazer download da imagem
        try:
            r = requests.get(img_url, stream=True)
            r.raise_for_status()
            with open(filename, "wb") as f:
                for chunk in r.iter_content(8192):
                    f.write(chunk)
            print(f"[OK] {filename}")
        except Exception as e:
            print(f"[ERRO] {img_url} -> {e}")
            continue

        # 7. Alterar o src da imagem para o ficheiro local
        img["src"] = filename

    # 8. Reconstruir HTML
    new_html = str(soup)

    # 9. Gravar como index.html
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(new_html)

    print("Página gravada como index.html")

# Exemplo de uso:
print("url?")
urls=input()
mini_wget(urls)
