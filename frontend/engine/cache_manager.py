import hashlib
import json
import os
from pathlib import Path

class CacheManager:
    def __init__(self, cache_dir="data/cache"):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def _get_image_hash(self, image_data):
        """Generates a SHA-256 hash for the image data."""
        return hashlib.sha256(image_data).hexdigest()

    def get_cached_result(self, image_data):
        """Retrieves cached result if it exists."""
        img_hash = self._get_image_hash(image_data)
        cache_file = self.cache_dir / f"{img_hash}.json"
        if cache_file.exists():
            with open(cache_file, "r") as f:
                return json.load(f)
        return None

    def save_to_cache(self, image_data, result):
        """Saves the result to cache using the image hash as the filename."""
        img_hash = self._get_image_hash(image_data)
        cache_file = self.cache_dir / f"{img_hash}.json"
        with open(cache_file, "w") as f:
            json.dump(result, f, indent=4)
