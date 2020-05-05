from con_reader import CONreaderVM
import os
import pickle
from patient import Patient
import sys
import os.path
from os import path

class Serializer:

    def __init__(self, root, out):
        self.root = root
        self.out = out

    def save_patient(self, dir, count):
        patientdir = self.root + '\\' + dir
        patientname = os.path.basename(os.path.normpath(patientdir))

        with open(patientdir+"\\meta.txt", "r") as meta:
            patho = meta.readline().split(' ')[1]

        confile = patientdir + '\sa\contours.con'
        cr = CONreaderVM(confile)

        _, _, weight, height, gender= cr.get_volume_data()

        p = Patient(patientname, patho, weight, height, gender, cr) 
        with open(self.out + '\\' + patientname, 'wb') as f:
            pickle.dump(p, f)

        file = open('interruptcount.txt', "w+")
        file.write(count)
        file.close()

    def save_all(self):
        patients = next(os.walk(self.root))[1]
        for patient in patients:
            self.save_patient(patient)

# source és target itt adható meg
# teljes újramentés előtt interruptcount.txt-t törölni kell
root = 'C:\BME\Önálló laboratórium\sample'
out = 'C:\BME'
count = 0

if (path.exists('interruptcount.txt')):
    file = open('interruptcount.txt',"r")
    interruptedcount = int(file.read())
    s = Serializer(root, out)
    patients = next(os.walk(root))[1]
    for patient in patients:
        count += 1
        if (count > interruptedcount):
            s.save_patient(patient, str(count))
    
else:
    s = Serializer(root, out)
    patients = next(os.walk(root))[1]
    for patient in patients:
        count += 1
        s.save_patient(patient, str(count))