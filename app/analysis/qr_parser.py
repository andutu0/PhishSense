from typing import Optional
from PIL import Image
from pyzbar.pyzbar import decode

# decode QR code from uploaded file
def decode_qr_from_file(file_storage) -> Optional[str]:
    try:
        # open image from file storage
        image = Image.open(file_storage.stream)
        
        # decode QR codes in the image
        decoded_objects = decode(image)
        
        if not decoded_objects:
            return None
        
        # get the first QR code's data
        data = decoded_objects[0].data.decode("utf-8", errors="ignore")
        
        return data
        
    except Exception as e:
        print(f"Error decoding QR code: {e}")
        return None

# decode QR code from uploaded file and determine its type
# so we can know if it's a URL or plain text
# in order to analyze it properly
def decode_qr_image(file_storage) -> dict:
    data = decode_qr_from_file(file_storage)
    
    if not data:
        return {
            "raw_data": None,
            "type": "unknown",
        }
    
    # determine type
    if data.startswith("http://") or data.startswith("https://"):
        data_type = "url"
    else:
        data_type = "text"
    
    return {
        "raw_data": data,
        "type": data_type,
    }