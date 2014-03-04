#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-
#######################################################################
#
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

#############################################################

config.plugins.PIMPmyPLiHD = ConfigSubsection()
config.plugins.MetrixWeather = ConfigSubsection()
config.plugins.MetrixWeather.refreshInterval = ConfigNumber(default=10)
config.plugins.MetrixWeather.woeid = ConfigNumber(default=640161) #Location (visit metrixhd.info)
config.plugins.MetrixWeather.tempUnit = ConfigSelection(default="Celsius", choices = [
				("Celsius", _("Celsius")),
				("Fahrenheit", _("Fahrenheit"))
				])

config.plugins.PIMPmyPLiHD.PiconsChoice = ConfigSelection(default="infobar-shd-picon", choices = [
				("infobar-shd-picon", _("SHD (220x132)")),
				("infobar-picon", _("Normal (100x60)"))
				])
	
config.plugins.PIMPmyPLiHD.InfobarWeatherWidget = ConfigSelection(default="no-weather", choices = [
				("weather", _("Yes")),
				("no-weather", _("No"))
				])

config.plugins.PIMPmyPLiHD.InfobarWeatherCityWidget = ConfigSelection(default="no-city", choices = [
				("city", _("Yes")),
				("no-city", _("No"))
				])
			
				
config.plugins.PIMPmyPLiHD.SkinColor = ConfigSelection(default="#0018b9ce", choices = [
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
			
config.plugins.PIMPmyPLiHD.FontSelection = ConfigSelection(default="nmsbd.ttf", choices = [
				("nmsbd.ttf", _("nmsbd (default PLiHD font)")),
				("/usr/share/enigma2/PIMP-my-PLiHD-by-talbs/fonts/DejaVuSansCondensed.ttf", _("DejaVuSansCondensed")),
				("/usr/share/enigma2/PIMP-my-PLiHD-by-talbs/fonts/DejaVuSansCondensedBold.ttf", _("DejaVuSansCondensedBold")),
				("/usr/share/enigma2/PIMP-my-PLiHD-by-talbs/fonts/DejaVuSansCondensedBoldItalic.ttf", _("DejaVuSansCondensedBoldItalic")),
				("/usr/share/enigma2/PIMP-my-PLiHD-by-talbs/fonts/DroidSans.ttf", _("DroidSans")),
				("/usr/share/enigma2/PIMP-my-PLiHD-by-talbs/fonts/KsBold.ttf", _("KsBold")),
				("/usr/share/enigma2/PIMP-my-PLiHD-by-talbs/fonts/KsBoldItalic.ttf", _("KsBoldItalic")),
				("/usr/share/enigma2/PIMP-my-PLiHD-by-talbs/fonts/Custom.ttf", _("Custom"))
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
  <eLabel font="Regular; 20" foregroundColor="#00ffffff" backgroundColor="#40000000" halign="left" position="335,605" size="250,33" text="Save" transparent="1" />
    <eLabel font="Regular; 20" foregroundColor="#00ffffff" backgroundColor="#40000000" halign="left" position="642,605" size="250,33" text="Reboot" transparent="1" />
 <widget name="config" position="21,77" scrollbarMode="showOnDemand" size="590,506" transparent="1" />
  <eLabel position="20,15" size="348,50" text="PIMPmyPLiHD" font="Regular; 40" valign="center" transparent="1" backgroundColor="#40000000" />
  <eLabel position="223,18" size="349,50" text="Setup" foregroundColor="#00ffffff" font="Regular; 30" valign="center" backgroundColor="#40000000" transparent="1" halign="left" />
  <eLabel position="625,600" size="5,40" backgroundColor="#00ffff00" />
  <eLabel position="320,600" size="5,40" backgroundColor="#0000ff00" />
  <eLabel position="20,600" size="5,40" backgroundColor="#00ff0000" />
  #<widget name="metrixVersion" position="987,11" size="200,30" backgroundColor="#40000000" foregroundColor="#00ffffff" transparent="1" halign="right" />
</screen>
"""

	def __init__(self, session, args = None, picPath = None):
		self.skin_lines = []
		Screen.__init__(self, session)
		self.session = session
		self.SkinTemplate = "/usr/share/enigma2/PIMP-my-PLiHD-by-talbs/skin_templates.xml"
		self.SkinDefault = "/usr/share/enigma2/PIMP-my-PLiHD-by-talbs/skinparts/skin_default.xml"
		self.SkinFinal = "/usr/share/enigma2/PIMP-my-PLiHD-by-talbs/skin.xml"
		self.daten = "/usr/share/enigma2/PIMP-my-PLiHD-by-talbs/skinparts/"
		list = []
		list.append(getConfigListEntry(_("Main Color"), config.plugins.PIMPmyPLiHD.SkinColor))
		list.append(getConfigListEntry(_("ListBox Selection Color"), config.plugins.PIMPmyPLiHD.ListBoxColor))
		list.append(getConfigListEntry(_("Picons Size"), config.plugins.PIMPmyPLiHD.PiconsChoice))
		list.append(getConfigListEntry(_("Font"), config.plugins.PIMPmyPLiHD.FontSelection))
		list.append(getConfigListEntry(_(" "), ))
		list.append(getConfigListEntry(_("Show Weather in second infobar"), config.plugins.PIMPmyPLiHD.InfobarWeatherWidget))		
		list.append(getConfigListEntry(_("Show City Name in Weather Widget"), config.plugins.PIMPmyPLiHD.InfobarWeatherCityWidget))	
		list.append(getConfigListEntry(_("MetrixWeather City ID"), config.plugins.MetrixWeather.woeid))
		list.append(getConfigListEntry(_("Temperature Unit"), config.plugins.MetrixWeather.tempUnit))
		list.append(getConfigListEntry(_("Weather Refresh Interval (min)"), config.plugins.MetrixWeather.refreshInterval))

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
		self.session.open(MessageBox, _("PIMP-my-PLiHD-by-talbs\n\nTo get your MetrixWeather City ID visit\n\nhttp://open-store.net/?page=metrixweather"), MessageBox.TYPE_INFO)

	def save(self):
	
		for x in self["config"].list:
			if len(x) > 1:
        			x[1].save()
			else:
       				pass
       			
		###########READING DATA FILES
		try:
			self.appendSkinFile(self.daten + "skin_templates_header.xml")
			self.appendSkinFile(self.daten + config.plugins.PIMPmyPLiHD.InfobarWeatherWidget.value + ".xml")
			self.appendSkinFile(self.daten + config.plugins.PIMPmyPLiHD.InfobarWeatherCityWidget.value + ".xml")
			self.appendSkinFile(self.daten + config.plugins.PIMPmyPLiHD.PiconsChoice.value + ".xml")		

			xFile = open(self.SkinTemplate, "w")
			for xx in self.skin_lines:
				xFile.writelines(xx)
			xFile.close()
	
			q = open(self.SkinFinal,"w")
			for line in open(self.SkinDefault):
				line = line.replace("#0018b9ce", config.plugins.PIMPmyPLiHD.SkinColor.value )
				line = line.replace("nmsbd.ttf", config.plugins.PIMPmyPLiHD.FontSelection.value )
				if config.plugins.PIMPmyPLiHD.ListBoxColor.value == "Black":
					line = line.replace("#0018b9cd", "black")
					line = line.replace("#00fffffe", "MyColor")
				else:
					line = line.replace("#0018b9cd", "MyColor")
					line = line.replace("#00fffffe", "white")
				q.write(line)
			q.close()
			
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
			
	def appendSkinFile(self,appendFileName):
		skFile = open(appendFileName, "r")
		file_lines = skFile.readlines()
		skFile.close()	
		for x in file_lines:
			self.skin_lines.append(x)
			

	def exit(self):
		for x in self["config"].list:
			if len(x) > 1:
					x[1].cancel()
			else:
       				pass
		self.close()
