import cv2
import numpy as np
import tflite_runtime.interpreter as tflite
from gpiozero import OutputDevice
from signal import pause
import time
import os


filename = "/home/elias/Music/arigato.mp3"
signal1 = OutputDevice(17)
signal2 = OutputDevice(18)#27
signal3 = OutputDevice(22)

interpreter = tflite.Interpreter(model_path="model_unquant.tflite")
interpreter.allocate_tensors()

input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

labels = ["PET", "Other", "Can", "Empty"]

cap = cv2.VideoCapture(0)


state = False

def set_signals(pet, other, can):
    if pet:
        signal1.on()
    else:
        signal1.off()
    
    if other:
        signal2.on()
    else:
        signal2.off()
    
    if can:
        signal3.on()
    else:
        signal3.off()
        
def openn():
    global state
    state = True
    #signal2.value =state
    print("Toggle:", state)

tc1 = 0
to1 = 0
tc2 = 0
to2 = 0
tc3 = 0
to3 = 0
timecooldown=0
imgtagen = False
lidIsOpen = False

PETAmount=0
CanAmount=0
BurnableAmount=0

print ("Start")
set_signals(True, False, True)
while True:
    ret, frame = cap.read()
    
    img2 = cv2.resize(frame, (224,224))
    img = cv2.resize(frame, (224,224))
    #cv2.imshow("Camera3", img)
    img = img.astype(np.float32) / 255.0
    img = np.expand_dims(img, axis=0)
    #cv2.imshow("Camera1", img[0] * 255)
    cv2.imshow("Camera2", frame)
    
    roi = frame[200:750,400:1000]
    roi = cv2.resize(roi, (224,224))
    cv2.imshow("Camera4", roi)
    roi2 = roi
    roi = roi.astype(np.float32) / 255.0
    roi = np.expand_dims(roi, axis=0)

    if imgtagen == False:
        #img2 = cv2.imread(frame)
        #roi = frame[200:750,400:1000]
        #roi = cv2.resize(roi, (224,224))
        #cv2.imwrite("bildtest2.jpg", roi)
        cv2.imwrite("bildrest.jpg", img[0])
        imgtagen = True
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
    interpreter.set_tensor(input_details[0]['index'], roi)
    interpreter.invoke()

    output = interpreter.get_tensor(output_details[0]['index'])
    
    predicted_index = np.argmax(output[0])
    confidence = output[0][predicted_index]
    #print(predicted_index)
    #print(labels[predicted_index])
    print([predicted_index])
    if confidence > 0.5:
        if labels[predicted_index] == "PET":
            if PETAmount < 2:
                print("Pet -> Open door 1")
                tc1= tc1 + 1
            else:
                ##GOR LJUD
                print("Ljud")
        elif labels[predicted_index] == "Other":
            if BurnableAmount < 3:
                print("Other -> Open door 2")
                tc2= tc2 + 1
            else:
                # GOR LJUD
                print("Ljud")
        elif labels[predicted_index] == "Can":
            if CanAmount < 6:
                print("Can -> Open door 3")
                tc3= tc3 + 1
            else:
                # GOR LJUD
                print("Ljud")
        elif lidIsOpen == False:
            set_signals (True,False, True)
            print("Empty")
            timecooldown = timecooldown + 1               
    
    if tc1>30:
        if (labels[predicted_index] == "PET") & (PETAmount < 2):
            set_signals(False, False, True)
        state=False
        #signal2.value=False
        to1 = to1 + 1
        lidIsOpen = True
        if to1>7:
            os.system("mpg123 arigato.mp3")
            tc1=0
            to1=0
            tc2=0
            to2=0
            tc3=0
            to3=0
            timecooldown=0
            set_signals(True, False, True)
            lidIsOpen = False
            PETAmount= PETAmount + 1
            
    if tc2>30:
        if (labels[predicted_index] == "Other") & (BurnableAmount < 4):
            set_signals(True, False, True)
            print("OPPNA")
        state=False
        #signal2.value=False
        to2 = to2 + 1
        lidIsOpen = True
        if to2>20:
            os.system("mpg123 arigato.mp3")
            tc2=0
            to2=0
            tc1=0
            to1=0
            tc3=0
            to3=0
            timecooldown=0
            set_signals(True, False, True)
            lidIsOpen = False
            BurnableAmount = BurnableAmount + 1
        
    if tc3>30:
        if (labels[predicted_index] == "Can") & (CanAmount < 6):
            set_signals(True, False, False)
        state=False
        #signal2.value=False
        to3 = to3 + 1
        lidIsOpen = True
        if to3>7:
            os.system("mpg123 arigato.mp3")
            tc2=0
            to2=0
            tc1=0
            to1=0
            tc3=0
            to3=0
            timecooldown=0
            set_signals(True, False, True)
            lidIsOpen = False
            CanAmount = CanAmount + 1
            
    if timecooldown > 15:
        timecooldown=0
        tc1=0
        to1=0
        tc2=0
        to2=0
        tc3=0
        to3=0
        state=False
        lidIsOpen = False
        
    roi2 = cv2.resize(roi2, (720,720))
    cv2.imshow("Camera5", roi2)            
    print("end","tc1:", tc1, "to1:", to1, " tc2:", tc2, "to2:", to2," tc3:", tc3, "to3:", to3,  "confidence", confidence)
    print("timecooldown" , timecooldown, "Burnable", BurnableAmount)
 