import pickle
import os, cv2
import face_recognition


# Method to train custom classifier to recognize face
def train_classifer(name):
    # Read all the images in custom data-set
    path = os.path.join(os.getcwd()+"/data/"+name+"/")
    print(path)

    images = []
    my_list = os.listdir(path)
    for cl in my_list:
        curImg = cv2.imread(f'{path}/{cl}')
        images.append(curImg)

    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encoded_face = face_recognition.face_encodings(img)[0]
        encodeList.append(encoded_face)
        print(encodeList)

    with open("./data/encoded/"+name+"_encoded", "wb") as fp:
        pickle.dump(encodeList, fp)