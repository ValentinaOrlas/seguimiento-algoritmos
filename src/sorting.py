def countingSort(frecuencias):
    
    if len(frecuencias) == 0:
        return []

    frecuenciaMaxima = max(frecuencias.values())
    
    # 1. Preparar los espacios vacíos
    listaConteos = []
    for i in range(frecuenciaMaxima + 1):
        listaConteos.append([])

    # 2. Acomodar cada palabra según las veces que se repite
    for palabra in frecuencias:
        cantidad = frecuencias[palabra]
        listaConteos[cantidad].append(palabra)

    # 3. Extraer los datos ya ordenados de mayor a menor
    palabrasOrdenadas = []
    
    # Recorremos desde el número más grande hasta el cero
    for i in range(frecuenciaMaxima, -1, -1):
        cajonActual = listaConteos[i]
        
        # Si el cajón tiene palabras adentro, las sacamos
        for palabra in cajonActual:
            palabrasOrdenadas.append((palabra, i))

    return palabrasOrdenadas

def radixSort(frecuencias):
    # Si viene vacío, devolvemos una lista vacía
    if len(frecuencias) == 0:
        return []

    # 1. Pasar el diccionario a una lista de parejas clásica: (palabra, cantidad)
    elementos = []
    for palabra in frecuencias:
        cantidad = frecuencias[palabra]
        elementos.append((palabra, cantidad))

    # 2. Buscar el número más grande para saber cuántos dígitos vamos a procesar
    frecuenciaMaxima = max(frecuencias.values())
    
    # 3. Ordenar dígito por dígito (unidades, decenas, centenas...)
    exponente = 1
    while (frecuenciaMaxima // exponente) > 0:
        elementos = ordenarPorDigito(elementos, exponente)
        exponente = exponente * 10

    # 4. Invertir la lista a mano (porque Radix los deja de menor a mayor)
    elementosInvertidos = []
    for i in range(len(elementos) - 1, -1, -1):
        elementosInvertidos.append(elementos[i])

    return elementosInvertidos


def ordenarPorDigito(elementos, exponente):
    cantidadElementos = len(elementos)
    
    # Preparamos el arreglo final y los 10 cajones para los dígitos (del 0 al 9)
    resultado = [0] * cantidadElementos
    conteoDigitos = [0] * 10

    # Paso A: Extraer el dígito que toca y contarlo
    for i in range(cantidadElementos):
        pareja = elementos[i]
        frecuencia = pareja[1]
        
        # Esta fórmula matemática saca el dígito exacto (unidades, luego decenas...)
        digito = (frecuencia // exponente) % 10
        conteoDigitos[digito] = conteoDigitos[digito] + 1

    # Paso B: Suma acumulada para calcular las posiciones finales de cada cajón
    for i in range(1, 10):
        conteoDigitos[i] = conteoDigitos[i] + conteoDigitos[i - 1]

    # Paso C: Acomodar los elementos leyendo de atrás hacia adelante para no desordenar los empates
    i = cantidadElementos - 1
    while i >= 0:
        pareja = elementos[i]
        frecuencia = pareja[1]
        digito = (frecuencia // exponente) % 10
        
        # Miramos en qué posición del resultado debe ir este elemento
        posicion = conteoDigitos[digito] - 1
        resultado[posicion] = pareja
        
        # Descontamos 1 para el siguiente número que termine en ese mismo dígito
        conteoDigitos[digito] = conteoDigitos[digito] - 1
        i = i - 1

    return resultado

def bucketSort(frecuencias):
    # Validación inicial por si no hay datos
    if len(frecuencias) == 0:
        return []

    frecuenciaMaxima = max(frecuencias.values())
    
    # 1. Crear las cubetas (una lista de listas vacías)
    cubetas = []
    for i in range(frecuenciaMaxima + 1):
        cubetas.append([])
        
    # 2. Distribuir cada elemento en su cubeta correspondiente
    for palabra in frecuencias:
        cantidad = frecuencias[palabra]
        
        # A diferencia del Counting Sort, aquí guardamos el paquete completo
        pareja = (palabra, cantidad)
        cubetas[cantidad].append(pareja)
        
    # 3. Recolectar el contenido de las cubetas de mayor a menor
    palabrasOrdenadas = []
    
    # Vamos desde la cubeta más alta hasta la cubeta cero
    for i in range(frecuenciaMaxima, -1, -1):
        cubetaActual = cubetas[i]
        
        # Si la cubeta tiene elementos adentro, los vaciamos en la lista final
        for elemento in cubetaActual:
            palabrasOrdenadas.append(elemento)
            
    return palabrasOrdenadas