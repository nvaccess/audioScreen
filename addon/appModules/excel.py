import globalPlugins.audioScreen
import api
import graphPlayer
import NVDAObjects.window.excelChart as excelChart
from NVDAObjects.window import Window
import config

try:
	from nvdaBuiltin.appModules import excel as BaseAppModule
except ImportError:
	from appModuleHandler import AppModule as BaseAppModule

class ChartPlayer(excelChart.Window):

	def script_playChart(self,gesture):
		focus=api.getFocusObject()
		valuesList=[]
		sampled=focus.excelChartObject.chartType not in (excelChart.xl3DLine, excelChart.xlLine, excelChart.xlLineMarkers, excelChart.xlLineMarkersStacked, excelChart.xlLineMarkersStacked100, excelChart.xlLineStacked, excelChart.xlLineStacked100)
		sr=focus.excelChartObject.seriesCollection()
		if isinstance(focus,excelChart.ExcelChartElementSeries):
			valuesList.append(sr.item(focus.arg1).values)
		else:
			for index in xrange(sr.count):
				valuesList.append(sr.item(index+1).values)
		axes=focus.excelChartObject.axes(excelChart.xlValue)
		playerConf=config.conf['audioScreen_ImagePlayer_pitchStereoGrey']
		focus._graphPlayer=graphPlayer.GraphPlayer(axes.minimumScale,axes.maximumScale,110,3520,playerConf['sweepDuration'],sampled,*valuesList)

	__gestures={
		"kb:shift+NVDA+5":"playChart",
	}

class AppModule(BaseAppModule):

	def chooseNVDAObjectOverlayClasses(self,obj,clsList):
		if isinstance(obj,excelChart.ExcelChart) or isinstance(obj,excelChart.ExcelChartElementBase):
			clsList.insert(0,ChartPlayer)
