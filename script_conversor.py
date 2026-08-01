import os
import re
import subprocess
import json

def limpiar_html(html_content):
    patron = r"IAJuriss\.com\s\|\sBase\ de\ Datos\ Jurídica\ de\ Venezuela\ \|\ Página\ \d+\ de\ \d+"
    return re.sub(patron, "", html_content, flags=re.IGNORECASE)

def procesar_archivo(json_file):
    if not os.path.exists(json_file):
        print(f"Error: {json_file} no encontrado.")
        return
        
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    url = data.get("url_pdf")
    if not url:
        return

    subprocess.run(["wget", "-O", "temp.pdf", url])
    subprocess.run(["pdftohtml", "-s", "-i", "temp.pdf", "salida.html"])

    with open("salida.html", 'r', encoding='utf-8') as f:
        data["contenido_html"] = limpiar_html(f.read())
    
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)

if __name__ == "__main__":
    # Toma el nombre del archivo desde la variable que le enviamos
    nombre_archivo = os.getenv("ARCHIVO_A_PROCESAR")
    procesar_archivo(nombre_archivo)
