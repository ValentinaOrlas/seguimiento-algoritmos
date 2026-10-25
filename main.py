import time
from src.config import DATA_DIR
from src.extractor import extraerTextoPdf, aislarAbstract, limpiarTexto, contarFrecuencias
from src.sorting import countingSort, radixSort, bucketSort

def main():
    print("Iniciando extracción de datos...\n")
    todasLasPalabras = []
    
    # 1. Iterar dinámicamente sobre todos los archivos PDF
    archivosPdf = list(DATA_DIR.glob("*.pdf"))

    for rutaPdf in archivosPdf:
        # ¡ESTA ES LA LÍNEA NUEVA! Para que veas que sí está avanzando
        print(f"Procesando: {rutaPdf.name}") 
        
        textoCrudo = extraerTextoPdf(rutaPdf)
        abstract = aislarAbstract(textoCrudo)
        
        # Validamos que se haya extraído correctamente
        if abstract and not abstract.startswith("No se pudo"):
            todasLasPalabras.extend(limpiarTexto(abstract))
        else:
            print(f"  -> [ADVERTENCIA] No se pudo extraer el abstract de: {rutaPdf.name}")
    
    # 2. Generar el diccionario de frecuencias
    frecuencias = contarFrecuencias(todasLasPalabras)
    print("\n" + "-" * 50)
    print(f"Total términos únicos: {len(frecuencias)}")
    print("-" * 50)

    # --- MEDICIÓN EMPÍRICA EN MILISEGUNDOS ---

    # 1. Counting Sort
    start = time.perf_counter()
    terminosCounting = countingSort(frecuencias)
    end = time.perf_counter()
    tiempoCounting = (end - start) * 1000

    # 2. Radix Sort
    start = time.perf_counter()
    terminosRadix = radixSort(frecuencias)
    end = time.perf_counter()
    tiempoRadix = (end - start) * 1000

    # 3. Bucket Sort
    start = time.perf_counter()
    terminosBucket = bucketSort(frecuencias)
    end = time.perf_counter()
    tiempoBucket = (end - start) * 1000

    # --- RESULTADOS FINALES ---
    print("\n=== TIEMPOS DE EJECUCIÓN (Milisegundos) ===")
    print(f"Counting Sort: {tiempoCounting:.4f} ms")
    print(f"Radix Sort:    {tiempoRadix:.4f} ms")
    print(f"Bucket Sort:   {tiempoBucket:.4f} ms")
    print("-" * 50)

    print("\n=== TOP 15 TÉRMINOS ===")
    for palabra, freq in terminosBucket[:15]:
        print(f"{palabra}: {freq}")

if __name__ == "__main__":
    main()