# AudioScreen: an experiment inimage accessibility for blind people
By Michael Curran, NV Access Limited
## Introduction
Audio Screen is an add-on for the [NVDA Screen Reading software](http://www.nvaccess.org/). Audio Screen can allow a blind person to move their finger around a Windows 8+ compatible touch screen, and hear the part of the image under their finger. If a touch screen is not available, the mouse can be moved instead, though this is some what less accurate for the user as mouse movement is relative.

Here a [demonstration of AudioScreen by Michael Curran [mp3 file, 17 mb]](http://www.nvaccess.org/audioScreen/audioScreenDemo20151129.mp3) where he demonstrates the various modes, and uses it to explore a map of Australia, a rainbow, the earth from space, a cartoon house, and a sun set.

As Audio Screen requires NVDA to run, the user will therefore also receive speech feedback such as the name of the control or text, directly under their finger. 

Audio Screen can be seen as an experimental alternative way for blind people to view basic images such as diagrams and maps when no other tactile format is available. 

AudioScreen has two modes of output: "pitch stereo grey" for investigating lines and contours of images (useful for maps and diagrams etc), and "HSV color" for investigating the color variation of images (useful for photographs).

## Pitch Stereo Grey mode

In this mode, AudioScreen represents the image under your finger or the mouse as multiple tones that vary in pitch, volume and stereo position. The idea is based on the vOICe visual-to-auditory mapping system by Peter Meijor. (www.seeingwithsound.com) 
audio Screen strives to provide roughly the same information your finger would for tactile diagrams. You can tell when your finger or mouse moves over a line, both horizontally and vertically. 
For example if your finger crosses a horizontal line as it moves down the screen, you can hear the line move up over your finger. If your finger crosses a vertical line as you move across the screen from left to right, you will hear the line move across your finger from right to left. 
If you leave your finger or mouse stationary at a point on the screen for more than half a second, audioScreen will start sweeping the  audio from left to right, isolating single columns of pixels, providing much more extreme detail of the image to help with detecting patterns etc.

In NVDA 2016.1 or later, If you place more than one finger on the screen at a time, audioScreen will sweep over the image bounded by all your fingers. For example, placing one finger at the top left of a large image, and one fingr at the bottom right, audioScreen will sweep over the entire image.

A part from receiving feedback from touch input or a mouse, you can also instruct audioScreen to sweep over an entire image or control, via its play navigator object command. This will perform multiple vOICe-style sweeps over NVDA's current navigator object.
 
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
* An installed copy of NVDA 2015.4 or higher (NVDA 2016.1 or higher for multi-finger sweeping)
* Windows 8 Operating system or later
* A Windows 8/10 compatible touch screen, otherwise a mouse. 
* Visual feedback for touch must be turned off in Windows. Search for Change Touch Input setting in the start screen, and in that dialog uncheck Show visual feedback when touching the screen.
 
## Download
* Download [AudioScreen 1.4 [NVDA add-on file]](http://www.nvaccess.org/audioScreen/audioScreen-1.4.nvda-addon).
* Download [Example images [zip file]](http://www.nvaccess.org/audioScreen/audioScreenImages.zip).

## Running AudioScreen
After downloading the Audio Screen add-on, with NVDA running simply press enter on the file in Windows Explorer to have NVDA install it for you. Alternatively, you can open Manage Add-ons found under Tools in the NVDA menu, and add it from there. After the add-on is installed, NVDA will ask to be restarted. 

Important: Visual feedback for touch must be turned off in Windows. Search for Change Touch Input setting in the start screen, and in that dialog uncheck Show visual feedback when touching the screen.
 
While NVDA is running with this add-on installed, open an interesting image in full-screen (For example, use Internet Explorer to display one of the example svg files, making sure to maximize it and put it in full-screen with f11). 

AudioScreen is off by default, so turn it on by switching to one of its modes by pressing NVDA+control+a. This toggles between Pitch stereo grey, HSV color, and off.

Now move your finger or mouse around the screen and start listening to the image under your finger. 
As NVDA can also speak controls and text under your finger, viewing an SVG map or diagram works great, as Internet Explorer will allow NVDA to speak the title and or description for any shape your finger moves over, assuming that a title and or description have been properly defined using the title and desc tags appropriately in the SVG file. 

## Commands
### Change Audio Mode (Press NVDA+Control+a)
This command toggles between several modes: 
* pitch stereo grey: for investigating lines and contours of images (useful for maps and diagrams etc)
* HSV color: for investigating the color variation of images (useful for photographs).
* Off [default]: completely disables AudioScreen.

### Play Navigator Object (Press NVDA+alt+a)
This command will play NVDA's current navigator object, by performing multiple vOICe-style stereo sweeps across it.

### Show Settings UI (Press NVDA+shift+a)
This brings up a settings dialog which allows you to change multiple options for audioScreen. The Settings UI can also be launched by choosing AudioScreen... found under Preferences in the NVDA menu.

## Settings

### AudioScreen Mode
Choose the desired mode:
* pitch stereo grey: for investigating lines and contours of images (useful for maps and diagrams etc)
* HSV color: for investigating the color variation of images (useful for photographs).
* Off [default]: completely disables AudioScreen.

### Pitch Stereo Grey settings

#### Reverse brightness
This option allows you to reverse the brightness of the image, so that rather than light being loud and dark being quiet, dark will be loud and light will be quiet. Very useful when playing an image where the foreground objects are darker than the background.

#### Number of columns in stereo field
How wide (in pixels) the image should be. When moving with your finger or the mouse, this is literally how wide the captured image is. For play navigator object, although the full image is fetched, it is compressed or stretched to fit this width.
  
  #### Number of rows (frequencies) 
How tall (in pixels) the image should be. Each row of pixels is represented by a particular frequency. frequencies are spread out logarithmically. When moving with your finger or the mouse, this is literally how tall the captured image is. For play navigator object, although the full image is fetched, it is compressed or stretched to fit this height.
 
 #### Lowest frequency in HZ
 The frequency (in HZ) used for the bottom most row of the image.
 
 #### Highest frequency in HZ
The frequency (in HZ) Used for the top most row of the image.

#### Initial stereo sweep delay in seconds
How long audioScreen should wait (in seconds) to start sweeping an image, after your finger or the mouse has moved.

#### Duration of stereo audio sweep in seconds
How long (in seconds) each sweep should go for. 

#### Number of stereo sweeps
The number of sweeps that should be played once your finger or the mouse has moved, or when the play navigator object command is run.

### HSV Color settings

#### Horizontal length of capture area in pixels
The width (in pixels) of the area under your finger or the mouse captured to detect the color. The color is averaged over this area. Smaller values will give more accurate colors, though can cause you to hear more detail than perhaps seen visually.

#### Vertical length of capture area in pixels
The height (in pixels) of the area under your finger or the mouse captured to detect the color. The color is averaged over this area. Smaller values will give more accurate colors, though can cause you to hear more detail than perhaps seen visually.

#### Lowest frequency (blue) in HZ
The frequency (in HZ) that represents blue. The frequency rises through aqua, green, yellow, orange, to red. As the color spectrum raps around from red back to blue through purple, purples are represented by both the low (blue) frequency and high (red) frequency at differing volume ratios. I.e. A blue-ish purple will be mostly the low (blue) frequency with a small amount of the high (red) frequency).

 
#### highest frequency (red) in HZ
The frequency (in HZ) that represents red. The frequency falls through orange, yellow, green, aqua, to blue. As the color spectrum raps around from blue back to red through purple, purples are represented by both the low (blue) frequency and high (red) frequency at differing volume ratios. I.e. A red-ish purple will be mostly the high (red) frequency with a small amount of the low (blue) frequency.

## Developing and Packaging from source

Clone the AudioScreen repository with the command:
git clone https://www.github.com/nvaccess/audioScreen

[Python 2.7](http://www.python.org/)  is required for building and developing this project.

AudioScreen depends on [libaudioverse](https://www.github.com/camlorn/libaudioverse):
* cd to the audioScreen repository you cloned with git
* Run the command: pip install --ignore-installed -t addon\globalPlugins\audioScreen\deps libaudioverse

### Packaging the NVDA add-on
In the addon directory:
* Edit manifest.ini to set the version of the add-on etc.
* Create a zip file using your favorite zip tool, including both manifest.ini and the globalPlugins directory. It is important that both manifest.ini and globalPlugins be in the root of the zip file, I.e. no interviening directory. The zip file should have a.nvda-addon extension.

## Background
For quite some time now, I have wanted a way to get access as a blind person to maps and basic diagrams with out the hassles of having to produce them in a tactile format. 

Although tactile formats are certainly very useful when they are available, they do have particular drawbacks, such as: 
* They are slow to produce
* Special materials are needed
* Sometimes a special machine is needed
* Rather non-environmental due to paper wastage
* Bulky to carry around
* Only very limited labeling can be included due to space constraints

A few years ago, I stumbled upon a very interesting peace of software called The vOICe, from www.seeingwithsound.com. This software could take images or video from a webcam, and play it to a blind person as audio, making use of pitch, volume and stereo panning. Although the vOICe software is more passive in the sence that it scans from left to right across an entire image, I could see many possibilities of using this image-to-sound mapping concept in a more active way, with the help of a touch screen. 

I should also note that I am aware of other research in to conveying images on touch screens with sound, but none of them that I have seen so far, have yet chosen to try using the vOICe mapping concept. 

When conveying information from one sence modality to another, I believe its very important not to loose information in the process. If you can provide roughly the same or better resolution in the second sence, the brain will have a much easier time of decoding the information. A mapping such as the vOICe I believe certainly gets extremely close to achieving this. 

### Mapping color to sound
Although access to basic diagrams such as maps and other line-based drawings have many practical applications for the blind, there is also an argument that access to color images such as in art or the beauty of the world, has some subjective importance. For example  how colors vary in a rainbow, or a picture of the earth from space. These things are very hard to describe in words.
 