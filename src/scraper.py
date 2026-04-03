import os
from PIL import Image
from pyzbar.pyzbar import decode
from docling.document_converter import DocumentConverter

converter = DocumentConverter()


def extract_menu_data(source):
    """
    Decodes QR codes to URLs or performs OCR on local images.
    Returns structured Markdown.
    """
    final_source = source

    # QR Code Detection Logic
    if isinstance(source, str) and os.path.exists(source):
        try:
            img = Image.open(source)
            qr_codes = decode(img)
            if qr_codes:
                final_source = qr_codes[0].data.decode('utf-8')
                print(f"QR Code detected: {final_source}")
        except Exception as e:
            print(f"QR Check failed: {e}")

    try:
        result = converter.convert(final_source)
        return result.document.export_to_markdown()
    except Exception as e:
        print(f"Docling Conversion Error: {e}")
        return None