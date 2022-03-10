import chipwhisperer as cw
import usb
import time


SCOPETYPE = 'OPENADC'
PLATFORM = 'CWLITEXMEGA'
SS_VER = 'SS_VER_1_1'

try:
    try:
        if not scope.connectStatus:
            scope.con()
    except NameError:
        scope = cw.scope()

    try:
        if SS_VER == "SS_VER_2_0":
            target_type = cw.targets.SimpleSerial2
        else:
            target_type = cw.targets.SimpleSerial
    except:
        SS_VER="SS_VER_1_1"
        target_type = cw.targets.SimpleSerial

    try:
        target = cw.target(scope, target_type)
    except IOError:
        print("INFO: Caught exception on reconnecting to target - attempting to reconnect to scope first.")
        print("INFO: This is a work-around when USB has died without Python knowing. Ignore errors above this line.")
        scope = cw.scope()
        target = cw.target(scope, target_type)
except:
    if usb.__version__ < '1.1.0':
        print("-----------------------------------")
        print("Unable to connect to chipwhisperer. pyusb {} detected (>= 1.1.0 required)".format(usb.__version))
        print("-----------------------------------")
    raise
print("INFO: Found ChipWhisperer😍")

prog = cw.programmers.XMEGAProgrammer

time.sleep(0.05)
scope.default_setup()
scope.io.pdic = 'low'
time.sleep(0.1)
scope.io.pdic = 'high_z' #XMEGA doesn't like pdic driven high
time.sleep(0.1) #xmega needs more startup time
scope.clock.clkgen_freq = 100E6
scope.glitch.clk_src="clkgen"
scope.glitch.resetDCMs()
scope.glitch.output = "enable_only"
scope.io.glitch_hp = True

scope.glitch.repeat = 69    # Adjust this value to vary the glitch duration
scope.glitch.manual_trigger()   # Send this command to trigger the glitch
