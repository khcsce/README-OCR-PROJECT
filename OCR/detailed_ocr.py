import easyocr as ocr  #OCR

reader = ocr.Reader(['en'],model_storage_directory='.')

result = reader.readtext("computertext.png")
print(result)
