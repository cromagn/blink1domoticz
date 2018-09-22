## blink1domoticz

BETA - Not production ready - Use at your own risk

A simple Domoticz plugin to blink(1) gateway 

- Uses blink1-tiny-server to talk to blink(1)

To build:
```
mkdir blink1
cd blink1
wget https://raw.githubusercontent.com/cromagn/blink1domoticz/master/blink1/plugin.pyet 
```

Usage:
```
usage:
  Switch OFF --> Turn Blink(1) off
  Switch ON --> Turn Blink(1) on if level >95 else blink for "level" value times
