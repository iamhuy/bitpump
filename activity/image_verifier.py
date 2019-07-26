import cognitive_face as CF

# Replace with a valid subscription key (keeping the quotes in place).
KEY = '2cd79f0da8014515b1b4ab75bb73125e'
CF.Key.set(KEY)

# Replace with your regional Base URL
BASE_URL = 'https://westcentralus.api.cognitive.microsoft.com/face/v1.0'
CF.BaseUrl.set(BASE_URL)

# You can use this example JPG or replace the URL below with your own URL to a JPEG image.
img_url = 'https://raw.githubusercontent.com/Microsoft/Cognitive-Face-Windows/master/Data/detection1.jpg'
faces = CF.face.detect(img_url)
print(faces)


class ImageVerifier(object):
    @classmethod
    def _find_user_in_image(cls, image):
        CF.face.detect(image)
