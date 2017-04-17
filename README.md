# picamera-stopmotion

Simple program to drive the PiCamera module during a stop-motion capture.

The inputs are read from ` cmd = input('?>') ` 

- preview
  - `<Enter>` take a picture
  - `++` set the preview to full opaque
  - `--` set the preview to full-transparecy 
  - `-`  decrease the preview opacity ( alpha )  
  - `+`  increase the preview opacity ( alpha ) 
- image effects
  - `F` next effect
  - `f` previous effect
- exposure mode 
  - `X` next mode
  - `x` previous mode
- White Balance Mode ( AWB ) 
  - `W` next mode
  - `w` previous mode

