# AUTOMATIC-ACCESS-SECURITY-SYSTEM-PROJECT
# This project combine between 4 technologies:
#     * Deep learning (face-recognition)
#     * Operating System Automation
#     * Linux os administration (FTP)
#     * Electronics by using ARDUINO Card 


* To build the prototype of this project :
      - I used a camera for face detection and recognition based on Deep Learning technology (face_recognition).
      - I used for Electronics ARDUINO CARD, 2 LEDs, SERVO motor, BreadBoard, Push Button, Resistors, wires.
      - Linux administration by configuring (FTP) protocol in centOS server machine.
      - Virtualisation by using VirtualBox software, where we set centOS server virtual machine.
      - Automation of OS by creating, adding, copying, renaming ... files and directories via python programing language.
      - ESP8266 to creat a local network.
* NOTE:
  - All the electronic components used in this prototype are programed with Python not C Arduino, by using pyfirmata library.
How this system work?
  This system works in two main phases: 
  * Phase 1: traitement of known person 
      * the local data-base, in my situation I consider my personal laptop as a local data-base, contains the pictures of diffrent people who are known for the               system of this building, once the camera recognise a person:
              1- LED1 who exists in the entry of the door lights up for 10 seconds.
              2- Alarm System inside the building broadcast 3 times a vocal message in our case "HANANE ZARKA is in front of the door"
              3- The door of the building opens to the user automatically by using SERVO motor.
              4- LED2 who exists inside the building light up for 10 seconds.
              5- The door of the building will be closed automatically.
  * Phase 2: traitment of unknown person
      * In case the camera don't recognise the user, that's mean the pictures of this user don't exists in the local data-base, the process of the functionality           in this case:
              1- Alarm system inside the building broadcast 3 times a vocal message in our case "UNKNOWN person in the door".
              2- The system will interact with the user by allowing him to enter his personal informations, like 1st name, last name, age, physical address,                        email, Profession..., those informations will be stored in a file, who's will be named by the name of this user, the camera will take a picture                    to this user and name it with his name.
              3- The file who contains the user informations and the taken picture will be stored in the local data-base and send a copy of them to the FTP                        server.
              4- LED1 who exists in the entry of the door lights up for 10 seconds.
              5- The door will not open automatically to the unknown persons, the access will be allowed from the inside of the building by pressing the push                      button, after 10 seconds the door will be closed automatically.
              6- LED2 who exists inside the building light up for 10 seconds.
              
              
