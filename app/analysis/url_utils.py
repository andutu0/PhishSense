from urllib.parse import urlparse

def extract_url_features(url):
    parsed = urlparse(url)
    domain = parsed.netloc
    path = parsed.path
    features = {
        "length": len(url),
        "num_subdomains": domain.count("."),
        "has_ip": any(char.isdigit() for char in domain),
        "path_length": len(path),
    }
    return features
