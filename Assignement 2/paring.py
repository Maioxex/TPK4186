import random

def studassparr():
    studasser = ["Inga Bertelsen","Tale Eikenes","Rebecka Fivelstad","Isabelle Galleberg","Elias Søvik Gunnarsson","Lars Magnus Johnsen","Aleksander Karlsen","Frida Karlsen","Monika Luu","Jesper Lybeck","Andrea Omdahl","Quynh-Anh Nguyen Pham","Iver Ringheim","Vebjørn Svare","Long Thanh Vu","Elena Willmann","Klara Louise Moltu Wüstenberg","Gard Drag-Erlandsen","Anders Kristensen"]
    i = 0
    while len(studasser) > 0:
        if len(studasser) == 3:
            print(studasser[0],",",studasser[1]," og ",studasser[2])
            studasser = []
        else:    
            person1 = random.choice(studasser)
            person2 = random.choice(studasser)
            if person1 != person2:
                print(person1,"og",person2)
                studasser.remove(person1)
                studasser.remove(person2)
                i += 1

intervall = [114,120]
def groups():
    group1 = random.randint(intervall[0],intervall[1])
    while True:
        group2 = random.randint(intervall[0],intervall[1])
        if group1 != group2:
            break
    return group2,group1

#studassparr()
print(groups())