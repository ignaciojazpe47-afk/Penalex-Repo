import os
import re
import subprocess
import json

def limpiar_html(html_content):
    patron = r"IAJuriss\.com\s\|\sBase\ de\ Datos\ Jurídica\ de\ Venezuela\ \|\ Página\ \d+\ de\ \d+"
    html_limpio = re.sub(patron, "", html_content, flags=re.IGNORECASE)
    return html_limpio

def procesar_archivo(json_file):
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    url = data.get("url_pdf")
    if not url:
        print("No se encontró URL en el JSON.")
        return

    # Descargar el PDF
    pdf_filename = "sentencia.pdf"
    subprocess.run(["wget", "-O", pdf_filename, url])

    # Convertir a HTML
    subprocess.run(["pdftohtml", "-s", "-i", pdf_filename, "salida.html"])

    # Leer y limpiar
    with open("salida.html", 'r', encoding='utf-8') as f:
        contenido = f.read()

    contenido_limpio = limpiar_html(contenido)

    # Guardar resultado en el mismo JSON
    data["contenido_html"] = contenido_limpio
    
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)

    print(f"Archivo {json_file} procesado.")

if __name__ == "__main__":
    procesar_archivo("prueba.json")
