from __future__ import division

import time
import colorsys
import libaudioverse
from screenBitmap import rgbPixelBrightness

fadeLength=0.1

class ImagePlayer_pitchStereoGrey(object):

	reverseBrightness=False

	def __init__(self,width,height,baseFreq=110,octiveCount=7):
		libaudioverse.initialize()
		self.width=width
		self.height=height
		self.lavSim=libaudioverse.Simulation()
		self.lavWaves=[]
		self.lavPanners=[]
		for x in xrange(self.height):
			lavPanner=libaudioverse.AmplitudePannerNode(self.lavSim)
			#lavPanner.azimuth=((x/self.height)*180)-90
			lavPanner.connect_simulation(0)
			self.lavPanners.append(lavPanner)
			lavWave=libaudioverse.SineNode(self.lavSim)
			lavWave.mul=0
			lavWave.connect(0,lavPanner,0)
			self.lavWaves.append(lavWave)
		self.setFrequences(baseFreq,octiveCount)
		self.lavSim.set_output_device(-1)

	def setFrequences(self,baseFreq,octiveCount):
		for x in xrange(self.height):
			self.lavWaves[x].frequency.value=baseFreq*((2**octiveCount)**(x/self.height))
		self.baseFreq=baseFreq
		self.octiveCount=octiveCount

	def setNewImage(self,imageData,maxBrightness=255):
		with self.lavSim:
			for y in xrange(self.height):
				index=-1-y;
				lavWave=self.lavWaves[index]
				lavPanner=self.lavPanners[index]
				if imageData:
					left=0
					right=0
					brightest=0
					for x in xrange(self.width):
						rRatio=x/self.width
						lRatio=1-rRatio
						px=rgbPixelBrightness(imageData[y][x])
						if self.reverseBrightness:
							px=maxBrightness-px
						brightest=max(brightest,px)
						left+=px*lRatio
						right+=px*rRatio
					lavWave.mul.linear_ramp_to_value(fadeLength,(brightest/maxBrightness)/self.height)
					if left or right:
						lavPanner.azimuth.linear_ramp_to_value(fadeLength,((right-left)/max(left,right))*90)
					else:
						lavPanner.azimuth.linear_ramp_to_value(fadeLength,0)
				else:
					lavWave.mul.linear_ramp_to_value(fadeLength,0)

	def __del__(self):
		self.lavSim.clear_output_device()

class ImagePlayer_hsv(object):

	def __init__(self,width,height,lowFreq=90,highFreq=4000):
		libaudioverse.initialize()
		self.width=width
		self.height=height
		self.lowFreq=lowFreq
		self.highFreq=highFreq
		self.lavSim=libaudioverse.Simulation()
		self.lavWave=libaudioverse.AdditiveSawNode(self.lavSim)
		self.lavWave.mul=0
		self.lavWave.frequency.value=lowFreq
		self.lavWave.connect_simulation(0)
		self.lavWave2=libaudioverse.SineNode(self.lavSim)
		self.lavWave2.mul=0
		self.lavWave2.frequency.value=lowFreq*(highFreq/lowFreq)
		self.lavWave2.connect_simulation(0)
		self.lavNoise=libaudioverse.NoiseNode(self.lavSim)
		self.lavNoise.mul.value=0
		self.lavNoise.noise_type.value=libaudioverse.NoiseTypes.brown
		self.lavNoise.connect_simulation(0)
		self.lavSim.set_output_device(-1)

	def setNewImage(self,imageData,maxBrightness=255):
		r=g=b=0
		if imageData is not None:
			for x in xrange(self.height):
				for y in xrange(self.width):
					px=imageData[y][x]
					r+=px.rgbRed
					g+=px.rgbGreen
					b+=px.rgbBlue
			r/=(self.width*self.height)
			g/=(self.width*self.height)
			b/=(self.width*self.height)
		h,s,v=colorsys.rgb_to_hsv(r/255,g/255,b/255)
		s=1-(10**(1-s)/10)
		iH=1-h
		iH_fromBlue=min(max(iH-0.333,0)/0.666,1)
		iH_imag=min(iH/0.333,1)
		print "h: %s, iH: %s, iH_fromBlue: %s, iH_imag: %s"%(h,iH,iH_fromBlue,iH_imag)
		self.lavWave.mul.value=v*s*iH_imag*0.75/(1+(iH_fromBlue*10))
		self.lavWave.frequency.value=self.lowFreq*((self.highFreq/self.lowFreq)**((2**iH_fromBlue)-1))
		self.lavWave.harmonics=int(1+((((1-abs(iH_fromBlue-0.5))*2)-1)*20))
		print "harmonics: %s"%self.lavWave.harmonics.value
		self.lavWave2.mul.value=v*s*(1-iH_imag)*0.075
		self.lavNoise.mul.value=(1-s)*v*0.4

	def __del__(self):
		self.lavSim.clear_output_device()


