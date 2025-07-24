import requests

class WLFIApiClient:
    def __init__(self, base_url="http://localhost:3001"):
        self.base_url = base_url

    def get_image(self, token_id: str):
        """
        Fetches the SVG image for a given token ID.
        """
        url = f"{self.base_url}/image/{token_id}"
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.text

    def get_metadata(self, token_id: str):
        """
        Fetches the metadata for a given token ID.
        """
        url = f"{self.base_url}/metadata/{token_id}"
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.json()

if __name__ == '__main__':
    # Example Usage:
    client = WLFIApiClient()

    # Get image
    try:
        image_svg = client.get_image("123") # Replace with a valid tokenId from your DB
        print("Image SVG (first 200 chars):\n", image_svg[:200])
    except requests.exceptions.RequestException as e:
        print(f"Error fetching image: {e}")

    # Get metadata
    try:
        metadata = client.get_metadata("123") # Replace with a valid tokenId from your DB
        print("\nMetadata:\n", metadata)
    except requests.exceptions.RequestException as e:
        print(f"Error fetching metadata: {e}")

