from con_reader import CONreaderVM
import os
import pickle
from patient import Patient

class Serializer:

    def __init__(self, root):
        self.root = root

    def save_patient(self, dir):
        patientdir = self.root + '\\' + dir
        patientname = os.path.basename(os.path.normpath(patientdir))

        with open(patientdir+"\\meta.txt", "r") as meta:
            patho = meta.readline().split(' ')[1]

        confile = patientdir + '\sa\contours.con'
        cr = CONreaderVM(confile)

        _, _, weight, height, gender= cr.get_volume_data()

        p = Patient(patientname, patho, weight, height, gender, cr) 
        with open(patientname, 'wb') as f:
            pickle.dump(p, f)

    def save_all(self):
        patients = next(os.walk(self.root))[1]
        for patient in patients:
            self.save_patient(patient)

s = Serializer('C:\BME\Önálló laboratórium\sample')
s.save_all()

