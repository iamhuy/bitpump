import cloudinary
from cloudinary import uploader

cloudinary.config(
  cloud_name="dneb2htng",
  api_key="144135535139985",
  api_secret="CX4fwIYq8f6RyU7BsGVzecHQULM"
)


def image_upload(name, file_path):
    return uploader.upload(file_path, public_id=name).get('url')
