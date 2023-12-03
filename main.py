from PIL import Image
import cv2
import numpy as np
from pyzbar.pyzbar import decode
import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('ip.com', 2222))

for j in range(0, 100):
    text = ""
    t = ""
    for i in range(1,3):
        text += s.recv(8192).decode("utf-8", 'ignore')
        if i % 2 == 0:
            text = text.replace("▇", "1")
            text = text.replace(" ", "0")
            text = text.split("\n")
            text = text[27:-3]
            for j in range(21):
                t += text[j][3:-2] + "\n"

                if (len(t) != 41):
                    t += "0"
    # Преобразовываем массив в строку
    t = ''.join([''.join(row) for row in t])
    t = t.split("\n")[:-1]

    qr_code_array = t

    # Определяем размеры изображения
    width = 41
    height = 21

    # Создаем изображение
    img = Image.new('RGB', (width, height), color='white')
    pixels = img.load()

    # Заполняем изображение пикселями
    for i in range(height):
        for j in range(width):
            color = (0, 0, 0) if qr_code_array[i][j] == '1' else (255, 255, 255)
            pixels[j, i] = color

    # Сохраняем изображение
    img.save("generated_qr_code.png")

    image_path = 'generated_qr_code.png'

    img = Image.open(image_path)
    # изменяем размер
    new_image = img.resize((200, 200))
    # сохранение картинки
    new_image.save('generated_qr_code.png')

    def read_qr_code(image_path):
        # Загрузка изображения
        image = cv2.imread(image_path)

        # Преобразование изображения в оттенки серого
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Распознавание QR-кода
        qr_codes = decode(gray)

        # Вывод результатов
        for qr_code in qr_codes:
            data = qr_code.data.decode('utf-8')

            # Отрисовка прямоугольника вокруг QR-кода
            rect_points = qr_code.polygon
            if len(rect_points) == 4:
                pts = []
                for pt in rect_points:
                    pts.append([pt.x, pt.y])
                pts = np.array(pts, dtype=int)
                pts = pts.reshape((-1, 1, 2))
                cv2.polylines(image, [pts], True, (0, 255, 0), 2)
        return data

    image_path = "generated_qr_code.png"
    data = read_qr_code(image_path)
    print(data)
    answer = eval(data)
    ans = str(answer) + "\n"
    s.send(str(ans).encode('UTF-8'))
