from PIL import Image


image = Image.open("mondial.jpg")
image.show()
image.size
width, height = image.size
print(width)
print(height)
print(image.filename)
print(image.format)
print(image.format_description)
