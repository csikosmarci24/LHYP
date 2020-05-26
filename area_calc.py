from patient import Patient
from con_reader import CONreaderVM
import pickle
import os.path
from os import path
import glob
import csv

def check_if_inside(pointX, pointY, conpoints):
    for pointA in conpoints:
        if(pointA[0] == pointX & pointA[1] > pointY):
            for pointB in conpoints:
                if(pointB[0] == pointX & pointB[1] < pointY):
                    for pointC in conpoints:
                        if(pointC[0] > pointX & pointC[1] == pointY):
                            for pointD in conpoints:
                                if(pointD[0] < pointX & pointD[1] == pointY):
                                    return True
    return False

def calc_ln(con):
    area = 0
    for mode in con:
        if mode == 'ln':
            conpoints = con[mode]
            points = []
            for point in conpoints:
                x = point[0].astype(int)
                y = point[1].astype(int)
                points.append([x, y])
            for i in range(200):
                for j in range(200):
                    if(check_if_inside(i, j, points)==True):
                        area+=1
    return area

def calc_lp(con):
    area = 0
    rn_points = []
    for mode in con:
        if mode == 'lp':
            lp_points = con[mode]
        if mode == 'rn':
            rn_points = con[mode]
    points = []
    for point in lp_points:
        x = point[0].astype(int)
        y = point[1].astype(int)
        points.append([x, y])
    if len(rn_points) != 0:
        for point in rn_points:
            x = point[0].astype(int)
            y = point[1].astype(int)
            points.append([x, y])
    for i in range(200):
        for j in range(200):
            if(check_if_inside(i, j, points)==True):
                area+=1

    if len(rn_points) != 0:
        right_vent = 0
        points = []
        for point in rn_points:
            x = point[0].astype(int)
            y = point[1].astype(int)
            points.append([x, y])
        for i in range(200):
            for j in range(200):
                if(check_if_inside(i, j, points)==True):
                    right_vent+=1
        area-=right_vent
    return area              

patients = glob.glob("C:\BME\Önálló laboratórium\csikos_data\\*")
pCount = 0
invalidCount = 0
for patient in patients:
    pCount+=1
    print("Patient: {}".format(pCount))
    pickleFile = open(patient, "rb")
    pat = pickle.load(pickleFile)
    pickleFile.close()
    contours = pat.contours.get_hierarchical_contours()
    if(pat.pathology == 'HCM'):
        patho = 1
    else:
        patho = 0

    slicesToMove = []
    for slc in contours:
        slicesToMove.append(slc)
        break
    lastSlice = slicesToMove[0]
    for slc in contours:
        lastSlice = slc
    sliceCount = lastSlice + 1 - slicesToMove[0]
    if (sliceCount % 2 == 0):
        slicesToMove.append(int(slicesToMove[0] + (sliceCount / 2)))
    else:
        slicesToMove.append(int(slicesToMove[0] + (sliceCount / 2) - 0.5))
    slicesToMove.append(lastSlice)

    row = []
    for slc in contours:
        if slc in slicesToMove:
            for frm in contours[slc]:
                for mode in contours[slc][frm]:
                    if mode == 'lp':
                        lastFrame = contours[slc][frm]
            row.append(calc_ln(lastFrame))
            row.append(calc_lp(lastFrame))
    row.append(patho)

    invalid = True
    for element in row:
        if element != 0:
            invalid = False
    
    if (invalid == True):
        print("Invalid data!")
        invalidCount+=1
    else:
        with open('data.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(row)
        print("Done")

print("Number of invalid patients: {}".format(invalidCount))