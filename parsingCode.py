import ddddocr

def recognize():
    ocr = ddddocr.DdddOcr()
    with open('yzm/CFAANG.jpg', 'rb') as f:
        img_bytes = f.read()
    res = ocr.classification(img_bytes)
    return res

recognize()
