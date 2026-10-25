import pdfplumber
import re
from src.config import DATA_DIR, STOP_WORDS
# Eliminamos la importación de Counter para hacerlo de forma manual

def extraerTextoPdf(rutaPdf):
    textoCompleto = ""
    try:
        # Abrimos el archivo
        with pdfplumber.open(rutaPdf) as pdf:
            # Recorremos cada página una por una
            for pagina in pdf.pages:
                texto = pagina.extract_text()
                # Si la página tiene texto, lo pegamos al total
                if texto:
                    textoCompleto = textoCompleto + texto + "\n"
        return textoCompleto
    except Exception as error:
        print(f"Error al leer el archivo {rutaPdf}: {error}")
        return None

def aislarAbstract(textoCompleto):
    # Validamos que sí haya texto
    if not textoCompleto:
        return None
        
    # Patrón para buscar la palabra Abstract y detenerse en Introduction o Keywords
    patron = r"(?:a\s*b\s*s\s*t\s*r\s*a\s*c\s*t|abstract)\s*(.*?)(?:\n\s*1\.?\s*introduction|\n\s*introduction)"
    
    # Ejecutamos la búsqueda ignorando mayúsculas
    coincidencia = re.search(patron, textoCompleto, re.DOTALL | re.IGNORECASE)
    
    if coincidencia:
        # Extraemos solo el fragmento encontrado y le quitamos los espacios de los bordes
        texto = coincidencia.group(1).strip()
        # Por seguridad, borramos la palabra keywords si se coló al final
        texto = re.sub(r'(?i)keywords:?', '', texto)
        return texto
    else:
        return "No se pudo aislar el Abstract con la regla actual."
        
def limpiarTexto(texto):
    if not texto:
        return []
        
    # 1. Todo a minúsculas
    textoMinusculas = texto.lower()
    
    # 2. Borrar números y signos de puntuación (dejamos solo letras y espacios)
    textoLimpio = re.sub(r'[^a-z\s]', '', textoMinusculas)
    
    # 3. Separar el párrafo en una lista de palabras individuales
    palabras = textoLimpio.split()
    
    # 4. Filtrar las stop words con un ciclo normal
    palabrasValidas = []
    for palabra in palabras:
        if palabra not in STOP_WORDS and len(palabra) > 2:
            palabrasValidas.append(palabra)
            
    return palabrasValidas

def contarFrecuencias(listaPalabras):
    # Creamos un diccionario vacío
    frecuencias = {}
    
    # Recorremos la lista gigante de palabras
    for palabra in listaPalabras:
        # Si la palabra ya existe en el diccionario, le sumamos 1 a su conteo
        if palabra in frecuencias:
            frecuencias[palabra] = frecuencias[palabra] + 1
        # Si es la primera vez que la vemos, la guardamos con un conteo de 1
        else:
            frecuencias[palabra] = 1
            
    return frecuencias