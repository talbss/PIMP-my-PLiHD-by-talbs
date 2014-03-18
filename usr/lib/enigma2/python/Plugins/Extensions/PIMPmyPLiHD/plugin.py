#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-
#######################################################################
#    Configuration tool for PIMP-my-PLiHD-by-talbs skin
#	 based on
#    MyMetrix 
#    Coded by iMaxxx (c) 2013
#    
#
#
#  This plugin is licensed under the Creative Commons
#  Attribution-NonCommercial-ShareAlike 3.0 Unported License.
#  To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-sa/3.0/
#  or send a letter to Creative Commons, 559 Nathan Abbott Way, Stanford, California 94305, USA.
#
#  Alternatively, this plugin may be distributed and executed on hardware which
#  is licensed by Dream Multimedia GmbH.
#
#
#  This plugin is NOT free software. It is open source, you are allowed to
#  modify it (if you keep the license), but it may not be commercially
#  distributed other than under the conditions noted above.
#
#
#######################################################################

from Plugins.Plugin import PluginDescriptor
from Screens.Screen import Screen
from Screens.MessageBox import MessageBox
from Screens.ChoiceBox import ChoiceBox
from Screens.Console import Console
from Screens.Standby import TryQuitMainloop
from Components.ActionMap import ActionMap
from Components.config import config, configfile, ConfigYesNo, ConfigSubsection, getConfigListEntry, ConfigSelection, ConfigNumber, ConfigText, ConfigInteger
from Components.ConfigList import ConfigListScreen
from Components.Label import Label
from os import environ, listdir, remove, rename, system
from skin import parseColor
from Components.Label import Label
import gettext
from Tools.Directories import fileExists, resolveFilename, SCOPE_LANGUAGE, SCOPE_PLUGINS
from shutil import move, copy

#############################################################

config.plugins.PIMPmyPLiHD = ConfigSubsection()
config.plugins.MetrixWeather = ConfigSubsection()
config.plugins.MetrixWeather.refreshInterval = ConfigNumber(default=10)
config.plugins.MetrixWeather.woeid = ConfigNumber(default=640161) #Location (visit metrixhd.info)
config.plugins.MetrixWeather.tempUnit = ConfigSelection(default="Celsius", choices = [
				("Celsius", _("Celsius")),
				("Fahrenheit", _("Fahrenheit"))
				])

config.plugins.PIMPmyPLiHD.PiconsChoice = ConfigSelection(default="normalpicon", choices = [
				("shdpicon", _("SHD (220x132)")),
				("normalpicon", _("Normal (100x60)"))
				])
	
config.plugins.PIMPmyPLiHD.InfobarWeatherWidget = ConfigSelection(default="No", choices = [
				("No", _("No")),
				("WeatherOnly", _("Weather Only")),
				("WeatherAndCity", _("Weather and City Name"))
				])
				
config.plugins.PIMPmyPLiHD.SkinColor = ConfigSelection(default="#00bf9217", choices = [
				("#00F0A30A", _("1-Amber")),
				("#00825A2C", _("2-Brown")),
				("#000050EF", _("3-Cobalt")),
				("#00911d10", _("4-Crimson")),
				("#0018b9ce", _("5-Cyan")),
				("#00a61d4d", _("6-Magenta")),
				("#00A4C400", _("7-Lime")),
				("#006A00FF", _("8-Indigo")),
				("#0070ad11", _("9-Green")),
				("#00008A00", _("10-Emerald")),
				("#0076608A", _("11-Mauve")),
				("#006D8764", _("12-Olive")),
				("#00c3461b", _("13-Orange")),
				("#00F472D0", _("14-Pink")),
				("#00E51400", _("15-Red")),
				("#007A3B3F", _("16-Sienna")),
				("#00647687", _("17-Steel")),
				("#00149baf", _("18-Teal")),
				("#006c0aab", _("19-Violet")),
				("#00bf9217", _("20-Yellow"))
				])

config.plugins.PIMPmyPLiHD.ListBoxColor = ConfigSelection(default="Main Color", choices = [
				("MainColor", _("Main Color")),
				("Black", _("Black"))
				])				
				
def main(session, **kwargs):
	session.open(PIMPmyPLiHD)

def Plugins(**kwargs):
	return PluginDescriptor(name="PIMP my PLiHD", description=_("Configuration tool for PIMP-my-PLiHD-by-talbs skin"), where = PluginDescriptor.WHERE_PLUGINMENU, icon="plugin.png", fnc=main)


#######################################################################


class PIMPmyPLiHD(ConfigListScreen, Screen):
	skin = """
<screen name="PIMPmyPLiHD" position="40,40" size="1200,640" flags="wfNoBorder" backgroundColor="#40000000">
  <eLabel font="Regular; 20" foregroundColor="#00ffffff" backgroundColor="#40000000" halign="left" position="37,605" size="250,33" text="Cancel" transparent="1" />
  <eLabel font="Regular; 20" foregroundColor="#00ffffff" backgroundColor="#40000000" halign="left" position="337,605" size="250,33" text="Save" transparent="1" />
  <eLabel font="Regular; 20" foregroundColor="#00ffffff" backgroundColor="#40000000" halign="left" position="637,605" size="250,33" text="Reboot" transparent="1" />
  <eLabel font="Regular; 20" foregroundColor="#00ffffff" backgroundColor="#40000000" halign="left" position="937,605" size="250,33" text="Information" transparent="1" />
 <widget name="config" position="21,77" scrollbarMode="showOnDemand" size="590,506" transparent="1" />
  <eLabel position="20,15" size="348,50" text="PIMPmyPLiHD configuration panel" font="Regular; 30" valign="center" transparent="1" backgroundColor="#40000000" />
  <eLabel position="920,600" size="5,40" backgroundColor="#000000ff" />
  <eLabel position="620,600" size="5,40" backgroundColor="#00ffff00" />
  <eLabel position="320,600" size="5,40" backgroundColor="#0000ff00" />
  <eLabel position="20,600" size="5,40" backgroundColor="#00ff0000" />
</screen>
"""

	def __init__(self, session, args = None, picPath = None):
		Screen.__init__(self, session)
		self.session = session
		
		fontlist = []
		self.myfontpath = "/usr/share/enigma2/PIMP-my-PLiHD-by-talbs/fonts/"
		self.openplifontpath = "/usr/share/fonts/"
		fontlist.append(('nmsbd.ttf', 'nmsbd (default PLiHD font)'))
		for myfonts in listdir(self.myfontpath):
			if myfonts != "meteocons.ttf":
				if myfonts.find('.ttf') !=-1:
					myfontsname = myfonts.replace('.ttf', '')
					fontlist.append((self.myfontpath + myfonts, myfontsname))
		config.plugins.PIMPmyPLiHD.FontSelection = ConfigSelection(default="nmsbd (default PLiHD font)",choices=fontlist)
		
		self.SkinDefault = "/usr/share/enigma2/PIMP-my-PLiHD-by-talbs/default_skin.xml"
		self.SkinDefaultTmp = self.SkinDefault + ".TMP"
		self.SkinFinal = "/usr/share/enigma2/PIMP-my-PLiHD-by-talbs/skin.xml"
		list = []
		list.append(getConfigListEntry(_("Skin Configuration: "), ))
		list.append(getConfigListEntry(_("   Main Color"), config.plugins.PIMPmyPLiHD.SkinColor))
		list.append(getConfigListEntry(_("   ListBox Selection Color"), config.plugins.PIMPmyPLiHD.ListBoxColor))
		list.append(getConfigListEntry(_("   Picons Size"), config.plugins.PIMPmyPLiHD.PiconsChoice))
		list.append(getConfigListEntry(_("   Font"), config.plugins.PIMPmyPLiHD.FontSelection))
		list.append(getConfigListEntry(_(" "), ))
		list.append(getConfigListEntry(_("Weather Widget Configuration:"), ))
		list.append(getConfigListEntry(_("   Display in second infobar"), config.plugins.PIMPmyPLiHD.InfobarWeatherWidget))		
		list.append(getConfigListEntry(_("   City ID"), config.plugins.MetrixWeather.woeid))
		list.append(getConfigListEntry(_("   Temperature Unit"), config.plugins.MetrixWeather.tempUnit))
		list.append(getConfigListEntry(_("   Refresh Interval (min)"), config.plugins.MetrixWeather.refreshInterval))

		ConfigListScreen.__init__(self, list)
		self["actions"] = ActionMap(["OkCancelActions","DirectionActions", "InputActions", "ColorActions"], {"left": self.keyLeft,"down": self.keyDown,"up": self.keyUp,"right": self.keyRight,"red": self.exit,"yellow": self.reboot, "blue": self.showInfo, "green": self.save,"cancel": self.exit}, -1)

	def keyLeft(self):	
		ConfigListScreen.keyLeft(self)	


	def keyRight(self):
		ConfigListScreen.keyRight(self)

	
	def keyDown(self):
		#print "key down"
		self["config"].instance.moveSelection(self["config"].instance.moveDown)

		
	def keyUp(self):
		#print "key up"
		self["config"].instance.moveSelection(self["config"].instance.moveUp)

	
	def reboot(self):
		restartbox = self.session.openWithCallback(self.restartGUI,MessageBox,_("Do you really want to restart Enigma2 now?"), MessageBox.TYPE_YESNO)
		restartbox.setTitle(_("Restart GUI"))
		
	def showInfo(self):
		self.session.open(MessageBox, _("PIMP-my-PLiHD-by-talbs\n\n- To get your MetrixWeather City ID visit\nhttp://open-store.net/?page=metrixweather\n\n- To use your own font, send it to\n/usr/share/enigma2/PIMP-my-PLiHD-by-talbs/fonts/ "), MessageBox.TYPE_INFO)

	def save(self):
	
		for x in self["config"].list:
			if len(x) > 1:
        			x[1].save()
			else:
       				pass
       			
		###########READING DATA FILES
		try:

			skinSearchAndReplace = []
			skinSearchAndReplace.append(['#00bf9217', config.plugins.PIMPmyPLiHD.SkinColor.value ])
			if config.plugins.PIMPmyPLiHD.FontSelection.value != "nmsbd.ttf":
				skinSearchAndReplace.append(['nmsbd.ttf', config.plugins.PIMPmyPLiHD.FontSelection.value ])
			if config.plugins.PIMPmyPLiHD.ListBoxColor.value == "Black":
				skinSearchAndReplace.append(['<color name="ListboxSelectedBackground" color="selectedFG"/>', '<color name="ListboxSelectedBackground" color="black"></color>' ])
				skinSearchAndReplace.append(['<color name="ListboxSelectedForeground" color="white"/>', '<color name="ListboxSelectedForeground" color="selectedFG"></color>' ])
			if config.plugins.PIMPmyPLiHD.PiconsChoice.value == "shdpicon":
				skinSearchAndReplace.append(['<panel name="InfoBarTemplate"/>', '<panel name="InfoBarTemplateSHDPicon"/>' ])
			if config.plugins.PIMPmyPLiHD.InfobarWeatherWidget.value == "WeatherOnly":
				skinSearchAndReplace.append(['<panel name="MetrixNoWeatherTemplate"/>', '<panel name="MetrixWeatherTemplate"/>' ])
			if config.plugins.PIMPmyPLiHD.InfobarWeatherWidget.value == "WeatherAndCity":
				skinSearchAndReplace.append(['<panel name="MetrixNoWeatherTemplate"/>', '<panel name="MetrixWeatherTemplate"/>' ])
				skinSearchAndReplace.append(['<panel name="MetrixWeatherNoCityTemplate"/>', '<panel name="MetrixWeatherCityTemplate"/>' ])		

			SkinDefaultFile = open(self.SkinDefault, "r")
			SkinDefaultLines = SkinDefaultFile.readlines()
			SkinDefaultFile.close()
			PimpedLines = []
			for Line in SkinDefaultLines:
				for item in skinSearchAndReplace:
					Line = Line.replace(item[0], item[1])
				PimpedLines.append(Line)
				
			TmpFile = open(self.SkinDefaultTmp, "w")
			for Lines in PimpedLines:
				TmpFile.writelines(Lines)
			TmpFile.close()
			move(self.SkinDefaultTmp, self.SkinFinal)
			
		except:
			self.session.open(MessageBox, _("Error creating Skin!"), MessageBox.TYPE_ERROR)

		configfile.save()
		restartbox = self.session.openWithCallback(self.restartGUI,MessageBox,_("GUI needs a restart to apply a new skin.\nDo you want to Restart the GUI now ?"), MessageBox.TYPE_YESNO)
		restartbox.setTitle(_("Restart GUI"))

	def restartGUI(self, answer):
		if answer is True:
			configfile.save()
			self.session.open(TryQuitMainloop, 3)
		else:
			self.close()
			
	def exit(self):
		for x in self["config"].list:
			if len(x) > 1:
					x[1].cancel()
			else:
       				pass
		self.close()
