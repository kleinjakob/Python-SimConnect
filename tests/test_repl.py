from SimConnect import *
import logging
from SimConnect.Enum import *
from time import sleep
import signal
import sys

def signal_handler(sig, frame):
	print('Received SIGINT! Exiting now...')
	sm.exit()
	sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)

logging.basicConfig(level=logging.DEBUG)
LOGGER = logging.getLogger(__name__)
LOGGER.info("START")
# time holder for inline commands
ct_g = millis()

# creat simconnection and pass used user classes
sm = SimConnect()
aq = AircraftRequests(sm)
ae = AircraftEvents(sm)

# Add a simple REPL, exposing the SimConnect Interface.

header = "SimConnect Test REPL"
footer = "Closing now!"

# Some Example definitions:
A = aq.find("ATC_ID")
T = ae.find("TOGGLE_PUSHBACK")
H = ae.find("KEY_TUG_HEADING")
S = ae.find("KEY_TUG_SPEED")
def H2I(hdg):
	return int((2**32-1)*hdg/360)

scope_vars = {"sm": sm, "aq": aq, "ae": ae, "A": A, "T": T, "H": H, "S": S, "H2I": H2I}

try:
	import IPython
except ImportError:
	from code import InteractiveConsole
	InteractiveConsole(locals=scope_vars).interact(header, footer)
else:
	print(header)
	IPython.start_ipython(argv=[], user_ns=scope_vars)
	print(footer)

sm.exit()
