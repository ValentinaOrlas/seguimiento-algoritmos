import pdfplumber
import re
from src.config import DATA_DIR, STOP_WORDS

def extract_text_from_pdf(pdf_path):
    """
    Abre un PDF y extrae todo su texto página por página.
    """
    full_text = ""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    full_text += text + "\n"
        return full_text
    except Exception as e:
        print(f"Error al leer el archivo {pdf_path}: {e}")
        return None

def get_abstract_only(full_text):
    """
    Aísla el Abstract soportando formatos de doble columna (Elsevier/IEEE).
    Detecta letras espaciadas (A B S T R A C T) y limpia etiquetas de Keywords.
    """
    if not full_text:
        return None
        
    # El patrón busca 'abstract' normal O espaciado (a\s*b\s*s\s*t\s*r\s*a\s*c\s*t).
    # Se detiene al encontrar cualquier variación de "1. Introduction" o "Introduction".
    pattern = r"(?:a\s*b\s*s\s*t\s*r\s*a\s*c\s*t|abstract)\s*(.*?)(?:\n\s*1\.?\s*introduction|\n\s*introduction)"
    
    match = re.search(pattern, full_text, re.DOTALL | re.IGNORECASE)
    
    if match:
        texto = match.group(1).strip()
        # Limpiamos la palabra "Keywords:" y saltos de línea extraños que se hayan colado
        texto = re.sub(r'(?i)keywords:?', '', texto)
        return texto
    else:
        return "No se pudo aislar el Abstract con la regla actual."
        
def clean_text(text):
    """
    Convierte a minúsculas, elimina puntuación y quita stop words.
    """
    if not text:
        return []
        
    # 1. Convertir a minúsculas
    text = text.lower()
    
    # 2. Eliminar todo lo que no sea letras (A-Z) o espacios
    text = re.sub(r'[^a-z\s]', '', text)
    
    # 3. Separar en palabras y filtrar stop words
    words = text.split()
    clean_words = [word for word in words if word not in STOP_WORDS and len(word) > 2]
    
    return clean_words