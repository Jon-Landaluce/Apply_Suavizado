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

def process_matrix(matrix, channels):
    rows = len(matrix)
    if rows == 0:
        return []

    columns = len(matrix[0])
    result_matrix = []

    for i in range(rows):
        new_row = []
        for j in range(columns):
            neighbors_sum = [0] * channels
            count_neighbors = 0

            if i > 0:
                neighbors_sum = [sum(x) for x in zip(neighbors_sum, matrix[i - 1][j])]
                count_neighbors += 1

            if i < rows - 1:
                neighbors_sum = [sum(x) for x in zip(neighbors_sum, matrix[i + 1][j])]
                count_neighbors += 1

            if j > 0:
                neighbors_sum = [sum(x) for x in zip(neighbors_sum, matrix[i][j - 1])]
                count_neighbors += 1

            if j < columns - 1:
                neighbors_sum = [sum(x) for x in zip(neighbors_sum, matrix[i][j + 1])]
                count_neighbors += 1

            neighbors_sum = [sum(x) for x in zip(neighbors_sum, matrix[i][j])]
            count_neighbors += 1

            average = [x / count_neighbors for x in neighbors_sum]
            new_row.append(average)

        result_matrix.append(new_row)

    return result_matrix

    
def double_smooth(matrix, channels):
    rows = len(matrix)
    if rows == 0:
        return []

    columns = len(matrix[0])
    result_matrix = []

    for i in range(rows):
        new_row = []
        for j in range(columns):
            neighbors_sum = [0] * channels
            count_neighbors = 0

            # Top 
            if i > 0:
                neighbors_sum = [sum(x) for x in zip(neighbors_sum, matrix[i - 1][j])]
                count_neighbors += 1

            # Bottom 
            if i < rows - 1:
                neighbors_sum = [sum(x) for x in zip(neighbors_sum, matrix[i + 1][j])]
                count_neighbors += 1

            # Left 
            if j > 0:
                neighbors_sum = [sum(x) for x in zip(neighbors_sum, matrix[i][j - 1])]
                count_neighbors += 1

            # Right 
            if j < columns - 1:
                neighbors_sum = [sum(x) for x in zip(neighbors_sum, matrix[i][j + 1])]
                count_neighbors += 1

            # central 
            neighbors_sum = [sum(x) for x in zip(neighbors_sum, matrix[i][j])]
            count_neighbors += 1

           
            average = [x / count_neighbors for x in neighbors_sum]
            new_row.append(average)

        result_matrix.append(new_row)

    return result_matrix
# Ruta de la imagen JPG
image_path = "arbol.jpg"

# Convertir la imagen a matriz
original_matrix, channels = image_to_matrix(image_path)

# Aplicar la doble función de suavizado
result_matrix = double_smooth(process_matrix(original_matrix, channels), channels)

# Guardar la nueva imagen
output_path = "imagen_doble_suavizado.jpeg"
matrix_to_image(result_matrix, channels, output_path)

print(f"La imagen con doble suavizado ha sido guardada en {output_path}")
