import ddddocr

def recognize(image):
    ocr = ddddocr.DdddOcr()
    with open(image, 'rb') as f:
        img_bytes = f.read()
    res = ocr.classification(img_bytes)
    return res


