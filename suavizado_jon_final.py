from PIL import Image

def image_to_matrix(image_path):
    img = Image.open(image_path)
    matrix = list(img.getdata())
    width, height = img.size
    channels = len(matrix[0]) if matrix else 0

    # Convertir tuplas a listas
    matrix = [list(pixel) for pixel in matrix]

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
            # Promedio Esquina Superior Izquierda
            if i == 0 and j == 0:
                temporalList.append((
                    (matrix[0][0][0] + matrix[0][1][0] + matrix[1][0][0]) // 3,
                    (matrix[0][0][1] + matrix[0][1][1] + matrix[1][0][1]) // 3,
                    (matrix[0][0][2] + matrix[0][1][2] + matrix[1][0][2]) // 3
                ))

            # Promedio Esquina Superior Derecha
            elif i == 0 and j == len(matrix[i]) - 1:
                temporalList.append((
                    (matrix[0][-2][0] + matrix[0][-1][0] + matrix[1][-1][0]) // 3,
                    (matrix[0][-2][1] + matrix[0][-1][1] + matrix[1][-1][1]) // 3,
                    (matrix[0][-2][2] + matrix[0][-1][2] + matrix[1][-1][2]) // 3
                ))

            # Promedio Esquina Inferior Izquierda
            elif i == len(matrix) - 1 and j == 0:
                temporalList.append((
                    (matrix[-1][0][0] + matrix[-1][1][0] + matrix[-2][0][0]) // 3,
                    (matrix[-1][0][1] + matrix[-1][1][1] + matrix[-2][0][1]) // 3,
                    (matrix[-1][0][2] + matrix[-1][1][2] + matrix[-2][0][2]) // 3
                ))

            # Promedio Esquina Inferior Derecha
            elif i == len(matrix) - 1 and j == len(matrix[i]) - 1:
                temporalList.append((
                    (matrix[-1][-1][0] + matrix[-1][-2][0] + matrix[-2][-1][0]) // 3,
                    (matrix[-1][-1][1] + matrix[-1][-2][1] + matrix[-2][-1][1]) // 3,
                    (matrix[-1][-1][2] + matrix[-1][-2][2] + matrix[-2][-1][2]) // 3
                ))

            # Promedio Elementos Borde Superior
            elif i == 0 and (j != 0 and j != len(matrix[i])):
                temporalList.append((
                    (matrix[i][j][0] + matrix[i][j - 1][0] + matrix[i][j + 1][0] + matrix[1][j][0]) // 4,
                    (matrix[i][j][1] + matrix[i][j - 1][1] + matrix[i][j + 1][1] + matrix[1][j][1]) // 4,
                    (matrix[i][j][2] + matrix[i][j - 1][2] + matrix[i][j + 1][2] + matrix[1][j][2]) // 4
                ))

            # Promedio Elementos Borde Inferior
            elif i == len(matrix) - 1 and (j != 0 and j != len(matrix[i])):
                temporalList.append((
                    (matrix[i][j][0] + matrix[i][j - 1][0] + matrix[i][j + 1][0] + matrix[i - 1][j][0]) // 4,
                    (matrix[i][j][1] + matrix[i][j - 1][1] + matrix[i][j + 1][1] + matrix[i - 1][j][1]) // 4,
                    (matrix[i][j][2] + matrix[i][j - 1][2] + matrix[i][j + 1][2] + matrix[i - 1][j][2]) // 4
                ))

            # Promedio Elementos Borde Izquierdo
            elif (i != 0 and i != len(matrix) - 1) and j == 0:
                temporalList.append((
                    (matrix[i][0][0] + matrix[i - 1][0][0] + matrix[i + 1][0][0] + matrix[i][1][0]) // 4,
                    (matrix[i][0][1] + matrix[i - 1][0][1] + matrix[i + 1][0][1] + matrix[i][1][1]) // 4,
                    (matrix[i][0][2] + matrix[i - 1][0][2] + matrix[i + 1][0][2] + matrix[i][1][2]) // 4
                ))

            # Promedio Elementos Borde Derecho
            elif (i != 0 and i != len(matrix) - 1) and j == len(matrix[i]) - 1:
                temporalList.append((
                    (matrix[i][len(matrix[i]) - 1][0] + matrix[i - 1][len(matrix[i]) - 1][0] + matrix[i + 1][len(matrix[i]) - 1][0] + matrix[i][len(matrix[i]) - 2][0]) // 4,
                    (matrix[i][len(matrix[i]) - 1][1] + matrix[i - 1][len(matrix[i]) - 1][1] + matrix[i + 1][len(matrix[i]) - 1][1] + matrix[i][len(matrix[i]) - 2][1]) // 4,
                    (matrix[i][len(matrix[i]) - 1][2] + matrix[i - 1][len(matrix[i]) - 1][2] + matrix[i + 1][len(matrix[i]) - 1][2] + matrix[i][len(matrix[i]) - 2][2]) // 4
                ))

            # Promedio Elementos Internos
            else:
                temporalList.append((
                    (matrix[i][j][0] + matrix[i + 1][j][0] + matrix[i - 1][j][0] + matrix[i][j + 1][0] + matrix[i][j - 1][0]) // 5,
                    (matrix[i][j][1] + matrix[i + 1][j][1] + matrix[i - 1][j][1] + matrix[i][j + 1][1] + matrix[i][j - 1][1]) // 5,
                    (matrix[i][j][2] + matrix[i + 1][j][2] + matrix[i - 1][j][2] + matrix[i][j + 1][2] + matrix[i][j - 1][2]) // 5
                ))

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







