import os
import requests
from PIL import Image
from io import BytesIO

def get_video_images(video_id: str, output_dir: str) -> list:
    """
    Downloads the highest quality thumbnail for a YouTube video.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Try maxresdefault first, then hqdefault
    urls = [
        f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg",
        f"https://img.youtube.com/vi/{video_id}/hqdefault.jpg"
    ]

    saved_files = []

    for url in urls:
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                img = Image.open(BytesIO(response.content))
                
                # Convert to WebP and resize if necessary
                output_path = os.path.join(output_dir, "thumbnail.webp")
                
                # Resize if massive (optional, keeping high quality for now)
                if img.width > 1920:
                    img.thumbnail((1920, 1080))

                img.save(output_path, "WEBP", quality=85)
                saved_files.append(output_path)
                print(f"Downloaded thumbnail: {output_path}")
                break # Stop after finding the best quality
        except Exception as e:
            print(f"Error downloading thumbnail from {url}: {e}")
            continue

    return saved_files
