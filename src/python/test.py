image_arrays=[]

from face_recognition.api import batch_face_locations
face_locations = batch_face_locations(
        images=image_arrays, number_of_times_to_upsample=0, batch_size=8)
top, right, bottom, left = face_locations