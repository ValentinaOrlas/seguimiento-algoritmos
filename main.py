from src.config import DATA_DIR
from src.extractor import extract_text_from_pdf, get_abstract_only, clean_text

def main():
    pdf_prueba = DATA_DIR / "1. Artificial intelligence literacy in higher and adult education A scoping literature review.pdf"
    
    print(f"--- Procesando: {pdf_prueba.name} ---\n")
    
    texto_crudo = extract_text_from_pdf(pdf_prueba)
    abstract = get_abstract_only(texto_crudo)
    
    print("=== ABSTRACT EXTRAÍDO ===")
    print(abstract[:500] + "...\n" if len(abstract) > 500 else abstract + "\n")
    
    palabras_limpias = clean_text(abstract)
    print(f"=== PALABRAS LIMPIAS (Total: {len(palabras_limpias)}) ===")
    print(palabras_limpias[:20])

if __name__ == "__main__":
    main()