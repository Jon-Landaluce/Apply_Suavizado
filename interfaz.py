import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
from statistics import mean

def image_to_matrix(image_path):
    img = Image.open(image_path)
    matrix = list(img.getdata())
    width, height = img.size
    channels = len(matrix[0]) if matrix else 0
    return [matrix[i * width:(i + 1) * width] for i in range(height)], channels

def matrix_to_image(matrix, channels):
    height = len(matrix)
    width = len(matrix[0])
    img = Image.new("RGB" if channels == 3 else "L", (width, height))

    for i in range(height):
        for j in range(width):
            pixel_value = tuple(map(int, matrix[i][j])) if channels == 3 else int(matrix[i][j])
            img.putpixel((j, i), pixel_value)

    return img

def process_matrix(matrix, channels):
    result_matrix = []

    for i in range(len(matrix)):
        temporalList = []
        for j in range(len(matrix[0])):
            if i == 0 and j == 0:
                temporalList.append((
                    (matrix[0][0][0] + matrix[0][1][0] + matrix[1][0][0]) // 3,
                    (matrix[0][0][1] + matrix[0][1][1] + matrix[1][0][1]) // 3,
                    (matrix[0][0][2] + matrix[0][1][2] + matrix[1][0][2]) // 3
                ))
            elif i == 0 and j == len(matrix[i]) - 1:
                temporalList.append((
                    (matrix[0][-2][0] + matrix[0][-1][0] + matrix[1][-1][0]) // 3,
                    (matrix[0][-2][1] + matrix[0][-1][1] + matrix[1][-1][1]) // 3,
                    (matrix[0][-2][2] + matrix[0][-1][2] + matrix[1][-1][2]) // 3
                ))
            elif i == len(matrix) - 1 and j == 0:
                temporalList.append((
                    (matrix[-1][0][0] + matrix[-1][1][0] + matrix[-2][0][0]) // 3,
                    (matrix[-1][0][1] + matrix[-1][1][1] + matrix[-2][0][1]) // 3,
                    (matrix[-1][0][2] + matrix[-1][1][2] + matrix[-2][0][2]) // 3
                ))
            elif i == len(matrix) - 1 and j == len(matrix[i]) - 1:
                temporalList.append((
                    (matrix[-1][-1][0] + matrix[-1][-2][0] + matrix[-2][-1][0]) // 3,
                    (matrix[-1][-1][1] + matrix[-1][-2][1] + matrix[-2][-1][1]) // 3,
                    (matrix[-1][-1][2] + matrix[-1][-2][2] + matrix[-2][-1][2]) // 3
                ))
            elif i == 0 and (j != 0 and j != len(matrix[i])):
                temporalList.append((
                    (matrix[i][j][0] + matrix[i][j - 1][0] + matrix[i][j + 1][0] + matrix[1][j][0]) // 4,
                    (matrix[i][j][1] + matrix[i][j - 1][1] + matrix[i][j + 1][1] + matrix[1][j][1]) // 4,
                    (matrix[i][j][2] + matrix[i][j - 1][2] + matrix[i][j + 1][2] + matrix[1][j][2]) // 4
                ))
            elif i == len(matrix) - 1 and (j != 0 and j != len(matrix[i])):
                temporalList.append((
                    (matrix[i][j][0] + matrix[i][j - 1][0] + matrix[i][j + 1][0] + matrix[i - 1][j][0]) // 4,
                    (matrix[i][j][1] + matrix[i][j - 1][1] + matrix[i][j + 1][1] + matrix[i - 1][j][1]) // 4,
                    (matrix[i][j][2] + matrix[i][j - 1][2] + matrix[i][j + 1][2] + matrix[i - 1][j][2]) // 4
                ))
            elif (i != 0 and i != len(matrix) - 1) and j == 0:
                temporalList.append((
                    (matrix[i][0][0] + matrix[i - 1][0][0] + matrix[i + 1][0][0] + matrix[i][1][0]) // 4,
                    (matrix[i][0][1] + matrix[i - 1][0][1] + matrix[i + 1][0][1] + matrix[i][1][1]) // 4,
                    (matrix[i][0][2] + matrix[i - 1][0][2] + matrix[i + 1][0][2] + matrix[i][1][2]) // 4
                ))
            elif (i != 0 and i != len(matrix) - 1) and j == len(matrix[i]) - 1:
                temporalList.append((
                    (matrix[i][len(matrix[i]) - 1][0] + matrix[i - 1][len(matrix[i]) - 1][0] + matrix[i + 1][len(matrix[i]) - 1][0] + matrix[i][len(matrix[i]) - 2][0]) // 4,
                    (matrix[i][len(matrix[i]) - 1][1] + matrix[i - 1][len(matrix[i]) - 1][1] + matrix[i + 1][len(matrix[i]) - 1][1] + matrix[i][len(matrix[i]) - 2][1]) // 4,
                    (matrix[i][len(matrix[i]) - 1][2] + matrix[i - 1][len(matrix[i]) - 1][2] + matrix[i + 1][len(matrix[i]) - 1][2] + matrix[i][len(matrix[i]) - 2][2]) // 4
                ))
            else:
                temporalList.append((
                    (matrix[i][j][0] + matrix[i + 1][j][0] + matrix[i - 1][j][0] + matrix[i][j + 1][0] + matrix[i][j - 1][0]) // 5,
                    (matrix[i][j][1] + matrix[i + 1][j][1] + matrix[i - 1][j][1] + matrix[i][j + 1][1] + matrix[i][j - 1][1]) // 5,
                    (matrix[i][j][2] + matrix[i + 1][j][2] + matrix[i - 1][j][2] + matrix[i][j + 1][2] + matrix[i][j - 1][2]) // 5
                ))
            if channels == 3:
                result_matrix.append(temporalList)
            else:
                avg_value = int(mean(matrix[i][j]))
                result_matrix.append(avg_value)
    return result_matrix

def double_smooth(matrix, channels):
    # Tu función double_smooth aquí
    pass

def open_file():
    file_path = filedialog.askopenfilename()
    original_matrix, channels = image_to_matrix(file_path)
    result_matrix = double_smooth(process_matrix(original_matrix, channels), channels)
    result_image = matrix_to_image(result_matrix, channels)

    update_image(result_image)

def update_image(img):
    img = ImageTk.PhotoImage(img)
    panel.config(image=img)
    panel.image = img

# Crear la ventana principal
root = tk.Tk()
root.title("Filtro de Suavizado Doble")

# Botón para cargar imagen
btn_load_image = tk.Button(root, text="Cargar Imagen", command=open_file)
btn_load_image.pack(pady=10)

# Panel para mostrar la imagen
panel = tk.Label(root)
panel.pack()

# Iniciar el bucle principal
root.mainloop()
