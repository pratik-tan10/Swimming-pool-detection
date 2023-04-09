import math
import urllib.request
from PIL import Image

# Set the coordinates of the area you want to download
lat1, lon1 = 37.4219999, -122.0840575  # top-left corner
lat2, lon2 = 37.4087165, -122.0564341  # bottom-right corner

# Calculate the distance between the two points
R = 6371  # radius of the Earth in km
dLat = math.radians(lat2 - lat1)
dLon = math.radians(lon2 - lon1)
a = math.sin(dLat/2) * math.sin(dLat/2) + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dLon/2) * math.sin(dLon/2)
c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
distance = R * c

# Set the size of the image based on the distance between the two points
size = (math.ceil(distance * 1000 / 5), math.ceil(distance * 1000 / 1))  # 25 meters per pixel

# Download the image
url = f"https://maps.googleapis.com/maps/api/staticmap?center={lat1},{lon1}&zoom=15&size={size[0]}x{size[1]}&maptype=satellite&key=YOUR_API_KEY"
image_data = urllib.request.urlopen(url).read()
image = Image.open(BytesIO(image_data))

# Save the image
image.save("image.png")
