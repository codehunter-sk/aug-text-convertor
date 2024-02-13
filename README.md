# aug-text-convertor
Augmentedly written text convertor

A working python GUI that will get its input from a video source (preferably system camera) and allow you to augmentedly write text with a (light)green object and convert it into digital text and save it.

Various libraries must be installed. They are given in requirements.txt.
Tesseract-OCR engine must be downloaded and stored appropriately or the path must be changed in "code_vrecog.py". (This is only if you are going to use Tesseract to detect the text, if you feel Keras-OCR is enough, then pls comment the necessary code lines.)

**Usage Instructions**
- Once a display screen is open, say your using a mouse, hold left click to write and release to stop writing
- Right click or press "c" to clear the screen
- Press "s" to save plain image
- Press "d" to detect with Keras-OCR
- Press "l" to detect with Tesseract-OCR
- Press "q" to quit the window
- Make sure to use green pen, or change the colour range as required

App Screens and Outputs:

![image](https://user-images.githubusercontent.com/93638366/183695120-be997456-ced6-417b-b246-4b986179d075.png)


![image](https://user-images.githubusercontent.com/93638366/183695462-bd00ea62-e1ea-4512-b232-81a0c0b62c51.png)


![image](https://github.com/codehunter-sk/aug-text-convertor/assets/93638366/86df2dac-39f2-49ae-bea1-963ef89c2628)


![image](https://user-images.githubusercontent.com/93638366/183696211-a78fb9fd-403e-4b06-a7d9-443dd2f5f238.png)
