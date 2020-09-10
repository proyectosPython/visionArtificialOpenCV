# Importamos la libreria Pillow
from PIL import Image

# Importamos Pytesseract
import pytesseract

# Abrimos la imagen
im = Image.open("example_01.png")

# Utilizamos el método "image_to_string"
# Le pasamos como argumento la imagen abierta con Pillow
texto = pytesseract.image_to_string(im)

# Mostramos el resultado
print(texto)