import time
from src.config import DATA_DIR
from src.extractor import extraerTextoPdf, aislarAbstract, limpiarTexto, contarFrecuencias
from src.sorting import countingSort, radixSort, bucketSort


def main():
    print("Iniciando extracción de datos...\n")
    todasLasPalabras = []
    pdfsFallidos = []  # para reportar cobertura al final

    # 1. Iterar dinámicamente sobre todos los archivos PDF
    archivosPdf = list(DATA_DIR.glob("*.pdf"))

    for rutaPdf in archivosPdf:
        print(f"Procesando: {rutaPdf.name}")
        textoCrudo = extraerTextoPdf(rutaPdf)
        abstract = aislarAbstract(textoCrudo)

        if abstract and not abstract.startswith("No se pudo"):
            todasLasPalabras.extend(limpiarTexto(abstract))
        else:
            print(f"  -> [ADVERTENCIA] No se pudo extraer el abstract de: {rutaPdf.name}")
            pdfsFallidos.append(rutaPdf.name)

    # 2. Generar el diccionario de frecuencias
    frecuencias = contarFrecuencias(todasLasPalabras)
    print("\n" + "-" * 50)
    print(f"PDFs procesados:       {len(archivosPdf)}")
    print(f"PDFs con abstract OK:  {len(archivosPdf) - len(pdfsFallidos)}")
    print(f"PDFs fallidos:         {len(pdfsFallidos)}")
    print(f"Total términos únicos: {len(frecuencias)}")
    print("-" * 50)

    if pdfsFallidos:
        print("\nArchivos sin abstract extraído (revisar formato/OCR):")
        for nombre in pdfsFallidos:
            print(f"  - {nombre}")
        print()

    # --- MEDICIÓN EMPÍRICA EN MILISEGUNDOS ---

    start = time.perf_counter()
    terminosCounting = countingSort(frecuencias.copy())
    tiempoCounting = (time.perf_counter() - start) * 1000

    start = time.perf_counter()
    terminosRadix = radixSort(frecuencias.copy())
    tiempoRadix = (time.perf_counter() - start) * 1000

    start = time.perf_counter()
    terminosBucket = bucketSort(frecuencias.copy())
    tiempoBucket = (time.perf_counter() - start) * 1000

    # --- REPORTE DE TIEMPOS ---
    print("-" * 50)
    print("=== TIEMPOS DE EJECUCIÓN (Milisegundos) ===")
    print(f"Counting Sort: {tiempoCounting:.4f} ms")
    print(f"Radix Sort:    {tiempoRadix:.4f} ms")
    print(f"Bucket Sort:   {tiempoBucket:.4f} ms")
    print("-" * 50)

    # --- TOP 15 POR ALGORITMO ---
    top15Counting = terminosCounting[:15]
    top15Radix    = terminosRadix[:15]
    top15Bucket   = terminosBucket[:15]

    # --- TABLA COMPARATIVA (ancho dinámico) ---
    filas = []
    for i in range(15):
        c = top15Counting[i] if i < len(top15Counting) else ("—", 0)
        r = top15Radix[i]    if i < len(top15Radix)    else ("—", 0)
        b = top15Bucket[i]   if i < len(top15Bucket)   else ("—", 0)
        filas.append((
            str(i + 1),
            f"{c[0]} ({c[1]})",
            f"{r[0]} ({r[1]})",
            f"{b[0]} ({b[1]})",
        ))

    encabezado = ("#", "Counting Sort", "Radix Sort", "Bucket Sort")
    anchos = [
        max(len(encabezado[j]), *(len(f[j]) for f in filas)) + 2
        for j in range(4)
    ]

    linea = "+" + "+".join("-" * a for a in anchos) + "+"
    fmt   = "|" + "|".join(f" {{:<{a - 1}}}" for a in anchos) + "|"

    titulo = "TOP 15 TÉRMINOS MÁS FRECUENTES — COMPARACIÓN DE ALGORITMOS"
    anchoTotal = sum(anchos) + 5

    print("\n" + "=" * anchoTotal)
    print(titulo)
    print("=" * anchoTotal)
    print(linea)
    print(fmt.format(*encabezado))
    print(linea)
    for fila in filas:
        print(fmt.format(*fila))
    print(linea)

if __name__ == "__main__":
    main()