import Domoticz
import subprocess

class BasePlugin:
    enabled = False
    def __init__(self):
        #self.var = 123
        return

    def onStart(self):
        Domoticz.Log("onStart called")
        if Parameters["Mode6"] == "Debug":
            Domoticz.Debugging(1)
            
        p = subprocess.Popen(["cmd dir", "hello world"], stdout=subprocess.PIPE)
        Domoticz.Log( p.communicate())

        Domoticz.Log("Start creating devces") 
        if (len(Devices) == 0):
        # Mettere loop di creazione devices
            Domoticz.Device(Name="Blink1", Unit=1, Type=241, Subtype=1).Create()
            Domoticz.Device(Name="Blink11", Unit=2, Type=241, Subtype=2).Create()
            Domoticz.Device(Name="Blink111", Unit=3, Type=241, Subtype=4).Create()
            Domoticz.Device(Name="Blink1111", Unit=4, Type=241, Subtype=6).Create()
        Domoticz.Log("Devices created.")
    
    def onStop(self):
        Domoticz.Log("onStop called")


    def onMessage(self, Data, Status, Extra):
        Domoticz.Log("onMessage called")

    def onCommand(self, Unit, Command, Level, Hue):
        Domoticz.Log("onCommand called for Unit " + str(Unit) + ": Parameter '" + str(Command) + "', Level: " + str(Level))


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


def onCommand(Unit, Command, Level, Hue):
    global _plugin
    _plugin.onCommand(Unit, Command, Level, Hue)


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
