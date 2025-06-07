from bs4 import BeautifulSoup
import requests
import csv
import unicodedata
import re


def ejecutar_scraping(url: str):
    try:
        print("[INFO] Iniciando navegador y cargando página...")

        response = requests.get(url, timeout=5)
        response.raise_for_status()
        html = response.text
        print("[INFO] Página cargada y navegador cerrado.")

    except requests.exceptions.RequestException as e:
        return {"error": f"No se pudo cargar la página: {e}"}


    soup = BeautifulSoup(html, "html.parser")
   
    print("[INFO] Contenido principal encontrado.")

    
    # ====================
    # EXTRAER PÁRRAFOS HASTA REFERENCES
    # ====================
    # ====================
    # EXTRAER PÁRRAFOS HASTA REFERENCES
    # ====================
    paragraphs = []
    print("[INFO] Comenzando análisis de elementos en mw-parser-output...")

    for frases in soup.find_all("p"):
        if frases.find_parent("table", class_=["infobox", "sidebar"]):
            continue
        if frases.name == "h2":
            span = frases.find("span", class_="mw-headline")
            if span and span.get("id") == "References":
                print("[INFO] Se llegó a la sección 'References'. Detener extracción.")
                break

        for tag in frases.find_all(["sup"]):
            tag.decompose()  # eliminamos solo referencias

        for tag in frases.find_all(["a", "span"]):
            tag.insert_before(" ")
            tag.insert_after(" ")
            tag.unwrap()
        # Obtener texto limpio
        text = frases.get_text(" ", strip=True)

        # Eliminar caracteres no ASCII (coreano, símbolos raros, IPA)
        text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")

        # Normalizar múltiples espacios a uno
        clean = re.sub(r"\s+", " ", text).strip()

        if clean:
            clean = re.sub(r"\s+", " ", clean)
            paragraphs.append(clean)
            print(f"[DEBUG] Párrafo agregado: {clean[:60]}...")



    print(f"[INFO] Total párrafos extraídos: {len(paragraphs)}")


    # ====================
    # EXTRAER INFOBOX
    # ====================
    infobox_data = {}
    infobox = soup.find("table", class_="infobox")
    if infobox:
        print("[INFO] Extrayendo infobox...")
        for row in infobox.find_all("tr"):
            th = row.find("th")
            td = row.find("td")
            if th and td:
                for tag in td.find_all(["span", "sup", "a"]):
                    tag.unwrap()
                key = th.get_text(strip=True)
                value = td.get_text(" ", strip=True)
                infobox_data[key] = re.sub(r"\s+", " ", value)

    print(f"[INFO] Total elementos infobox: {len(infobox_data)}")

    # ====================
    # EXTRAER SIDEBAR
    # ====================
    sidebar_data = []
    sidebars = soup.find_all("table", class_="sidebar")
    print(f"[INFO] Tablas sidebar encontradas: {len(sidebars)}")

    for sidebar in sidebars:
        heading = ""
        for row in sidebar.find_all("tr"):
            th = row.find("th", class_="sidebar-heading")
            td = row.find("td", class_="sidebar-content")
            if th:
                heading = th.get_text(strip=True)
            if td:
                for tag in td.find_all(["span", "sup", "a"]):
                    tag.unwrap()
                value = td.get_text(" ", strip=True)
                sidebar_data.append((heading, re.sub(r"\s+", " ", value)))

    print(f"[INFO] Filas extraídas de sidebar: {len(sidebar_data)}")

    # ====================
    # GUARDAR EN CSV
    # ====================
   # with open("wikipedia_scrape_output.csv", "w", newline='', encoding='utf-8') as file:
    #    writer = csv.writer(file)

     #   for k, v in infobox_data.items():
      #      writer.writerow([f"[Infobox] {k}", v])

       # for heading, value in sidebar_data:
        #    writer.writerow([f"[Sidebar] {heading}", value])

        #for p in paragraphs:
         #   writer.writerow(["Contenido", p]) ##

    return {"mensaje": "Scraping completado con éxito",
            "contenido": paragraphs
            }
    





