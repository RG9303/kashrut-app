import requests

class OpenFoodFactsClient:
    def __init__(self):
        self.base_url = "https://world.openfoodfacts.org/api/v2/product/"
        self.headers = {
            "User-Agent": "KashrutApp/1.0 (tescaelements@example.com) - Digital Mashgiach"
        }

    def get_product(self, barcode):
        """
        Busca un producto por código de barras.
        Retorna un dict con 'product_name' e 'ingredients_text' si se encuentra.
        """
        if not barcode:
            return None

        try:
            url = f"{self.base_url}{barcode}.json"
            response = requests.get(url, headers=self.headers, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('status') == 1:
                    product = data.get('product', {})
                    return {
                        "product_name": product.get('product_name', 'Nombre no disponible'),
                        "ingredients_text": product.get('ingredients_text_es') or product.get('ingredients_text', 'Ingredientes no disponibles'),
                        "brands": product.get('brands', ''),
                        "image_url": product.get('image_front_url', '')
                    }
        except Exception as e:
            print(f"Error OFF API: {e}")
            return None
        
        return None
