
from PIL import Image

def image_to_matrix(image_path):
    img = Image.open(image_path)
    matrix = list(img.getdata())
    width, height = img.size
    channels = len(matrix[0]) if matrix else 0
    return [matrix[i * width:(i + 1) * width] for i in range(height)], channels

def matrix_to_image(matrix, channels, output_path):
    height = len(matrix)
    width = len(matrix[0])
    img = Image.new("RGB" if channels == 3 else "L", (width, height))

    for i in range(height):
        for j in range(width):
            pixel_value = tuple(map(int, matrix[i][j])) if channels == 3 else int(matrix[i][j])
            img.putpixel((j, i), pixel_value)

    img.save(output_path)

def double_smooth(matrix, channels):
    result_matrix = []

    # Verificar si la matriz tiene longitud menor o igual a 1
    if len(matrix) <= 1:
        return result_matrix

    # Bucle externo para iterar matrix y asignar valores a las filas
    for i, row in enumerate(matrix):
        temporalList = []

        # Bucle interno para iterar y dar valores a los elementos de las filas
        for j, value in enumerate(row):
            neighbors = [
                matrix[i-1][j] if i > 0 else [0] * channels,
                matrix[i+1][j] if i < len(matrix) - 1 else [0] * channels,
                matrix[i][j-1] if j > 0 else [0] * channels,
                matrix[i][j+1] if j < len(row) - 1 else [0] * channels,
                matrix[i][j]
            ]

            # Calcular el promedio manualmente
            average = [sum(channel) / len(channel) for channel in zip(*neighbors)]
            temporalList.append(average)

        result_matrix.append(temporalList)

    return result_matrix

# Ruta de la imagen JPG
image_path = "arbol.jpg"

# Convertir la imagen a matriz
original_matrix, channels = image_to_matrix(image_path)

# Aplicar la doble función de suavizado
result_matrix = double_smooth(original_matrix, channels)

# Guardar la nueva imagen
output_path = "imagen_doble_suavizado.jpeg"
matrix_to_image(result_matrix, channels, output_path)

print(f"La imagen con doble suavizado ha sido guardada en {output_path}")
from PIL import Image

def image_to_matrix(image_path):
    img = Image.open(image_path)
    matrix = list(img.getdata())
    width, height = img.size
    channels = len(matrix[0]) if matrix else 0
    return [matrix[i * width:(i + 1) * width] for i in range(height)], channels

def matrix_to_image(matrix, channels, output_path):
    height = len(matrix)
    width = len(matrix[0])
    img = Image.new("RGB" if channels == 3 else "L", (width, height))

    for i in range(height):
        for j in range(width):
            pixel_value = tuple(map(int, matrix[i][j])) if channels == 3 else int(matrix[i][j])
            img.putpixel((j, i), pixel_value)

    img.save(output_path)

def double_smooth(matrix, channels):
    result_matrix = []

    # Verificar si la matriz tiene longitud menor o igual a 1
    if len(matrix) <= 1:
        return result_matrix

    # Bucle externo para iterar matrix y asignar valores a las filas
    for i, row in enumerate(matrix):
        temporalList = []

        # Bucle interno para iterar y dar valores a los elementos de las filas
        for j, value in enumerate(row):
            neighbors = [
                matrix[i-1][j] if i > 0 else [0] * channels,
                matrix[i+1][j] if i < len(matrix) - 1 else [0] * channels,
                matrix[i][j-1] if j > 0 else [0] * channels,
                matrix[i][j+1] if j < len(row) - 1 else [0] * channels,
                matrix[i][j]
            ]

            # Calcular el promedio manualmente
            average = [sum(channel) / len(channel) for channel in zip(*neighbors)]
            temporalList.append(average)

        result_matrix.append(temporalList)

    return result_matrix

# Ruta de la imagen JPG
image_path = "arbol.jpg"

# Convertir la imagen a matriz
original_matrix, channels = image_to_matrix(image_path)

# Aplicar la doble función de suavizado
result_matrix = double_smooth(original_matrix, channels)

# Guardar la nueva imagen
output_path = "imagen_doble_suavizado.jpeg"
matrix_to_image(result_matrix, channels, output_path)

print(f"La imagen con doble suavizado ha sido guardada en {output_path}")
