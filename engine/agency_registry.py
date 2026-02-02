"""
Registro de agencias certificadoras confiables y sus enlaces de verificación.
"""

AGENCY_REGISTRY = {
    "OU": {
        "full_name": "Orthodox Union",
        "website": "https://oukosher.org/product-search/",
        "icon": "✅",
        "description": "La agencia certificadora más grande y reconocida mundialmente."
    },
    "OK": {
        "full_name": "OK Kosher Certification",
        "website": "https://www.ok.org/consumers/kosher-food-guide/",
        "icon": "✅",
        "description": "Certificadora global altamente respetada."
    },
    "STAR-K": {
        "full_name": "Star-K Kosher Certification",
        "website": "https://www.star-k.org/products",
        "icon": "✅",
        "description": "Conocida por sus altos estándares tecnológicos y halájicos."
    },
    "CRC": {
        "full_name": "Chicago Rabbinical Council",
        "website": "https://crcweb.org/kosher/consumer/symbol_search",
        "icon": "✅",
        "description": "Consejo Rabínico de Chicago."
    },
    "KOF-K": {
        "full_name": "Kof-K Kosher Supervision",
        "website": "https://www.kof-k.org/Industrial/KosherCertificates.aspx",
        "icon": "✅",
        "description": "Agencia internacional con sede en NJ."
    },
    "KMD": {
        "full_name": "Kosher Maguén David (México)",
        "website": "https://kosher.com.mx/",
        "icon": "🇲🇽",
        "description": "Principal certificación de la Comunidad Maguén David en México."
    },
    "ALEF": {
        "full_name": "Alef / One Kosher",
        "website": "https://onekosher.com/",
        "icon": "🇲🇽",
        "description": "Agencia de certificación con fuerte presencia en México y Latam."
    },
    "KA": {
        "full_name": "Kashrut Authority (Australia)",
        "website": "https://www.ka.org.au/",
        "icon": "🇦🇺",
        "description": "Autoridad principal en Australia."
    },
    "KF": {
        "full_name": "Federation of Synagogues (UK)",
        "website": "https://www.kfkosher.org/",
        "icon": "🇬🇧",
        "description": "Certificación prominente en Reino Unido y Europa."
    }
}

def check_agency(symbol_name: str):
    """
    Busca si el símbolo detectado coincide con alguna agencia en nuestro registro.
    Intenta coincidencia parcial o exacta.
    """
    symbol_upper = symbol_name.upper().strip()
    
    # Búsqueda exacta
    if symbol_upper in AGENCY_REGISTRY:
        return AGENCY_REGISTRY[symbol_upper]
    
    # Búsqueda parcial (ej. "OU Pareve" -> "OU")
    for key, data in AGENCY_REGISTRY.items():
        if key in symbol_upper or symbol_upper.replace("THE", "").strip() in data["full_name"].upper():
            return data
            
    return None
