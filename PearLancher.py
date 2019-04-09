import sys
from pygame import time

try:
	import launchpad_py as launchpad
except ImportError:
	try:
		import launchpad
	except ImportError:
		sys.exit("ERROR: loading launchpad.py failed")


# LED Arrays:
leds = [
    [[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0]],
    [[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0]],
    [[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0]],
    [[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0]],
    [[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0]],
    [[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0]],
    [[0,0,0],[0,0,0],[0,63,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0]],
    [[0,0,0],[0,0,0],[0,63,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0]],
    [[0,0,0],[0,0,0],[0,63,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0]],
]


# create an instance
lp = launchpad.LaunchpadMk2();


def main():
    # open the first Launchpad Mk2
    if lp.Open(0, "mk2"):
        print(" - Launchpad Mk2: OK")
    else:
        print(" - Launchpad Mk2: ERROR")
        return

    # Clear the buffer because the Launchpad remembers everything
    lp.ButtonFlush()

    # Set LED colors to default defined
    for r in range(9):
        for c in range(9):
            setColor(r, c, leds[r][c][0], leds[r][c][1], leds[r][c][2])

    while 1:
        stateArray = lp.ButtonStateXY()
        if(len(stateArray) == 0):
            time.wait(30)
            continue
        row = str(stateArray[1])
        column = str(stateArray[0])
        isPressed = stateArray[2] == 127
        print(row + " " + column + " " + str(isPressed))
        received(stateArray[1], stateArray[0], isPressed)

# sets color of an individual pad
def setColor(row, column, r, g, b, shifter=0) :
    lp.LedCtrlXY(column, row, min(63, r + shifter), min(63, g + shifter), min(63, b + shifter))

# called on every pad press
def received(r, c, isPressed):
    # change shifter color of pad to indicate press/release
    if isPressed:
        setColor(r, c, leds[r][c][0], leds[r][c][1], leds[r][c][2], 20)
    else:
        setColor(r, c, leds[r][c][0], leds[r][c][1], leds[r][c][2], 0)

main()