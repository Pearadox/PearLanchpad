import sys, time
import pygame

try:
	import launchpad_py as launchpad
except ImportError:
	try:
		import launchpad
	except ImportError:
		sys.exit("ERROR: loading launchpad.py failed")


# LED Arrays:
leds = [
    [[60,0,60],[60,0,60],[63,10,0],[0,0,0],[63,0,0],[0,0,0],[63,10,0],[63,10,0],[0,0,0]],
    [[60,0,60],[60,0,60],[0,0,0],[0,0,0],[0,63,0],[0,63,0],[20,20,20],[20,20,20],[20,20,20]],
    [[0,0,0],[0,0,0],[0,0,0],[0,0,0],[50,30,0],[50,30,0],[0,30,30],[0,30,30],[0,30,30]],
    [[0,0,0],[0,0,0],[0,0,0],[63,10,0],[63,10,0],[63,10,0],[63,10,0],[63,10,0],[63,10,0]],
    [[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0]],
    [[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0]],
    [[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0]],
    [[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0]],
    [[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0]],
]

# Current button status:
btns = [[False for x in range(9)] for y in range(9)]

# reset pattern counter
resetSenseTime = 0
isPattern = False

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
    lp.Reset()
    global btns
    btns = [[False for x in range(9)] for y in range(9)]

    pygame.time.wait(100)

    # Set LED colors to default defined
    for r in range(9):
        for c in range(9):
            setColor(r, c, leds[r][c][0], leds[r][c][1], leds[r][c][2])
    setColor(0, 7, leds[0][7][0], leds[0][7][1], leds[0][7][2])

    while 1:
        pygame.time.wait(10)

        # call looper
        looper()

        # update button events
        stateArray = lp.ButtonStateXY()
        if(len(stateArray) == 0):
            continue

        # update buttons
        row = str(stateArray[1])
        column = str(stateArray[0])
        isPressed = stateArray[2] == 127
        print(row + " " + column + " " + str(isPressed))
        received(stateArray[1], stateArray[0], isPressed)


# sets color of an individual pad
def setColor(row, column, r, g, b, shifter=0) :
    lp.LedCtrlXY(column, row, min(63, r + shifter), min(63, g + shifter), min(63, b + shifter))

def setAllColor(r, g, b):
    lp.LedAllOn(r,g,b)

# called on every pad press
def received(r, c, isPressed):
    # update btn array
    btns[r][c] = isPressed

    # change shifter color of pad to indicate press/release
    if isPressed:
        setColor(r, c, leds[r][c][0], leds[r][c][1], leds[r][c][2], 20)
    else:
        setColor(r, c, leds[r][c][0], leds[r][c][1], leds[r][c][2], 0)

    # check for reset pattern
    if btns[8][0] and btns[8][1] and btns[8][2] and btns[8][3]:
        global isPattern
        global resetSenseTime
        currentTimeMillis = int(round(time.time() * 1000))
        if not isPattern:
            resetSenseTime = currentTimeMillis
            isPattern = True
    else:
        isPattern = False


def looper():
    global isPattern
    global resetSenseTime
    currentTimeMillis = int(round(time.time() * 1000))
    if isPattern and (currentTimeMillis - resetSenseTime) > 1000:
        isPattern = False

        # show reset indication
        setAllColor(0,63,0)
        pygame.time.wait(500)

        main()


main()