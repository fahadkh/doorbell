import face_recognition as fr
import numpy as np
import sys

#Running "python save_encoding.py face_pic.jpg person_name" will save as person_name.npy

def save_encoding(file_name, person_name):
	npy_name = person_name + ".npy"

	img = fr.load_image_file(file_name)
	enc = fr.face_encodings(img)[0]

	np.save(npy_name, enc)

if __name__ == "__main__":
	fname = sys.argv[1]
	pname = sys.argv[2]

	save_encoding(fname, pname)
