# AudioScreen: an experiment inimage accessibility for blind people
By Michael Curran, NV Access Limited
## Introduction
Audio Screen is an add-on for the [NVDA Screen Reading software](http://www.nvaccess.org/). Audio Screen can allow a blind person to move a finger around a Windows 8+ compatible touch screen, and hear the part of the image under their finger. If a touch screen is not available, the mouse can be moved instead, though this is some what less accurate for the user as mouse movement is relative.

As Audio Screen requires NVDA to run, the user will therefore also receive speech feedback such as the name of the control or text, directly under their finger. 

Audio Screen can be seen as an experimental alternative way for blind people to view basic images such as diagrams and maps when no other tactile format is available. 

AudioScreen has two modes of output: "pitch stereo grey" for investigating lines and contours of images (useful for maps and diagrams etc), and "HSV color" for investigating the color variation of images (useful for photographs).

## Pitch Stereo Grey mode

In this mode, AudioScreen represents the image under your finger as multiple tones that vary in pitch, volume and stereo position. The idea is based on the vOICe visual-to-auditory mapping system by Peter Meijor. (www.seeingwithsound.com) 
audio Screen strives to provide roughly the same information your finger would for tactile diagrams. You can tell when your finger moves over a line, both horizontally and vertically. 
For example if your finger crosses a horizontal line as it moves down the screen, you can hear the line move up over your finger. If your finger crosses a vertical line as you move across the screen from left to right, you will hear the line move across your finger from right to left. 

## HSV Color mode

In this mode, AudioScreen will convey the color (specifically hue, saturation and brightness) of the image under your finger. 

Hue (position in the color spectrum) is represented by a tone at a particular pitch. Currently, the lowest pitch is blue, moving up through green, yellow, orange, red (the highest pitch). As a spectrum is infact a circle, going from red, through purples back to blue, the top (red) pitch fades out, and the bottom (blue) pitch fades back in.

Saturation (how vivid the color is) is represented by brown noise (low random noise). When the color is its most vivid (full saturation) there is no random noise and the spectrum tone can be completely heard. As the saturation decreases towards grey (no saturation) the spectrum tone gets quieter and the random noise gets louder, eventually with only the random noise being heard at no saturation.

Brightness is represented by the over all volume of the sound as a whole.

Some examples:
* black: silence
* White: loud random noise
* Vivid blue: a very low tone
* Vivid yellow: a mid to high tone
* Faded red: a very high tone with some random noise.
* Dark green: a quiet low-mid tone.
* Dark grey: quiet random noise.

## System requirements
* An installed copy of NVDA 2015.4 or higher
* Windows 8 Operating system or later
* A Windows 8/10 compatible touch screen, otherwise a mouse. 

