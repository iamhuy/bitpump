import cognitive_face as CF

# Replace with a valid subscription key (keeping the quotes in place).
KEY = 'd2ccb3ca6972497bba7b2c2ef8c2d8d9'
CF.Key.set(KEY)

# Replace with your regional Base URL
BASE_URL = 'https://westcentralus.api.cognitive.microsoft.com/face/v1.0'
CF.BaseUrl.set(BASE_URL)

GROUP_ID = "bitpump"
CF.person_group.train(GROUP_ID)


class ImageVerifier(object):
    @classmethod
    def add_face(cls, full_name, image):
        person_id = CF.person.create(GROUP_ID, name=full_name).get('personId')
        CF.person.add_face(image, GROUP_ID, person_id)
        CF.person_group.train(GROUP_ID)
        return person_id

    @classmethod
    def find_user_in_image(cls, image):
        face_list = CF.face.detect(image)
        face_ids = []
        for face in face_list:
            face_ids.append(face['faceId'])
        results = CF.face.identify(face_ids=face_ids,
                                   person_group_id=GROUP_ID,
                                   max_candidates_return=1,
                                   threshold=0.5)

        person_id_list = []
        for result in results:
            if result['candidates']:
                person_id_list.append(result['candidates'][0]['personId'])
        return person_id_list
