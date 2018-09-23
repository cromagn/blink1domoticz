# Blink1 PlugIn
#
# Author: cromagn
# BETA - Not production ready - Use at your own risk
# GNU General Public License v3.0
#
"""
<plugin 
key="blink1" 
name="Blink(1) Devices" 
author="cromagn" version="0.0.3" wikilink="http://cromagn.blogspot.com/"
externallink="https://blink1.thingm.com/"
description=" A plugin able to control the Blink(1) led device"
>
    <params>
        <param field="Address" label="IP Address" width="200px" required="true" default="127.0.0.1"/>
        <param field="Mode1" label="Port" width="75px" default="8888"/>
        <param field="Mode6" label="Debug" width="100px">
            <options>
                <option label="True" value="Debug" default="true"/>
                <option label="False" value="Normal" />
            </options>
        </param>
    </params>
</plugin>
"""
import Domoticz
import subprocess
import ast

class BasePlugin:
    # Move to init ASAP
    myConn= None
    enabled = False
    httpConn = None
    command = 'blink1/on'
    level=100
    Hue=0
    rgb='ffffff'
    cw=0
    m=0
    t=0
    w=0
    
    def __init__(self):
      
        return

    def onStart(self):
        Domoticz.Log("onStart called")
        if Parameters["Mode6"] == "Debug":
            Domoticz.Debugging(1)

        Domoticz.Log("Start creating devices") 
        if (len(Devices) == 0):
        # Mettere loop di creazione devices
            Domoticz.Device(Name="BlinkRGB", Unit=2, Type=241, Subtype=2).Create()

        Domoticz.Log("Devices created.")
        Domoticz.Log("Start create connection.")
        self.myConn=Domoticz.Connection(Name="Blink_conn", Transport="TCP/IP", Protocol="HTTP", Address=Parameters["Address"], Port=Parameters["Mode1"])
        Domoticz.Log("Connection created.")
    
    def onStop(self):
        Domoticz.Log("onStop called")
        
    def onConnect(self, Connection, Status, Description):
        Domoticz.Log("onConnect called with parameter " + self.command)
        
        sendData = { 'Verb' : 'GET',
                         'URL'  : str(self.command),
                         'Headers' : { 'Content-Type': 'text/xml; charset=utf-8', \
                                       'Connection': 'keep-alive', \
                                       'Accept': 'Content-Type: text/html; charset=UTF-8', \
                                       'Host': Parameters["Address"]+":"+Parameters["Mode1"], \
                                       'User-Agent':'Domoticz/1.0' }
                       }
        Connection.Send(sendData)
        Connection.Disconnect()
        


    def onMessage(self, Data, Status):
        Domoticz.Log("onMessage called")

    def onCommand(self, Unit, Command, Level, Hue):
        Domoticz.Log("onCommand called for Unit " + str(Unit) + ": Parameter '" + str(Command) + "', Level: " + str(Level)+ "', Hue: " + str(Hue))
        
        if str(Command)=='Set Color':
            # Set Color attribute
            self.level = Level
            re = ast.literal_eval(str(Hue))
            self.rgb='%.2x' % re.get("r", "00")+ '%.2x' % re.get("g", "00")+ '%.2x' % re.get("b", "00")
            self.cw=re.get("cw", "00")
            self.m=re.get("m", "00")
            self.t=re.get("t", "00")
            self.ww=re.get("ww", "00")
             
        if str(Command)=='On':
            # If level > 95--> fadeto else blink
            if(self.level>95):
                self.command='/blink1/fadeToRGB?rgb=%23'+str(self.rgb)+'&time=0.5'
                #Lamp ON on the Domoticz representation
                Devices[2].Update(nValue=1, sValue='On')
            else:
                self.command='/blink1/blink?rgb=%23'+str(self.rgb)+'&time=0.5&count='+  str(self.level)       
            
            self.myConn.Connect()
            
        if str(Command)=='Off':
            self.command='/blink1/off'
            #Lamp OFF on the Domoticz representation
            Devices[2].Update(nValue=0, sValue='Off')
            self.myConn.Connect()
        
      
        Domoticz.Log("onCommand ended")

    def onDisconnect(self, Connection):
        Domoticz.Log("onDisconnect called")
        
    def onHeartbeat(self):
        Domoticz.Log("onHeartbeat called")

global _plugin
_plugin = BasePlugin()

def onStart():
    global _plugin
    _plugin.onStart()

def onStop():
    global _plugin
    _plugin.onStop()

def onConnect(Connection, Status, Description):
    global _plugin
    _plugin.onConnect(Connection, Status, Description)

def onMessage(Connection, Data):
    global _plugin
    _plugin.onMessage(Connection, Data)

def onCommand(Unit, Command, Level, Hue):
    global _plugin
    _plugin.onCommand(Unit, Command, Level, Hue)

def onNotification(Name, Subject, Text, Status, Priority, Sound, ImageFile):
    global _plugin
    _plugin.onNotification(Name, Subject, Text, Status, Priority, Sound, ImageFile)

def onDisconnect(Connection):
    global _plugin
    _plugin.onDisconnect(Connection)

def onHeartbeat():
    global _plugin
    _plugin.onHeartbeat()

    # Generic helper functions
def DumpConfigToLog():
    for x in Parameters:
        if Parameters[x] != "":
            Domoticz.Debug( "'" + x + "':'" + str(Parameters[x]) + "'")
    Domoticz.Debug("Device count: " + str(len(Devices)))
    for x in Devices:
        Domoticz.Debug("Device:           " + str(x) + " - " + str(Devices[x]))
        Domoticz.Debug("Device ID:       '" + str(Devices[x].ID) + "'")
        Domoticz.Debug("Device Name:     '" + Devices[x].Name + "'")
        Domoticz.Debug("Device nValue:    " + str(Devices[x].nValue))
        Domoticz.Debug("Device sValue:   '" + Devices[x].sValue + "'")
        Domoticz.Debug("Device LastLevel: " + str(Devices[x].LastLevel))
    return
