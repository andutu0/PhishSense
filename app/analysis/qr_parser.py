from typing import Dict, Any

from PIL import Image
from pyzbar.pyzbar import decode


def decode_qr_image(file_storage) -> Dict[str, Any]:
    image = Image.open(file_storage.stream)
    decoded = decode(image)

    if not decoded:
        return {
            "raw_data": None,
            "type": "unknown",
        }

    data = decoded[0].data.decode("utf8", errors="ignore")

    if data.startswith("http://") or data.startswith("https://"):
        data_type = "url"
    else:
        data_type = "text"

    return {
        "raw_data": data,
        "type": data_type,
    }
