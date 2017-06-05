import face_recognition as fr
import numpy as np
import sys


def load_known_encoding(file_name):
	return np.load(file_name)

def get_pic_encodings(pic_name):
	img = fr.load_image_file(pic_name)
	enc = fr.face_encodings(img)
	return enc

def run_recognizer(path, names):
#	path = "../face_recognizer/hilary.jpg"
	encodings = get_pic_encodings(path)
	if len(encodings) == 0:
		return None
	unk_enc = encodings[0]
	known_names_files = [x + ".npy" for x in names]
	known_encodings = [load_known_encoding(x) for x in known_names_files]
	results = fr.compare_faces(known_encodings, unk_enc)

	for i,j in zip(names, results):
		if j:
			return i

	return None
