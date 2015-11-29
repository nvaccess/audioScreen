import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__),'deps'))

import ctypes
import globalPluginHandler
import touchHandler
import screenBitmap
import screenExplorer
import textInfos
import ui
from . import imagePlayer

class ScreenExplorerWithAudio(screenExplorer.ScreenExplorer):

	def __init__(self,gp):
		self.gp=gp
		super(ScreenExplorerWithAudio,self).__init__()

	def moveTo(self,x,y,new=False,unit=textInfos.UNIT_LINE):
		super(ScreenExplorerWithAudio,self).moveTo(x,y,new,unit)
		self.gp.playAt(x,y)

class GlobalPlugin(globalPluginHandler.GlobalPlugin):

	audioScreenModes=[
		(_("Off"),None),
		(_("pitch stereo grey"),imagePlayer.ImagePlayer_pitchStereoGrey,32,16),
		(_("HSV Color"),imagePlayer.ImagePlayer_hsv,3,3),
	]

	def __init__(self):
		self.curAudioScreenMode=0
		self.imagePlayer=self.screenBitmap=None
		if touchHandler.handler:
			touchHandler.handler.screenExplorer=ScreenExplorerWithAudio(self)
		super(GlobalPlugin,self).__init__()

	def playAt(self,x,y):
		if not self.imagePlayer: return
		width=self.screenBitmap.width
		height=self.screenBitmap.height
		x=x-(width/2)
		y=y-(height/2)
		buffer=self.screenBitmap.captureImage(x,y,width,height)
		self.imagePlayer.setNewImage(buffer)

	def stopPlaying(self):
		if self.imagePlayer: self.imagePlayer.setNewImage(None)

	def event_mouseMove(self,obj,nextHandler,x=None,y=None):
		nextHandler()
		if touchHandler.handler: return
		self.playAt(x,y)

	def script_toggleAudioScreen(self,gesture):
		self.curAudioScreenMode=(self.curAudioScreenMode+1)%len(self.audioScreenModes)
		modeInfo=self.audioScreenModes[self.curAudioScreenMode]
		if modeInfo[1] is None:
			self.imagePlayer=self.screenBitmap=None
			ui.message(_("AudioScreen off"))
		else:
			self.imagePlayer=modeInfo[1](*modeInfo[2:])
			self.screenBitmap=screenBitmap.ScreenBitmap(modeInfo[2],modeInfo[3])
			inputType=_("touch input") if touchHandler.handler else _("mouse input")
			ui.message(_("AudioScreen mode {mode}, {inputType}").format(mode=modeInfo[0],inputType=inputType))
	script_toggleAudioScreen.__doc__="Switches audioScreen on and off"

	def script_toggleBrightness(self,gesture):
		if not self.imagePlayer:
			ui.message(_("Audio screen currently off"))
			return
		rb=not self.imagePlayer.reverseBrightness
		if not rb:
			ui.message("Dark on light")
		else:
			ui.message("Light on dark")
		self.imagePlayer.reverseBrightness=rb
	script_toggleBrightness.__doc__="Toggles between light on dark, and dark on light"

	def script_hoverUp(self,gesture):
		self.stopPlaying()

	__gestures={
		"ts:hoverUp":"hoverUp",
		"kb:NVDA+Shift+a":"toggleBrightness",
		"kb:NVDA+Control+a":"toggleAudioScreen",
	}

 