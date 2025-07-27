import requests

class WLFIApiClient:
    def __init__(self, base_url="https://metadata.wlfins.domains/"):
        self.base_url = base_url

    def get_image(self, token_id: str):
        """
        Fetches the SVG image for a given token ID.
        """
        url = f"{self.base_url}/image/{token_id}"
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.text

    def get_composite_image(self, token_id: str):
        """
        Fetches the composite PNG image for a given token ID.
        """
        url = f"{self.base_url}/composite-image/{token_id}"
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.content

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
    # Make sure your API server is running first!
    client = WLFIApiClient()

    # Replace with a valid tokenId from your database
    # This is the decimal representation of the namehash
    example_token_id = "2727872353928655157841542879942343446921942823933093953431841122373210533342"

    print(f"--- Testing with Token ID: {example_token_id} ---")

    # 1. Get Metadata
    try:
        metadata = client.get_metadata(example_token_id)
        print("\nSuccessfully fetched metadata:")
        for key, value in metadata.items():
            if key == 'attributes':
                print(f"  {key}:")
                for attr in value:
                    print(f"    - {attr['trait_type']}: {attr['value']}")
            else:
                print(f"  {key}: {value}")
    except requests.exceptions.RequestException as e:
        print(f"\nError fetching metadata: {e}")

    # 2. Get SVG Image
    try:
        image_svg = client.get_image(example_token_id)
        print("\nSuccessfully fetched SVG image.")
        # print("Image SVG (first 200 chars):\n", image_svg[:200])
    except requests.exceptions.RequestException as e:
        print(f"\nError fetching SVG image: {e}")

    # 3. Get Composite Image
    try:
        image_png = client.get_composite_image(example_token_id)
        print("\nSuccessfully fetched composite PNG image.")
        # To save the image:
        # with open("composite_image.png", "wb") as f:
        #     f.write(image_png)
        # print("Composite image saved to composite_image.png")
    except requests.exceptions.RequestException as e:
        print(f"\nError fetching composite image: {e}")