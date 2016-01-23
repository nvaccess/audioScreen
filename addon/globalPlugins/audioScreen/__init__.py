import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__),'../../deps'))
sys.path.append(os.path.join(os.path.dirname(__file__),'../../'))

import ctypes
import wx
import libaudioverse
import config
from gui.settingsDialogs import SettingsDialog
import gui
import globalPluginHandler
import touchHandler
import globalCommands
import api
import screenBitmap
import textInfos
import ui
import imagePlayer

class AudioScreenDialog(SettingsDialog):
	title=_("AudioScreen settings")

	def __init__(self,parent,plugin):
		self.plugin=plugin
		super(AudioScreenDialog,self).__init__(parent)

	def makeSettings(self,settingsSizer):
		generalSizer=wx.StaticBoxSizer(wx.StaticBox(self,wx.ID_ANY,_("General")),wx.VERTICAL)
		modeChoiceSizer=wx.BoxSizer(wx.HORIZONTAL)
		modeChoiceSizer.Add(wx.StaticText(self,wx.ID_ANY,_("Mode")))
		self.modeChoice=wx.Choice(self,wx.ID_ANY,choices=[x[0] for x in self.plugin.audioScreenModes])
		self.modeChoice.SetSelection(self.plugin.curAudioScreenMode)
		modeChoiceSizer.Add(self.modeChoice)
		generalSizer.Add(modeChoiceSizer)
		settingsSizer.Add(generalSizer)
		modesSizer=wx.BoxSizer(wx.HORIZONTAL)
		self.modeControls=[]
		for mode in self.plugin.audioScreenModes[1:]:
			modeSizer=wx.StaticBoxSizer(wx.StaticBox(self,wx.ID_ANY,mode[0]),wx.VERTICAL)
			modeConf=config.conf["audioScreen_%s"%mode[1].__name__]
			for v in mode[2]:
				if v[1]=='boolean':
					control=wx.CheckBox(self,wx.ID_ANY,label=v[3])
					control.SetValue(modeConf[v[0]])
					modeSizer.Add(control)
				else:
					fieldSizer=wx.BoxSizer(wx.HORIZONTAL)
					fieldSizer.Add(wx.StaticText(self,wx.ID_ANY,v[3]))
					control=wx.TextCtrl(self,wx.ID_ANY)
					control.SetValue(str(modeConf[v[0]]))
					fieldSizer.Add(control)
					modeSizer.Add(fieldSizer)
				self.modeControls.append(control)
			modesSizer.Add(modeSizer)
		settingsSizer.Add(modesSizer)

	def postInit(self):
		self.modeChoice.SetFocus()

	def onOk(self,evt):
		modeControlIndex=0
		for mode in GlobalPlugin.audioScreenModes[1:]:
			modeConf=config.conf["audioScreen_%s"%mode[1].__name__]
			for v in mode[2]:
				control=self.modeControls[modeControlIndex]
				if v[1]=='boolean':
					modeConf[v[0]]=control.IsChecked()
				else:
					try:
						value=float(control.Value) if v[1]=='float' else int(control.Value)
					except:
						value=v[2]
					modeConf[v[0]]=value
				modeControlIndex+=1
		curMode=self.modeChoice.GetSelection()
		self.plugin.setMode(curMode)
		super(AudioScreenDialog,self).onOk(evt)

class GlobalPlugin(globalPluginHandler.GlobalPlugin):

	audioScreenModes=[
		(_("Off"),None),
		(_("pitch stereo grey"),imagePlayer.ImagePlayer_pitchStereoGrey,[
			("reverseBrightness","boolean",False,_("Reverse brightness (useful for white on black)")),
			("width","integer",176,_("Number of columns in stereo field")),
			("height","integer",64,_("Number of rows (frequencies)")),
			("lowFreq","float",500.0,_("Lowest frequency in HZ")),
			("highFreq","float",5000.0,_("highest frequency in HZ")),
			("sweepDelay","float",0.5,_("Initial stereo sweep Delay in seconds")), 
			("sweepDuration","float",4.0,_("Duration of stereo audio sweep in seconds")), 
			("sweepCount","integer",4,_("Numver of stereo sweeps")), 
		]),
		(_("HSV Color"),imagePlayer.ImagePlayer_hsv,[
			("width","integer",2,_("Horizontal length of   capture area in pixels")),
			("height","integer",2,_("Vertical length of capture area in pixels")),
			("lowFreq","float",90.0,_("Lowest frequency (blue) in HZ")),
			("highFreq","float",5760,_("highest frequency (red) in HZ")),
		]),
	]
	for mode in audioScreenModes[1:]:
		config.conf.spec["audioScreen_%s"%mode[1].__name__]={v[0]:"%s(default=%s)"%v[1:3] for v in mode[2]}

	def __init__(self):
		libaudioverse.initialize()
		self._lastRect=None
		self.curAudioScreenMode=0
		self.imagePlayer=self.screenBitmap=None
		item = gui.mainFrame.sysTrayIcon.preferencesMenu.Append(wx.ID_ANY,_("&AudioScreen..."),_("AudioScreen"))
		gui.mainFrame.sysTrayIcon.Bind(wx.EVT_MENU, self.script_showUI, item)
		super(GlobalPlugin,self).__init__()

	def terminate(self):
		libaudioverse.shutdown()

	def playPoint(self,x,y):
		if not self.imagePlayer: return
		screenWidth,screenHeight=api.getDesktopObject().location[2:]
		width=self.screenBitmap.width
		height=self.screenBitmap.height
		x=x-(width/2)
		y=y-(height/2)
		self.playRect(x,y,width,height)

	def playRect(self,x,y,width,height,detailed=False,forceRestart=False):
		if not self.imagePlayer: return
		rect=(x,y,width,height)
		if not forceRestart and rect==self._lastRect:
			return
		self._lastRect=rect
		buffer=self.screenBitmap.captureImage(x,y,width,height)
		self.imagePlayer.setNewImage(buffer,detailed=detailed)

	def stopPlaying(self):
		if self.imagePlayer: self.imagePlayer.setNewImage(None)

	def event_mouseMove(self,obj,nextHandler,x=None,y=None):
		nextHandler()
		if touchHandler.handler: return
		self.playPoint(x,y)

	def setMode(self,modeID,report=False):
		self.curAudioScreenMode=modeID
		modeInfo=self.audioScreenModes[modeID]
		if self.imagePlayer:
			imagePlayer=self.imagePlayer
			self.imagePlayer=None
			imagePlayer.terminate()
		self.screenBitmap=None
		if modeInfo[1] is None:
			if report: ui.message(_("AudioScreen off"))
		else:
			modeConf={k:v for k,v in config.conf["audioScreen_%s"%modeInfo[1].__name__].iteritems()}
			self.imagePlayer=modeInfo[1](**modeConf)
			self.screenBitmap=screenBitmap.ScreenBitmap(self.imagePlayer.width,self.imagePlayer.height)
			if report:
				inputType=_("touch input") if touchHandler.handler else _("mouse input")
				ui.message(_("AudioScreen mode {mode}, {inputType}").format(mode=modeInfo[0],inputType=inputType))

	def script_toggleAudioScreen(self,gesture):
		self.setMode((self.curAudioScreenMode+1)%len(self.audioScreenModes),report=True)
	script_toggleAudioScreen.__doc__="Toggles AudioScreen   between several modes"

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

	def script_hover(self,gesture):
		preheldTracker=getattr(gesture,'preheldTracker',None)
		if preheldTracker:
			xList=[tracker.x for tracker in preheldTracker.childTrackers]
			xList.append(preheldTracker.x)
			xList.append(gesture.tracker.x)
			yList=[tracker.y for tracker in preheldTracker.childTrackers]
			yList.append(preheldTracker.y)
			yList.append(gesture.tracker.y)
			minX=min(xList)
			maxX=max(xList)
			minY=min(yList)
			maxY=max(yList)
			self.playRect(minX,minY,maxX-minX,maxY-minY,detailed=True)
		else:
			self.playPoint(gesture.tracker.x,gesture.tracker.y)
		script=globalCommands.commands.getScript(gesture)
		if script: script(gesture)
	script_hover.__doc__=_("Plays the image under your fingers")

	def script_hoverUp(self,gesture):
		self.stopPlaying()
		script=globalCommands.commands.getScript(gesture)
		if script: script(gesture)
	script_hoverUp.__doc__=_("Stops audioScreen playback")

	def script_playNavigatorObject(self,gesture):
		if not self.imagePlayer:
			ui.message(_("AudioScreen disabled"))
			return
		obj=api.getNavigatorObject()
		x,y,w,h=obj.location
		self.playRect(x,y,w,h,detailed=True,forceRestart=True)
	script_playNavigatorObject.__doc__=_("Plays the image of the current navigator object")

	def script_showUI(self,gesture):
		wx.CallAfter(gui.mainFrame._popupSettingsDialog,AudioScreenDialog,self)

	__gestures={
		"ts:hoverDown":"hover",
		"ts:hold+hoverDown":"hover",
		"ts:hover":"hover",
		"ts:hold+hover":"hover",
		"ts:hoverUp":"hoverUp",
		"ts:hold+hoverUp":"hover",
		"kb:NVDA+Shift+a":"showUI",
		"kb:NVDA+Control+a":"toggleAudioScreen",
		"kb:alt+NVDA+a":"playNavigatorObject",
	}
