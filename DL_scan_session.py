#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Deterministic Learning Scan Session (version 5.0.1)

~~ Version Info ~~
5.0.1: Jan 18, 2017, minor adjustments to scan version. 
    Fixed error with randomizing the order of Round 2 lists
    Adjusted instructions to be simpler and report the correct response hands depending on counterbalance setting
    Added dimming of text to unselected word to show some feedback about which word was chosen
    Capped max bonus at $15.0

~~ PsychoPy Version Info and Citations ~~
Developed for PsychoPy2 v1.82.01
  Peirce, JW (2007) PsychoPy - Psychophysics software in Python. 
    Journal of Neuroscience Methods, 162(1-2), 8-13.
  Peirce, JW (2009) Generating stimuli for neuroscience using PsychoPy. 
    Frontiers in Neuroinformatics, 2:10. doi: 10.3389/neuro.11.010.2008
"""

from __future__ import division
from psychopy import visual, core, data, event, logging, gui
from psychopy.constants import *
import numpy as np
from numpy import sin, cos, tan, log, log10, pi, average, sqrt, std, deg2rad, rad2deg, linspace, asarray
from numpy.random import random, randint, normal, shuffle
import random
import os

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# User options
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# Experiment Name
expName = 'DL Scan Session v500 series'
# Experiment Info Collection
expInfo = {'subject':'', 'age':'','sex':'f','eth':'w','hand':'r','counterbalance':0}
# Experiment Version
expVersion='5.0.1'

# ~~~~~~ Window Properties ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# Window resolution width
displayW = 1024
# Window resolution height
displayH = 768
# Background color
bgColor = [-0.7,-0.7,-0.7]
# Size of space to use on display, width
windowFractionW = 0.9
# Size of space to use on display, height
windowFractionH = 0.9

# ~~~~~~ Text Properties ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# Font size for stimuli (words and feedback text), in pixels
stimFontSize = 45
# Font size for normal text (instructions, break screen, finish), in pixels
textFontSize = 24
# Font size for fixation cross, in pixels
fixhFontSize = 80
# Set this to True if stimulus text should be bold
bStimTextBold=False
# Font color for normal text
fontColor = 'lightgray'
# Font color for highlighted text (e.g., selected word)
brightFontColor = 'white'
# Font color for dimmed text (e.g., unselected word)
dimFontColor = 'gray'
# Font color for positive feedback
corColor = 'lime'
# Font color for negative feedback
errColor = 'red'

# ~~~~~~ Image Properties ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# Background image resolution
imgW = 900
imgH = 600
# Size of semi-transparent background box for text display
boxW = 250
boxH = 250
# Opacity of background box (1.0 = opaque)
boxOpacity = 0.5

# ~~~~~~ Timing Properties ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
dlReadyScans = 3
dlBaselineScans = 4
dlNBackTrials = 7 #NB, don't change, this is hard-coded into the list file

# Length of stimulus display (trial), in seconds
dlStimTime = 4.0
# Length of feedback display, in seconds
dlFdbkTime = 2.0

nbTrialTime = 1.0
nbFixTime = 1.0

nPairs = 80

# ~~~~~~ Task Instructions ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

sDlInstructionsC0R1 = ("We'll be starting soon. This will be the same task that you practiced before getting in the scanner. To remind you, "
"The goal is to learn which words you should select and which you should avoid. Focus on the words you select.\n\n"+
"There will be a total of 80 pairs of words, broken up into 4 blocks. After the first four blocks, we'll repeat the 80 pairs for another four blocks.\n\n"+
"Remember, the second time through the set, you will no longer see feedback, but your responses will count toward earning some bonus cash. "
"You\'ll see how much you earned at the very end.\n\n"
"To select the TOP word, press the button under your RIGHT index finger.\n\n"
"To select the BOTTOM word, press the button under your LEFT index finger.\n\n"
"The words will be on the screen for 4 seconds. Please respond any time while they are on the screen.\n\n"
"The experimenter will check in with you in a moment. In the meantime, relax a bit!")
sDlInstructionsC0R2 = ("Good work so far! You're half way there.\n\n"
"This is the start of the second round. You\'ll see the words you selected in those first four blocks, but this time paired with a brand new word. "
"Words that were correct are still correct this time through. Incorrect words are still incorrect. Try to make as many correct choices as you can to earn "
"some bonus cash. You won\'t get any feedback, but you can see how much you earned at the very end.\n\n"
"As before, to select the TOP word, press the button under your RIGHT index finger.\n\n"
"To select the BOTTOM word, press the button under your LEFT index finger.\n\n"
"The words will be on the screen for 4 seconds. Please respond any time while they are on the screen.\n\n"
"The experimenter will check in with you in a moment. Try your hardest and good luck!")
sDlInstructionsC1R1 = ("We'll be starting soon. This will be the same task that you practiced before getting in the scanner. To remind you, "
"The goal is to learn which words you should select and which you should avoid. Focus on the words you select.\n\n"+
"There will be a total of 80 pairs of words, broken up into 4 blocks. After the first four blocks, we'll repeat the 80 pairs for another four blocks.\n\n"+
"Remember, the second time through the set, you will no longer see feedback, but your responses will count toward earning some bonus cash. "
"You\'ll see how much you earned at the very end.\n\n"
"To select the TOP word, press the button under your LEFT index finger.\n\n"
"To select the BOTTOM word, press the button under your RIGHT index finger.\n\n"
"The words will be on the screen for 4 seconds. Please respond any time while they are on the screen.\n\n"
"The experimenter will check in with you in a moment. In the meantime, relax a bit!")
sDlInstructionsC1R2 = ("Good work so far! You're half way there.\n\n"
"This is the start of the second round. You\'ll see the words you selected in those first four blocks, but this time paired with a brand new word. "
"Words that were correct are still correct this time through. Incorrect words are still incorrect. Try to make as many correct choices as you can to earn "
"some bonus cash. You won\'t get any feedback, but you can see how much you earned at the very end.\n\n"
"As before, to select the TOP word, press the button under your LEFT index finger.\n\n"
"To select the BOTTOM word, press the button under your RIGHT index finger.\n\n"
"The words will be on the screen for 4 seconds. Please respond any time while they are on the screen.\n\n"
"The experimenter will check in with you in a moment. Try your hardest and good luck!")

sDlBreakText = ("Take a short break. We'll resume in a moment.")

sDlFinalDisplay = ('Congratulations, you have finished! We have one more short task for you. The experimenter will check on you shortly.')

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# Experiment Setup
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# Ensure that relative paths start from the same directory as this script
_thisDir = os.path.dirname(os.path.abspath(__file__))
os.chdir(_thisDir)

# Set up experiment files and info
dlg = gui.DlgFromDict(dictionary=expInfo, title=expName)
if dlg.OK == False: core.quit()  # user pressed cancel

inFile = gui.fileOpenDlg(prompt='Select all four list files for this experiment (named consecutively):', allowed="CSV files (.csv)|*.csv", tryFilePath=_thisDir)
if inFile == None: core.quit()
if len(inFile) != 4:
    core.quit()

run1List = inFile[0]; run2List = inFile[1]; run3List = inFile[2]; run4List = inFile[3]

expInfo['date'] = data.getDateStr()
expInfo['expName'] = expName
expInfo['expVersion'] = expVersion
endExpNow = False # flag for experiment kill switch

# Data caching vars
selection = ''
trialAcc = 0
rewValue = 0
curReward = 0

# Set up data dir and file
if not os.path.isdir('__data'):
    os.makedirs('__data')
filenameDL = _thisDir + os.sep + '__data' + os.path.sep + 's%s_%s_v%s__%s' %( expInfo.get('subject'), 'DL', expVersion, expInfo['date'])
logFile = logging.LogFile(filenameDL+'.log', level=logging.DEBUG)
logging.console.setLevel(logging.WARNING)

# Set up experiment manager
dlExp = data.ExperimentHandler(
    name=expName,
    version=expVersion,
    extraInfo=expInfo,
    dataFileName=filenameDL
)

# Set up display
win = visual.Window(
    size=(displayW, displayH),
    fullscr=True,
    screen=0,
    allowGUI=False,
    allowStencil=False,
    monitor=u'testMonitor',
    color=bgColor,
    colorSpace='rgb',
    useFBO=True
)
expInfo['frameRate']=win.getActualFrameRate()
if expInfo['frameRate']!=None:
    frameDur = 1.0/round(expInfo['frameRate'])
else:
    frameDur = 1.0/60.0

# Set up clocks for timing
instructClock = core.Clock()
readyClock = core.Clock()
jitterClock = core.Clock()
trialClock = core.Clock()
feedbackClock = core.Clock()
nBackDispClock = core.Clock()
nBackFixClock = core.Clock()
finishClock = core.Clock()
globalClock = core.Clock()
routineTimer = core.CountdownTimer() 

# Run and trial loop handlers
dlBlock1Runs = data.TrialHandler(
    nReps=4,
    method='sequential',
    extraInfo=expInfo,
    trialList=[None],
    name='dlBlock1Runs'
)
dlBlock2Runs = data.TrialHandler(
    nReps=4,
    method='sequential',
    extraInfo=expInfo,
    trialList=[None],
    name='dlBlock2Runs'
)
dlTrials = data.TrialHandler(
    nReps=1,
    method='random',
    extraInfo=expInfo,
    trialList=data.importConditions(str(run1List)),
    name='dlTrials'
)

# Set up display objects
instructText = visual.TextStim(
    win=win,
    name='instructText',
    text='Task instructions...',
    font='Arial',
    height=textFontSize,
    units='pix',
    wrapWidth=int( round( displayW*windowFractionW, -1) ),
    color=fontColor,
    colorSpace='rgb'
)
readyText = visual.TextStim(
    win=win,
    name='readyText',
    text='The experiment will begin in a moment...',
    font='Arial',
    height=textFontSize,
    units='pix',
    wrapWidth=int( round( displayW*windowFractionW,-1) ),
    color=fontColor,
    colorSpace='rgb'
)
jitterText = visual.TextStim(
    win=win,
    name='jitterText',
    text='+',
    font='Arial',
    units='pix',
    height=fixhFontSize,
    bold=bStimTextBold,
    color=fontColor,
    colorSpace='rgb'
)
dlWordTop = visual.TextStim(
    win=win,
    name='dlWordTop',
    text='',
    font='Arial',
    bold=bStimTextBold,
    pos=[0, 50],
    units='pix',
    height=stimFontSize,
    color=fontColor,
    colorSpace='rgb'
)
dlWordBtm = visual.TextStim(
    win=win,
    name='dlWordBtm',
    text='',
    font='Arial',
    bold=bStimTextBold,
    pos=[0, -50],
    units='pix',
    height=stimFontSize,
    color=fontColor,
    colorSpace='rgb'
)
dlBox = visual.Rect(
    win=win,
    name='dlBox',
    width=boxW,
    height=boxH,
    lineWidth=1,
    lineColor='black',
    lineColorSpace='rgb',
    fillColor='black',
    fillColorSpace='rgb',
    opacity=boxOpacity,
    interpolate=True,
    units='pix'
)
dlImage = visual.ImageStim(
    win=win,
    name='dlImage',
    size=[imgW,imgH],
    units='pix',
    interpolate=True
)
dlReward = visual.TextStim(
    win=win,
    name='dlReward',
    text='- - -',
    font='Arial',
    bold=bStimTextBold,
    pos=[0,0],
    units='pix',
    height=stimFontSize,
    color=fontColor,
    colorSpace='rgb'
)
nbWord = visual.TextStim(
    win=win,
    name='nbWord',
    text='WORD',
    font='Arial',
    pos=[0,0],
    units='pix',
    height=stimFontSize,
    color=fontColor,
    colorSpace='rgb'
)
nbFix = visual.TextStim(
    win=win,
    name='nbFix',
    text='+',
    font='Arial',
    units='pix',
    height=fixhFontSize,
    bold=bStimTextBold,
    color=fontColor,
    colorSpace='rgb'
)
finishText = visual.TextStim(
    win=win,
    name='finishText',
    text='Congratulations! You are done!\n\nSomeone will be in to get you out shortly.',
    font='Arial',
    height=textFontSize,
    units='pix',
    wrapWidth=int( round( displayW*windowFractionW, -1) ),
    color=fontColor,
    colorSpace='rgb'
)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# Run experiment
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#~~| DL R1 Instructions |~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
if expInfo['counterbalance'] == 0:
    instructText.setText( sDlInstructionsC0R1)
elif expInfo['counterbalance'] == 1:
    instructText.setText( sDlInstructionsC1R1)
else:
    print("error: invalid counterbalance value.")
    core.quit()

t = 0
instructClock.reset()
frameN = -1
event.clearEvents(eventType='keyboard')
contResp = event.BuilderKeyResponse()
contResp.status = NOT_STARTED
instructComponents = []
instructComponents.append(instructText)
instructComponents.append(contResp)
for thisComponent in instructComponents:
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED
continueRoutine = True
while continueRoutine:
    t = instructClock.getTime()
    frameN = frameN + 1
    if t >= 0.0 and instructText.status == NOT_STARTED:
        instructText.tStart = t
        instructText.frameNStart = frameN
        instructText.setAutoDraw(True)
    if t >= 0.0 and contResp.status == NOT_STARTED:
        contResp.tStart = t
        contResp.frameNStart = frameN
        contResp.status = STARTED
        contResp.clock.reset()
        event.clearEvents(eventType='keyboard')
    if contResp.status == STARTED:
        theseKeys = event.getKeys(keyList=['space'])
        if "escape" in theseKeys:
            endExpNow = True
        if len(theseKeys) > 0:
            contResp.keys = theseKeys[-1]
            contResp.rt = contResp.clock.getTime()
            continueRoutine = False
    if not continueRoutine:
        break
    continueRoutine = False
    for thisComponent in instructComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break
    if endExpNow or event.getKeys(keyList=["escape"]):
        core.quit()
    if continueRoutine:
        win.flip()
for thisComponent in instructComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
if contResp.keys in ['', [], None]:
   contResp.keys=None
routineTimer.reset()

#~~| DL R1 Trial Loop |~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
dlBlock1Runs = data.TrialHandler(
    nReps=4,
    method='sequential',
    extraInfo=expInfo,
    trialList=[None],
    name='dlBlock1Runs'
)
dlExp.addLoop(dlBlock1Runs)
thisRun = dlBlock1Runs.trialList[0]

# Dictionary to hold words that S chooses
selectedWords = dict()

for thisRun in dlBlock1Runs:
    currentLoop = dlBlock1Runs
    
    # Loop the ready screen for 3 discard acquisitions at the beginning of each run
    readyLoop = data.TrialHandler(
        nReps=dlReadyScans,
        method='sequential', 
        extraInfo=expInfo,
        trialList=[None],
        name='readyLoop'
    )
    thisReadyLoop = readyLoop.trialList[0]
    for thisReadyLoop in readyLoop:
        t = 0
        readyClock.reset()
        frameN = -1
        event.clearEvents(eventType='keyboard')
        triggerCatch = event.BuilderKeyResponse()
        triggerCatch.status = NOT_STARTED
        readyComponents = []
        readyComponents.append(readyText)
        readyComponents.append(triggerCatch)
        for thisComponent in readyComponents:
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        continueRoutine = True
        while continueRoutine:
            t = readyClock.getTime()
            frameN = frameN + 1
            if t >= 0.0 and readyText.status == NOT_STARTED:
                readyText.tStart = t
                readyText.frameNStart = frameN
                readyText.setAutoDraw(True)
            if t >= 0.0 and triggerCatch.status == NOT_STARTED:
                triggerCatch.tStart = t
                triggerCatch.frameNStart = frameN
                triggerCatch.status = STARTED
                triggerCatch.clock.reset()
                event.clearEvents(eventType='keyboard')
            if triggerCatch.status == STARTED:
                theseKeys = event.getKeys(keyList=['lshift'])
                if "escape" in theseKeys:
                    endExpNow = True
                if len(theseKeys) > 0:
                    triggerCatch.keys = theseKeys[-1]
                    triggerCatch.rt = triggerCatch.clock.getTime()
                    continueRoutine = False
            if not continueRoutine:
                break
            continueRoutine = False
            for thisComponent in readyComponents:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break
            if endExpNow or event.getKeys(keyList=["escape"]):
                core.quit()
            if continueRoutine:
                win.flip()
        for thisComponent in readyComponents:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        if triggerCatch.keys in ['', [], None]:
           triggerCatch.keys=None
        routineTimer.reset()
#        dlExp.nextEntry()
    
    # Handle import of trial lists
    if dlBlock1Runs.thisN == 0:
        curRunList = run1List
    elif dlBlock1Runs.thisN == 1:
        curRunList = run2List
    elif dlBlock1Runs.thisN == 2:
        curRunList = run3List
    elif dlBlock1Runs.thisN == 3:
        curRunList = run4List
    dlTrials = data.TrialHandler(
        nReps=1,
        method='random',
        extraInfo=expInfo,
        trialList=data.importConditions( str( curRunList ) ),
        name='dlTrials'
    )
    dlExp.addLoop(dlTrials)
    thisDlTrial = dlTrials.trialList[0]
    
    for thisDlTrial in dlTrials:
        currentLoop = dlTrials
        # Loop jitter screen for N times, determined by input list
        jitterLoop = data.TrialHandler(
            nReps=int(thisDlTrial['jitter']),
            method='sequential',
            extraInfo=expInfo,
            trialList=[None],
            name='jitterLoop'
        )
        thisJitterLoop = jitterLoop.trialList[0]
        
        for thisJitterLoop in jitterLoop:
            t = 0
            jitterClock.reset()
            frameN = -1
            event.clearEvents(eventType='keyboard')
            triggerCatch = event.BuilderKeyResponse()
            triggerCatch.status = NOT_STARTED
            jitterComponents = []
            jitterComponents.append(jitterText)
            jitterComponents.append(triggerCatch)
            for thisComponent in jitterComponents:
                if hasattr(thisComponent, 'status'):
                    thisComponent.status = NOT_STARTED
            continueRoutine = True
            while continueRoutine:
                t = jitterClock.getTime()
                frameN = frameN + 1
                if t >= 0.0 and jitterText.status == NOT_STARTED:
                    jitterText.tStart = t
                    jitterText.frameNStart = frameN
                    jitterText.setAutoDraw(True)
                if t >= 0.0 and triggerCatch.status == NOT_STARTED:
                    triggerCatch.tStart = t
                    triggerCatch.frameNStart = frameN
                    triggerCatch.status = STARTED
                    triggerCatch.clock.reset()
                    event.clearEvents(eventType='keyboard')
                if triggerCatch.status == STARTED:
                    theseKeys = event.getKeys(keyList=['lshift'])
                    if "escape" in theseKeys:
                        endExpNow = True
                    if len(theseKeys) > 0:
                        triggerCatch.keys = theseKeys[-1]
                        triggerCatch.rt = triggerCatch.clock.getTime()
                        continueRoutine = False
                if not continueRoutine:
                    break
                continueRoutine = False
                for thisComponent in jitterComponents:
                    if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                        continueRoutine = True
                        break
                if endExpNow or event.getKeys(keyList=["escape"]):
                    core.quit()
                if continueRoutine:
                    win.flip()
            for thisComponent in jitterComponents:
                if hasattr(thisComponent, "setAutoDraw"):
                    thisComponent.setAutoDraw(False)
            if triggerCatch.keys in ['', [], None]:
               triggerCatch.keys=None
            routineTimer.reset()
#            dlExp.nextEntry()
        
        #~~~| DL trial |~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
        # Randomize and set item positions
        rand = randint(0,2)
        if rand == 1:
            dlWordTop.setText( str(thisDlTrial['word1']) )
            dlWordBtm.setText( str(thisDlTrial['word2']) )
        else:
            dlWordTop.setText( str(thisDlTrial['word2']) )
            dlWordBtm.setText( str(thisDlTrial['word1']) )
            
        # Reset font colors
        dlWordTop.setColor(fontColor)
        dlWordBtm.setColor(fontColor)
        
        # Load image
        dlImage.setImage( str(thisDlTrial['image']) )
        
        # Set up reward value
        rewValue = thisDlTrial['reward']
        trialAcc = -1
        action = ''
        selWord = ''
        
        # Begin trial routine
        t = 0
        trialClock.reset()
        frameN = -1
        routineTimer.add(dlStimTime)
        trialResp = event.BuilderKeyResponse()
        trialResp.status = NOT_STARTED
        event.clearEvents('keyboard')
        trialComponents = []
        trialComponents.append(dlImage)
        trialComponents.append(dlBox)
        trialComponents.append(dlWordTop)
        trialComponents.append(dlWordBtm)
        trialComponents.append(trialResp)
        for thisComponent in trialComponents:
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        continueRoutine = True
        while continueRoutine and routineTimer.getTime() > 0:
            t = trialClock.getTime()
            frameN = frameN + 1
            if t >= 0.0 and dlImage.status == NOT_STARTED:
                dlImage.tStart = t
                dlImage.frameNStart = frameN
                dlImage.setAutoDraw(True)
            if dlImage.status == STARTED and t >= (0.0 + (dlStimTime-win.monitorFramePeriod*0.75)):
                dlImage.setAutoDraw(False)
            if t >= 0.0 and dlBox.status == NOT_STARTED:
                dlBox.tStart = t
                dlBox.frameNStart = frameN
                dlBox.setAutoDraw(True)
            if dlBox.status == STARTED and t >= (0.0 + (dlStimTime-win.monitorFramePeriod*0.75)):
                dlBox.setAutoDraw(False)
            if t >= 0.0 and dlWordTop.status == NOT_STARTED:
                dlWordTop.tStart = t
                dlWordTop.frameNStart = frameN
                dlWordTop.setAutoDraw(True)
            if dlWordTop.status == STARTED and t >= (0.0 + (dlStimTime-win.monitorFramePeriod*0.75)):
                dlWordTop.setAutoDraw(False)
            if t >= 0.0 and dlWordBtm.status == NOT_STARTED:
                dlWordBtm.tStart = t
                dlWordBtm.frameNStart = frameN
                dlWordBtm.setAutoDraw(True)
            if dlWordBtm.status == STARTED and t >= (0.0 + (dlStimTime-win.monitorFramePeriod*0.75)):
                dlWordBtm.setAutoDraw(False)
            if t >= 0.0 and trialResp.status == NOT_STARTED:
                trialResp.tStart = t
                trialResp.frameNStart = frameN
                trialResp.status = STARTED
                trialResp.clock.reset()
                event.clearEvents(eventType='keyboard')
            if trialResp.status == STARTED and t >= (0.0 + (dlStimTime-win.monitorFramePeriod*0.75)):
                trialResp.status = STOPPED
            if trialResp.status == STARTED:
                theseKeys = event.getKeys(keyList=['2', '3', '4', '7', '8', '9'])
                if "escape" in theseKeys:
                    endExpNow = True
                if len(theseKeys) > 0:
                    trialResp.keys = theseKeys[-1]
                    trialResp.rt = trialResp.clock.getTime()
                    # Set accuracy for feedback
                    if str( thisDlTrial['feedback'] ) == 'cor':
                        trialAcc = 1
                    else:
                        trialAcc = 0
                    # Figure out which word was chosen
                    action = '--'
                    selWord = '--'
                    if expInfo['counterbalance'] == 0:
                        #<5 = top, >5 bottom
                        if trialResp.keys == '2' or trialResp.keys == '3' or trialResp.keys == '4' or trialResp.keys < 5:
                            action = 'top'
                            selWord = str( dlWordTop.text )
                            dlWordBtm.setColor(dimFontColor) # dim unselected word
                            dlWordTop.setColor(brightFontColor) # highlight selection
                        elif trialResp.keys == '7' or trialResp.keys == '8' or trialResp.keys == '9' or trialResp.keys > 5:
                            action = 'btm'
                            selWord = str( dlWordBtm.text )
                            dlWordTop.setColor(dimFontColor)
                            dlWordBtm.setColor(brightFontColor)
                    elif expInfo['counterbalance'] == 1:
                        #<5 = bottom, >5 top
                        if trialResp.keys == '2' or trialResp.keys == '3' or trialResp.keys == '4' or trialResp.keys < 5:
                            action = 'btm'
                            selWord = str( dlWordBtm.text )
                            dlWordTop.setColor(dimFontColor)
                            dlWordBtm.setColor(brightFontColor)
                        elif trialResp.keys == '7' or trialResp.keys == '8' or trialResp.keys == '9' or trialResp.keys > 5:
                            action = 'top'
                            selWord = str( dlWordTop.text )
                            dlWordBtm.setColor(dimFontColor) # dim unselected word
                            dlWordTop.setColor(brightFontColor) # highlight selection
                    selectedWords[ str(thisDlTrial['pair']) ] = str(selWord)
            if not continueRoutine:
                break
            continueRoutine = False
            for thisComponent in trialComponents:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break
            if endExpNow or event.getKeys(keyList=["escape"]):
                core.quit()
            if continueRoutine:
                win.flip()
        for thisComponent in trialComponents:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        dlTrials.addData('dl.selection', selWord)
        dlTrials.addData('dl.keys', trialResp.keys)
        dlTrials.addData('dl.action', action)
        if trialResp.keys in ['', [], None]:
           trialResp.keys=None
        if trialResp.keys != None:
            dlTrials.addData('dl.acc', trialAcc)
            dlTrials.addData('dl.rt', trialResp.rt)
        else:
            trialAcc = -1 # for feedback display
            selectedWords[ str(thisDlTrial['pair']) ] = str(thisDlTrial['word1'])
            dlTrials.addData('dl.acc', 'noresp')
            dlTrials.addData('dl.rt', 0)
        
        #~~~| DL feedback |~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
        if str(trialAcc) == '1':
            dlReward.setText( u'+$%s!' %(rewValue) )
            dlReward.setColor( corColor )
        elif str(trialAcc) == '0':
            dlReward.setText(u'-$%s' %(rewValue) )
            dlReward.setColor( errColor )
        else:
            dlReward.setText('- - -')
            dlReward.setColor( fontColor)
        
        # Begin feedback routine
        t = 0
        feedbackClock.reset() 
        frameN = -1
        routineTimer.add(dlFdbkTime)
        feedbackComponents = []
        feedbackComponents.append(dlImage)
        feedbackComponents.append(dlBox)
        feedbackComponents.append(dlReward)
        for thisComponent in feedbackComponents:
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        continueRoutine = True
        while continueRoutine and routineTimer.getTime() > 0:
            t = feedbackClock.getTime()
            frameN = frameN + 1
            if t >= 0.0 and dlImage.status == NOT_STARTED:
                dlImage.tStart = t
                dlImage.frameNStart = frameN
                dlImage.setAutoDraw(True)
            if dlImage.status == STARTED and t >= (0.0 + (dlFdbkTime-win.monitorFramePeriod*0.75)):
                dlImage.setAutoDraw(False)
            if t >= 0.0 and dlBox.status == NOT_STARTED:
                dlBox.tStart = t
                dlBox.frameNStart = frameN
                dlBox.setAutoDraw(True)
            if dlBox.status == STARTED and t >= (0.0 + (dlFdbkTime-win.monitorFramePeriod*0.75)):
                dlBox.setAutoDraw(False)
            if t >= 0.0 and dlReward.status == NOT_STARTED:
                dlReward.tStart = t
                dlReward.frameNStart = frameN
                dlReward.setAutoDraw(True)
            if dlReward.status == STARTED and t >= (0.0 + (dlFdbkTime-win.monitorFramePeriod*0.75)):
                dlReward.setAutoDraw(False)
            if not continueRoutine:
                break
            continueRoutine = False
            for thisComponent in feedbackComponents:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break
            if endExpNow or event.getKeys(keyList=["escape"]):
                core.quit()
            if continueRoutine:
                win.flip()
        for thisComponent in feedbackComponents:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        
        #~~~| DL fix (pre NBack) |~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
        t = 0
        jitterClock.reset() 
        frameN = -1
        event.clearEvents('keyboard')
        triggerCatch = event.BuilderKeyResponse()
        triggerCatch.status = NOT_STARTED
        jitterComponents = []
        jitterComponents.append(jitterText)
        jitterComponents.append(triggerCatch)
        for thisComponent in jitterComponents:
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        continueRoutine = True
        while continueRoutine:
            t = jitterClock.getTime()
            frameN = frameN + 1
            if t >= 0.0 and jitterText.status == NOT_STARTED:
                jitterText.tStart = t
                jitterText.frameNStart = frameN
                jitterText.setAutoDraw(True)
            if t >= 0.0 and triggerCatch.status == NOT_STARTED:
                triggerCatch.tStart = t
                triggerCatch.frameNStart = frameN
                triggerCatch.status = STARTED
                triggerCatch.clock.reset()
                event.clearEvents(eventType='keyboard')
            if triggerCatch.status == STARTED:
                theseKeys = event.getKeys(keyList=['lshift'])
                if "escape" in theseKeys:
                    endExpNow = True
                if len(theseKeys) > 0:
                    triggerCatch.keys = theseKeys[-1]
                    triggerCatch.rt = triggerCatch.clock.getTime()
                    continueRoutine = False
            if not continueRoutine:
                break
            continueRoutine = False
            for thisComponent in jitterComponents:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break
            if endExpNow or event.getKeys(keyList=["escape"]):
                core.quit()
            if continueRoutine:
                win.flip()
        for thisComponent in jitterComponents:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        routineTimer.reset()
        
        #~~~| NBack Loop |~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
        nBackWords = [ str( thisDlTrial['nBackWord1'] ), str( thisDlTrial['nBackWord2'] ), str( thisDlTrial['nBackWord3'] ), str( thisDlTrial['nBackWord4'] ), str( thisDlTrial['nBackWord5'] ), str( thisDlTrial['nBackWord6'] ), str( thisDlTrial['nBackWord7'] )]
        # Set up NBack Loop
        nBackLoop = data.TrialHandler(
            nReps=dlNBackTrials,
            method='sequential',
            extraInfo=expInfo,
            originPath=None,
            trialList=[None],
            name='nBackLoop'
        )
        thisNBackLoop = nBackLoop.trialList[0]
        for thisNBackLoop in nBackLoop:
            # Set word for this trial
            nbWord.setText(nBackWords[nBackLoop.thisN])
            
            #~~~| NBack Trial |~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
            t = 0
            nBackDispClock.reset() 
            frameN = -1
            routineTimer.add(nbTrialTime)
            nbResp = event.BuilderKeyResponse()
            nbResp.status = NOT_STARTED
            nBackDispComponents = []
            nBackDispComponents.append(nbWord)
            nBackDispComponents.append(nbResp)
            for thisComponent in nBackDispComponents:
                if hasattr(thisComponent, 'status'):
                    thisComponent.status = NOT_STARTED
            continueRoutine = True
            while continueRoutine and routineTimer.getTime() > 0:
                t = nBackDispClock.getTime()
                frameN = frameN + 1
                if t >= 0.0 and nbWord.status == NOT_STARTED:
                    nbWord.tStart = t
                    nbWord.frameNStart = frameN
                    nbWord.setAutoDraw(True)
                if nbWord.status == STARTED and t >= (0.0 + (nbTrialTime-win.monitorFramePeriod*0.75)):
                    nbWord.setAutoDraw(False)
                if t >= 0.0 and nbResp.status == NOT_STARTED:
                    nbResp.tStart = t
                    nbResp.frameNStart = frameN
                    nbResp.status = STARTED
                    nbResp.clock.reset()
                    event.clearEvents(eventType='keyboard')
                if nbResp.status == STARTED and t >= (0.0 + (nbTrialTime-win.monitorFramePeriod*0.75)):
                    nbResp.status = STOPPED
                if nbResp.status == STARTED:
                    theseKeys = event.getKeys(keyList=['2', '3', '4', '7', '8', '9'])
                    if "escape" in theseKeys:
                        endExpNow = True
                    if len(theseKeys) > 0:
                        nbResp.keys = theseKeys[-1]
                        nbResp.rt = nbResp.clock.getTime()
                if not continueRoutine:
                    break
                continueRoutine = False
                for thisComponent in nBackDispComponents:
                    if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                        continueRoutine = True
                        break
                if endExpNow or event.getKeys(keyList=["escape"]):
                    core.quit()
                if continueRoutine:
                    win.flip()
            for thisComponent in nBackDispComponents:
                if hasattr(thisComponent, "setAutoDraw"):
                    thisComponent.setAutoDraw(False)
            if nbResp.keys in ['', [], None]:
               nbResp.keys=None
            dlTrials.addData('nb.keys',nbResp.keys)
            if nbResp.keys != None:
                dlTrials.addData('nb.rt', nbResp.rt)
            
            #~~~| NBack Fix |~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
            t = 0
            nBackFixClock.reset()
            frameN = -1
            routineTimer.add(nbFixTime)
            nBackFixComponents = []
            nBackFixComponents.append(nbFix)
            for thisComponent in nBackFixComponents:
                if hasattr(thisComponent, 'status'):
                    thisComponent.status = NOT_STARTED
            continueRoutine = True
            while continueRoutine and routineTimer.getTime() > 0:
                t = nBackFixClock.getTime()
                frameN = frameN + 1
                if t >= 0.0 and nbFix.status == NOT_STARTED:
                    nbFix.tStart = t
                    nbFix.frameNStart = frameN
                    nbFix.setAutoDraw(True)
                if nbFix.status == STARTED and t >= (0.0 + (nbFixTime-win.monitorFramePeriod*0.75)):
                    nbFix.setAutoDraw(False)
                if not continueRoutine:
                    break
                continueRoutine = False
                for thisComponent in nBackFixComponents:
                    if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                        continueRoutine = True
                        break
                if endExpNow or event.getKeys(keyList=["escape"]):
                    core.quit()
                if continueRoutine:
                    win.flip()
            for thisComponent in nBackFixComponents:
                if hasattr(thisComponent, "setAutoDraw"):
                    thisComponent.setAutoDraw(False)
            # Next NBack Trial
#            dlExp.nextEntry()
            
        # Next DL trial
        dlExp.nextEntry()
        
    #~~~| End Run Baseline |~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
    baselineLoop = data.TrialHandler(
        nReps=dlBaselineScans,
        method='sequential', 
        extraInfo=expInfo,
        trialList=[None],
        name='baselineLoop'
    )
    thisBaselineLoop = baselineLoop.trialList[0]
    
    for thisBaselineLoop in baselineLoop:
        t = 0
        jitterClock.reset()
        frameN = -1
        event.clearEvents(eventType='keyboard')
        triggerCatch = event.BuilderKeyResponse()
        triggerCatch.status = NOT_STARTED
        jitterComponents = []
        jitterComponents.append(jitterText)
        jitterComponents.append(triggerCatch)
        for thisComponent in jitterComponents:
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        continueRoutine = True
        while continueRoutine:
            t = jitterClock.getTime()
            frameN = frameN + 1
            if t >= 0.0 and jitterText.status == NOT_STARTED:
                jitterText.tStart = t
                jitterText.frameNStart = frameN
                jitterText.setAutoDraw(True)
            if t >= 0.0 and triggerCatch.status == NOT_STARTED:
                triggerCatch.tStart = t
                triggerCatch.frameNStart = frameN
                triggerCatch.status = STARTED
                triggerCatch.clock.reset()
                event.clearEvents(eventType='keyboard')
            if triggerCatch.status == STARTED:
                theseKeys = event.getKeys(keyList=['lshift'])
                if "escape" in theseKeys:
                    endExpNow = True
                if len(theseKeys) > 0:
                    triggerCatch.keys = theseKeys[-1]
                    triggerCatch.rt = triggerCatch.clock.getTime()
                    continueRoutine = False
            if not continueRoutine:
                break
            continueRoutine = False
            for thisComponent in jitterComponents:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break
            if endExpNow or event.getKeys(keyList=["escape"]):
                core.quit()
            if continueRoutine:
                win.flip()
        for thisComponent in jitterComponents:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        if triggerCatch.keys in ['', [], None]:
           triggerCatch.keys=None
        routineTimer.reset()
        # Next baseline scan
#        dlExp.nextEntry()
    
    #~~~| Run break screen |~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
    # Set up screen text
    if dlBlock1Runs.thisN == 3:
        if expInfo['counterbalance'] == 0:
            instructText.setText( sDlInstructionsC0R2)
        elif expInfo['counterbalance'] == 1:
            instructText.setText( sDlInstructionsC1R2)
    else:
        instructText.setText(sDlBreakText)
    t = 0
    instructClock.reset() 
    frameN = -1
    event.clearEvents(eventType='keyboard')
    contResp = event.BuilderKeyResponse()
    contResp.status = NOT_STARTED
    instructComponents = []
    instructComponents.append(instructText)
    instructComponents.append(contResp)
    for thisComponent in instructComponents:
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    continueRoutine = True
    while continueRoutine:
        t = instructClock.getTime()
        frameN = frameN + 1
        if t >= 0.0 and instructText.status == NOT_STARTED:
            instructText.tStart = t
            instructText.frameNStart = frameN
            instructText.setAutoDraw(True)
        if t >= 0.0 and contResp.status == NOT_STARTED:
            contResp.tStart = t
            contResp.frameNStart = frameN
            contResp.status = STARTED
            contResp.clock.reset()
            event.clearEvents(eventType='keyboard')
        if contResp.status == STARTED:
            theseKeys = event.getKeys(keyList=['space'])
            if "escape" in theseKeys:
                endExpNow = True
            if len(theseKeys) > 0:
                contResp.keys = theseKeys[-1]
                contResp.rt = contResp.clock.getTime()
                continueRoutine = False
        if not continueRoutine:
            break
        continueRoutine = False
        for thisComponent in instructComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break
        if endExpNow or event.getKeys(keyList=["escape"]):
            core.quit()
        if continueRoutine:
            win.flip()
    for thisComponent in instructComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    if contResp.keys in ['', [], None]:
       contResp.keys=None
    routineTimer.reset()
    
    # Next Run
    dlExp.nextEntry()

# Handle import of trial lists for Round 2 runs, set up random order for lists 1-4
runOrder = [0, 1, 2, 3]
random.shuffle(runOrder)
#~~| DL R2 Trial Loop |~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
dlBlock2Runs = data.TrialHandler(
    nReps=4,
    method='sequential',
    extraInfo=expInfo,
    trialList=[None],
    name='dlBlock2Runs'
)
dlExp.addLoop(dlBlock2Runs)
thisRun = dlBlock2Runs.trialList[0]

for thisRun in dlBlock2Runs:
    currentLoop = dlBlock2Runs
    
    # Loop the ready screen for 3 discard acquisitions at the beginning of each run
    readyLoop = data.TrialHandler(
        nReps=dlReadyScans,
        method='sequential', 
        extraInfo=expInfo,
        trialList=[None],
        name='readyLoop')
    thisReadyLoop = readyLoop.trialList[0]
    for thisReadyLoop in readyLoop:
        t = 0
        readyClock.reset()
        frameN = -1
        event.clearEvents(eventType='keyboard')
        triggerCatch = event.BuilderKeyResponse()
        triggerCatch.status = NOT_STARTED
        readyComponents = []
        readyComponents.append(readyText)
        readyComponents.append(triggerCatch)
        for thisComponent in readyComponents:
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        continueRoutine = True
        while continueRoutine:
            t = readyClock.getTime()
            frameN = frameN + 1
            if t >= 0.0 and readyText.status == NOT_STARTED:
                readyText.tStart = t
                readyText.frameNStart = frameN
                readyText.setAutoDraw(True)
            if t >= 0.0 and triggerCatch.status == NOT_STARTED:
                triggerCatch.tStart = t
                triggerCatch.frameNStart = frameN
                triggerCatch.status = STARTED
                triggerCatch.clock.reset()
                event.clearEvents(eventType='keyboard')
            if triggerCatch.status == STARTED:
                theseKeys = event.getKeys(keyList=['lshift'])
                if "escape" in theseKeys:
                    endExpNow = True
                if len(theseKeys) > 0:
                    triggerCatch.keys = theseKeys[-1]
                    triggerCatch.rt = triggerCatch.clock.getTime()
                    continueRoutine = False
            if not continueRoutine:
                break
            continueRoutine = False
            for thisComponent in readyComponents:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break
            if endExpNow or event.getKeys(keyList=["escape"]):
                core.quit()
            if continueRoutine:
                win.flip()
        for thisComponent in readyComponents:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        if triggerCatch.keys in ['', [], None]:
           triggerCatch.keys=None
        routineTimer.reset()
#        dlExp.nextEntry()
    
    # Grab list for current run
    if runOrder[dlBlock2Runs.thisN] == 0:
        curRunList = run1List
    elif runOrder[dlBlock2Runs.thisN] == 1:
        curRunList = run2List
    elif runOrder[dlBlock2Runs.thisN] == 2:
        curRunList = run3List
    elif runOrder[dlBlock2Runs.thisN] == 3:
        curRunList = run4List
    
    dlTrials = data.TrialHandler(
        nReps=1,
        method='random',
        extraInfo=expInfo,
        trialList=data.importConditions( str( curRunList ) ),
        name='dlTrials'
    )
    dlExp.addLoop(dlTrials)
    thisDlTrial = dlTrials.trialList[0]
    
    for thisDlTrial in dlTrials:
        currentLoop = dlTrials
        # Loop jitter screen for N times, determined by input list
        jitterLoop = data.TrialHandler(
            nReps=int(thisDlTrial['jitter']),
            method='sequential',
            extraInfo=expInfo,
            trialList=[None],
            name='jitterLoop'
        )
        thisJitterLoop = jitterLoop.trialList[0]
        for thisJitterLoop in jitterLoop:
            t = 0
            jitterClock.reset()
            frameN = -1
            event.clearEvents(eventType='keyboard')
            triggerCatch = event.BuilderKeyResponse()
            triggerCatch.status = NOT_STARTED
            jitterComponents = []
            jitterComponents.append(jitterText)
            jitterComponents.append(triggerCatch)
            for thisComponent in jitterComponents:
                if hasattr(thisComponent, 'status'):
                    thisComponent.status = NOT_STARTED
            continueRoutine = True
            while continueRoutine:
                t = jitterClock.getTime()
                frameN = frameN + 1
                if t >= 0.0 and jitterText.status == NOT_STARTED:
                    jitterText.tStart = t
                    jitterText.frameNStart = frameN
                    jitterText.setAutoDraw(True)
                if t >= 0.0 and triggerCatch.status == NOT_STARTED:
                    triggerCatch.tStart = t
                    triggerCatch.frameNStart = frameN
                    triggerCatch.status = STARTED
                    triggerCatch.clock.reset()
                    event.clearEvents(eventType='keyboard')
                if triggerCatch.status == STARTED:
                    theseKeys = event.getKeys(keyList=['lshift'])
                    if "escape" in theseKeys:
                        endExpNow = True
                    if len(theseKeys) > 0:
                        triggerCatch.keys = theseKeys[-1]
                        triggerCatch.rt = triggerCatch.clock.getTime()
                        continueRoutine = False
                if not continueRoutine:
                    break
                continueRoutine = False
                for thisComponent in jitterComponents:
                    if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                        continueRoutine = True
                        break
                if endExpNow or event.getKeys(keyList=["escape"]):
                    core.quit()
                if continueRoutine:
                    win.flip()
            for thisComponent in jitterComponents:
                if hasattr(thisComponent, "setAutoDraw"):
                    thisComponent.setAutoDraw(False)
            if triggerCatch.keys in ['', [], None]:
               triggerCatch.keys=None
            routineTimer.reset()
#            dlExp.nextEntry()
        
        #~~~| DL trial |~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
        # Randomize and set item positions
        rand = randint(0,2)
        corResp = 'none'
        if rand == 1:
            dlWordTop.setText( str( selectedWords[ str(thisDlTrial['pair']) ] ) )
            dlWordBtm.setText( str(thisDlTrial['word3'] ) )
            if str(thisDlTrial['feedback']) == 'cor':
                if expInfo['counterbalance'] == 0:
                    corResp = '2'
                else:
                    corResp = '7'
            else:
                if expInfo['counterbalance'] == 0:
                    corResp = '7'
                else:
                    corResp = '2'
        else:
            dlWordTop.setText( str(thisDlTrial['word3']) )
            dlWordBtm.setText( str( selectedWords[ str(thisDlTrial['pair']) ] ) )
            if str(thisDlTrial['feedback']) == 'cor':
                if expInfo['counterbalance'] == 0:
                    corResp = '7'
                else:
                    corResp = '2'
            else:
                if expInfo['counterbalance'] == 0:
                    corResp = '2'
                else:
                    corResp = '7'
            
        # Reset font colors
        dlWordTop.setColor(fontColor)
        dlWordBtm.setColor(fontColor)
        
        # Set up reward value
        rewValue = thisDlTrial['reward']
        trialAcc = -1
        action = ''
        selWord = ''
        
        # Begin trial routine
        t = 0
        trialClock.reset()
        frameN = -1
        routineTimer.add(dlStimTime)
        trialResp = event.BuilderKeyResponse()
        trialResp.status = NOT_STARTED
        event.clearEvents('keyboard')
        trialComponents = []
        trialComponents.append(dlWordTop)
        trialComponents.append(dlWordBtm)
        trialComponents.append(trialResp)
        for thisComponent in trialComponents:
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        continueRoutine = True
        while continueRoutine and routineTimer.getTime() > 0:
            t = trialClock.getTime()
            frameN = frameN + 1
            if t >= 0.0 and dlWordTop.status == NOT_STARTED:
                dlWordTop.tStart = t
                dlWordTop.frameNStart = frameN
                dlWordTop.setAutoDraw(True)
            if dlWordTop.status == STARTED and t >= (0.0 + (dlStimTime-win.monitorFramePeriod*0.75)):
                dlWordTop.setAutoDraw(False)
            if t >= 0.0 and dlWordBtm.status == NOT_STARTED:
                dlWordBtm.tStart = t
                dlWordBtm.frameNStart = frameN
                dlWordBtm.setAutoDraw(True)
            if dlWordBtm.status == STARTED and t >= (0.0 + (dlStimTime-win.monitorFramePeriod*0.75)):
                dlWordBtm.setAutoDraw(False)
            if t >= 0.0 and trialResp.status == NOT_STARTED:
                trialResp.tStart = t
                trialResp.frameNStart = frameN
                trialResp.status = STARTED
                trialResp.clock.reset()
                event.clearEvents(eventType='keyboard')
            if trialResp.status == STARTED and t >= (0.0 + (dlStimTime-win.monitorFramePeriod*0.75)):
                trialResp.status = STOPPED
            if trialResp.status == STARTED:
                theseKeys = event.getKeys(keyList=['2', '3', '4', '7', '8', '9'])
                if "escape" in theseKeys:
                    endExpNow = True
                if len(theseKeys) > 0:
                    trialResp.keys = theseKeys[-1]
                    trialResp.rt = trialResp.clock.getTime()
                    # Figure out which word was chosen
                    action = '--'
                    selWord = '--'
                    if expInfo['counterbalance'] == 0:
                        #<5 = top, >5 bottom
                        if trialResp.keys == '2' or trialResp.keys == '3' or trialResp.keys == '4' or trialResp.keys < 5:
                            action = 'top'
                            selWord = str( dlWordTop.text )
                            dlWordBtm.setColor(dimFontColor) # dim unselected word
                            dlWordTop.setColor(brightFontColor) # highlight selected word
                        elif trialResp.keys == '7' or trialResp.keys == '8' or trialResp.keys == '9' or trialResp.keys > 5:
                            action = 'btm'
                            selWord = str( dlWordBtm.text )
                            dlWordTop.setColor(dimFontColor) # dim unselected word
                            dlWordBtm.setColor(brightFontColor) # highlight selected word
                    elif expInfo['counterbalance'] == 1:
                        #<5 = bottom, >5 top
                        if trialResp.keys == '2' or trialResp.keys == '3' or trialResp.keys == '4' or trialResp.keys < 5:
                            action = 'btm'
                            selWord = str( dlWordBtm.text )
                            dlWordTop.setColor(dimFontColor) # dim unselected word
                            dlWordBtm.setColor(brightFontColor) # highlight selected word
                        elif trialResp.keys == '7' or trialResp.keys == '8' or trialResp.keys == '9' or trialResp.keys > 5:
                            action = 'top'
                            selWord = str( dlWordTop.text )
                            dlWordBtm.setColor(dimFontColor) # dim unselected word
                            dlWordTop.setColor(brightFontColor) # highlight selected word
                    if str(trialResp.keys) == str(corResp):
                        trialAcc = 1
                        curReward += rewValue
                    else:
                        trialAcc = 0
                        curReward -= rewValue
            if not continueRoutine:
                break
            continueRoutine = False
            for thisComponent in trialComponents:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break
            if endExpNow or event.getKeys(keyList=["escape"]):
                core.quit()
            if continueRoutine:
                win.flip()
        for thisComponent in trialComponents:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        dlTrials.addData('dl.selection', selWord)
        dlTrials.addData('dl.keys', trialResp.keys)
        dlTrials.addData('dl.action', action)
        if trialResp.keys in ['', [], None]:
           trialResp.keys=None
        if trialResp.keys != None:
            dlTrials.addData('dl.acc', trialAcc)
            dlTrials.addData('dl.rt', trialResp.rt)
        else:
            trialAcc = -1 # for feedback display
            dlTrials.addData('dl.acc', 'noresp')
            dlTrials.addData('dl.rt', 0)
        
        #~~~| DL fix (in place of feedback |~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
        
        # Begin feedback routine
        t = 0
        feedbackClock.reset() 
        frameN = -1
        routineTimer.add(dlFdbkTime)
        feedbackComponents = []
        feedbackComponents.append(jitterText)
        for thisComponent in feedbackComponents:
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        continueRoutine = True
        while continueRoutine and routineTimer.getTime() > 0:
            t = feedbackClock.getTime()
            frameN = frameN + 1
            if t >= 0.0 and jitterText.status == NOT_STARTED:
                jitterText.tStart = t
                jitterText.frameNStart = frameN
                jitterText.setAutoDraw(True)
            if jitterText.status == STARTED and t >= (0.0 + (dlFdbkTime-win.monitorFramePeriod*0.75)):
                jitterText.setAutoDraw(False)
            if not continueRoutine:
                break
            continueRoutine = False
            for thisComponent in feedbackComponents:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break
            if endExpNow or event.getKeys(keyList=["escape"]):
                core.quit()
            if continueRoutine:
                win.flip()
        for thisComponent in feedbackComponents:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        
        #~~~| DL fix (pre NBack) |~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
        t = 0
        jitterClock.reset() 
        frameN = -1
        event.clearEvents('keyboard')
        triggerCatch = event.BuilderKeyResponse()
        triggerCatch.status = NOT_STARTED
        jitterComponents = []
        jitterComponents.append(jitterText)
        jitterComponents.append(triggerCatch)
        for thisComponent in jitterComponents:
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        continueRoutine = True
        while continueRoutine:
            t = jitterClock.getTime()
            frameN = frameN + 1
            if t >= 0.0 and jitterText.status == NOT_STARTED:
                jitterText.tStart = t
                jitterText.frameNStart = frameN
                jitterText.setAutoDraw(True)
            if t >= 0.0 and triggerCatch.status == NOT_STARTED:
                triggerCatch.tStart = t
                triggerCatch.frameNStart = frameN
                triggerCatch.status = STARTED
                triggerCatch.clock.reset()
                event.clearEvents(eventType='keyboard')
            if triggerCatch.status == STARTED:
                theseKeys = event.getKeys(keyList=['lshift'])
                if "escape" in theseKeys:
                    endExpNow = True
                if len(theseKeys) > 0:
                    triggerCatch.keys = theseKeys[-1]
                    triggerCatch.rt = triggerCatch.clock.getTime()
                    continueRoutine = False
            if not continueRoutine:
                break
            continueRoutine = False
            for thisComponent in jitterComponents:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break
            if endExpNow or event.getKeys(keyList=["escape"]):
                core.quit()
            if continueRoutine:
                win.flip()
        for thisComponent in jitterComponents:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        routineTimer.reset()
        
        #~~~| NBack Loop |~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
        nBackWords = [ str( thisDlTrial['nBackWord1'] ), str( thisDlTrial['nBackWord2'] ), str( thisDlTrial['nBackWord3'] ), str( thisDlTrial['nBackWord4'] ), str( thisDlTrial['nBackWord5'] ), str( thisDlTrial['nBackWord6'] ), str( thisDlTrial['nBackWord7'] )]
        # Set up NBack Loop
        nBackLoop = data.TrialHandler(
            nReps=dlNBackTrials,
            method='sequential',
            extraInfo=expInfo,
            originPath=None,
            trialList=[None],
            name='nBackLoop'
        )
        thisNBackLoop = nBackLoop.trialList[0]
        
        for thisNBackLoop in nBackLoop:
            # Set word for this trial
            nbWord.setText(nBackWords[nBackLoop.thisN])
            
            #~~~| NBack Trial |~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
            t = 0
            nBackDispClock.reset() 
            frameN = -1
            routineTimer.add(nbTrialTime)
            nbResp = event.BuilderKeyResponse()
            nbResp.status = NOT_STARTED
            nBackDispComponents = []
            nBackDispComponents.append(nbWord)
            nBackDispComponents.append(nbResp)
            for thisComponent in nBackDispComponents:
                if hasattr(thisComponent, 'status'):
                    thisComponent.status = NOT_STARTED
            continueRoutine = True
            while continueRoutine and routineTimer.getTime() > 0:
                t = nBackDispClock.getTime()
                frameN = frameN + 1
                if t >= 0.0 and nbWord.status == NOT_STARTED:
                    nbWord.tStart = t
                    nbWord.frameNStart = frameN
                    nbWord.setAutoDraw(True)
                if nbWord.status == STARTED and t >= (0.0 + (nbTrialTime-win.monitorFramePeriod*0.75)):
                    nbWord.setAutoDraw(False)
                if t >= 0.0 and nbResp.status == NOT_STARTED:
                    nbResp.tStart = t
                    nbResp.frameNStart = frameN
                    nbResp.status = STARTED
                    nbResp.clock.reset()
                    event.clearEvents(eventType='keyboard')
                if nbResp.status == STARTED and t >= (0.0 + (nbTrialTime-win.monitorFramePeriod*0.75)):
                    nbResp.status = STOPPED
                if nbResp.status == STARTED:
                    theseKeys = event.getKeys(keyList=['2', '3', '4', '7', '8', '9'])
                    if "escape" in theseKeys:
                        endExpNow = True
                    if len(theseKeys) > 0:
                        nbResp.keys = theseKeys[-1]
                        nbResp.rt = nbResp.clock.getTime()
                if not continueRoutine:
                    break
                continueRoutine = False
                for thisComponent in nBackDispComponents:
                    if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                        continueRoutine = True
                        break
                if endExpNow or event.getKeys(keyList=["escape"]):
                    core.quit()
                if continueRoutine:
                    win.flip()
            for thisComponent in nBackDispComponents:
                if hasattr(thisComponent, "setAutoDraw"):
                    thisComponent.setAutoDraw(False)
            if nbResp.keys in ['', [], None]:
               nbResp.keys=None
            dlTrials.addData('nb.keys',nbResp.keys)
            if nbResp.keys != None:
                dlTrials.addData('nb.rt', nbResp.rt)
            
            #~~~| NBack Fix |~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
            t = 0
            nBackFixClock.reset()
            frameN = -1
            routineTimer.add(nbFixTime)
            nBackFixComponents = []
            nBackFixComponents.append(nbFix)
            for thisComponent in nBackFixComponents:
                if hasattr(thisComponent, 'status'):
                    thisComponent.status = NOT_STARTED
            continueRoutine = True
            while continueRoutine and routineTimer.getTime() > 0:
                t = nBackFixClock.getTime()
                frameN = frameN + 1
                if t >= 0.0 and nbFix.status == NOT_STARTED:
                    nbFix.tStart = t
                    nbFix.frameNStart = frameN
                    nbFix.setAutoDraw(True)
                if nbFix.status == STARTED and t >= (0.0 + (nbFixTime-win.monitorFramePeriod*0.75)):
                    nbFix.setAutoDraw(False)
                if not continueRoutine:
                    break
                continueRoutine = False
                for thisComponent in nBackFixComponents:
                    if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                        continueRoutine = True
                        break
                if endExpNow or event.getKeys(keyList=["escape"]):
                    core.quit()
                if continueRoutine:
                    win.flip()
            for thisComponent in nBackFixComponents:
                if hasattr(thisComponent, "setAutoDraw"):
                    thisComponent.setAutoDraw(False)
            # Next NBack Trial
#            dlExp.nextEntry()
            
        # Next DL trial
        dlExp.nextEntry()
        
    #~~~| End Run Baseline |~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
    baselineLoop = data.TrialHandler(
        nReps=dlBaselineScans,
        method='sequential', 
        extraInfo=expInfo,
        trialList=[None],
        name='baselineLoop'
    )
    thisBaselineLoop = baselineLoop.trialList[0]
    
    for thisBaselineLoop in baselineLoop:
        t = 0
        jitterClock.reset()
        frameN = -1
        event.clearEvents(eventType='keyboard')
        triggerCatch = event.BuilderKeyResponse()
        triggerCatch.status = NOT_STARTED
        jitterComponents = []
        jitterComponents.append(jitterText)
        jitterComponents.append(triggerCatch)
        for thisComponent in jitterComponents:
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        continueRoutine = True
        while continueRoutine:
            t = jitterClock.getTime()
            frameN = frameN + 1
            if t >= 0.0 and jitterText.status == NOT_STARTED:
                jitterText.tStart = t
                jitterText.frameNStart = frameN
                jitterText.setAutoDraw(True)
            if t >= 0.0 and triggerCatch.status == NOT_STARTED:
                triggerCatch.tStart = t
                triggerCatch.frameNStart = frameN
                triggerCatch.status = STARTED
                triggerCatch.clock.reset()
                event.clearEvents(eventType='keyboard')
            if triggerCatch.status == STARTED:
                theseKeys = event.getKeys(keyList=['lshift'])
                if "escape" in theseKeys:
                    endExpNow = True
                if len(theseKeys) > 0:
                    triggerCatch.keys = theseKeys[-1]
                    triggerCatch.rt = triggerCatch.clock.getTime()
                    continueRoutine = False
            if not continueRoutine:
                break
            continueRoutine = False
            for thisComponent in jitterComponents:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break
            if endExpNow or event.getKeys(keyList=["escape"]):
                core.quit()
            if continueRoutine:
                win.flip()
        for thisComponent in jitterComponents:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        if triggerCatch.keys in ['', [], None]:
           triggerCatch.keys=None
        routineTimer.reset()
        # Next baseline scan
#        dlExp.nextEntry()
    
    #~~~| Run break screen |~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
    # Set up screen text
    if dlBlock2Runs.thisN < 3:
        instructText.setText(sDlBreakText)
        t = 0
        instructClock.reset() 
        frameN = -1
        event.clearEvents(eventType='keyboard')
        contResp = event.BuilderKeyResponse()
        contResp.status = NOT_STARTED
        instructComponents = []
        instructComponents.append(instructText)
        instructComponents.append(contResp)
        for thisComponent in instructComponents:
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        continueRoutine = True
        while continueRoutine:
            t = instructClock.getTime()
            frameN = frameN + 1
            if t >= 0.0 and instructText.status == NOT_STARTED:
                instructText.tStart = t
                instructText.frameNStart = frameN
                instructText.setAutoDraw(True)
            if t >= 0.0 and contResp.status == NOT_STARTED:
                contResp.tStart = t
                contResp.frameNStart = frameN
                contResp.status = STARTED
                contResp.clock.reset()
                event.clearEvents(eventType='keyboard')
            if contResp.status == STARTED:
                theseKeys = event.getKeys(keyList=['space'])
                if "escape" in theseKeys:
                    endExpNow = True
                if len(theseKeys) > 0:
                    contResp.keys = theseKeys[-1]
                    contResp.rt = contResp.clock.getTime()
                    continueRoutine = False
            if not continueRoutine:
                break
            continueRoutine = False
            for thisComponent in instructComponents:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break
            if endExpNow or event.getKeys(keyList=["escape"]):
                core.quit()
            if continueRoutine:
                win.flip()
        for thisComponent in instructComponents:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        if contResp.keys in ['', [], None]:
           contResp.keys=None
        routineTimer.reset()
    
    # Next Run
    dlExp.nextEntry()

#~~~| Goodbye Screen |~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
if curReward > 15:
    curReward = 15.0

if curReward < 0:
    sDlFinalDisplay = ('Unfortunately, you didn\'t earn any bonus :(\n\nBut you finished! We have one more short task for you. The experimenter will check on you shortly.')
else:
    sDlFinalDisplay = ('Great job! You\'ve made an additional $%s!\n\nWe have one more short task for you. The experimenter will check on you shortly.' %(curReward) )

finishText.setText( sDlFinalDisplay )

t = 0
finishClock.reset()
frameN = -1
event.clearEvents(eventType='keyboard')
endResp = event.BuilderKeyResponse()
endResp.status = NOT_STARTED
finishComponents = []
finishComponents.append(finishText)
finishComponents.append(endResp)
for thisComponent in finishComponents:
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED
continueRoutine = True
while continueRoutine:
    t = finishClock.getTime()
    frameN = frameN + 1
    if t >= 0.0 and finishText.status == NOT_STARTED:
        finishText.tStart = t
        finishText.frameNStart = frameN
        finishText.setAutoDraw(True)
    if t >= 0.0 and endResp.status == NOT_STARTED:
        endResp.tStart = t
        endResp.frameNStart = frameN
        endResp.status = STARTED
        endResp.clock.reset()
        event.clearEvents(eventType='keyboard')
    if endResp.status == STARTED:
        theseKeys = event.getKeys(keyList=['q', 'Q'])
        if "escape" in theseKeys:
            endExpNow = True
        if len(theseKeys) > 0:
            endResp.keys = theseKeys[-1]
            endResp.rt = endResp.clock.getTime()
            continueRoutine = False
    if not continueRoutine:
        break
    continueRoutine = False
    for thisComponent in finishComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break
    if endExpNow or event.getKeys(keyList=["escape"]):
        core.quit()
    if continueRoutine:
        win.flip()
for thisComponent in finishComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
if endResp.keys in ['', [], None]:
   endResp.keys=None
routineTimer.reset()
win.close()
core.quit()
