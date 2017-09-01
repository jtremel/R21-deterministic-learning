#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Deterministic Learning Localizer Task (version 1.0.0)

This requires 12 list files (1 for each run), generated from the LocListGen v5+ Excel macro

~~ Version Info ~~
0.1.0: Jan 31, 2017, initial development version
1.0.0: Feb 6, 2017, ready for scanning

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
import os

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# User options
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# Experiment Name
expName = 'DL Localizer'
# Experiment Info Collection
expInfo = {'subject':'','counterbalance':0}
# Experiment Version
expVersion='1.0.0'

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
# Font size for stimuli (word text), in pixels
stimFontSize = 45
# Font size for normal text (instructions), in pixels
textFontSize = 24
# Font size for fixation cross, in pixels
fixhFontSize = 80
# Set this to True if stimulus text should be bold
bStimTextBold=False
# Font color for normal text
fontColor = 'lightgray'
# Font color for stimulus text
stimFontColor = 'black'

# ~~~~~~ Image Properties ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# Image stimulus resolution
imgW = 900
imgH = 600

fixBoxColor = 'gray'
wordBoxColor = 'lightgray'

# ~~~~~~ Timing Properties ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# Length of stimulus display period (in seconds)
stimTime = 2.0

# ~~~~~~ Experiment Properties ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# Number of discarded acquisitions at start of run (usually 3)
nDiscard = 3
# Number of acquisitions for passive baseline phase of block (usually 6)
nPassive = 6

# ~~~~~~ Task Instructions ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
sInstructionsC0 = ('For this task, you\'re going to see a series of images and words. When you see a repeat, '+
'press the button under your RIGHT index finger. Otherwise, don\'t press a button, but pay attention to the image '+
'or word being presented. When looking at the images, try to look at the whole image and not just a piece of it. The '+
'images and words will be on the screen for about 2 seconds each.\n\n'+
'This is the last scan and takes about 10 minutes. After this, we\'ll get you out of the scanner!\n\n'+
'The experimenter will check in with you in a moment.')

sInstructionsC1 = ('For this task, you\'re going to see a series of images and words. When you see a repeat, '+
'press the button under your LEFT index finger. Otherwise, don\'t press a button, but pay attention to the image '+
'or word being presented. When looking at the images, try to look at the whole image and not just a piece of it. The '+
'images and words will be on the screen for about 2 seconds each.\n\n'+
'This is the last scan and takes about 10 minutes. After this, we\'ll get you out of the scanner!\n\n'+
'The experimenter will check in with you in a moment.')

sFinishText = ('Congratulations, you have finished the scan!\n\nSomeone will be in to get you out of the scanner shortly.')

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# Experiment Setup
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# Ensure that relative paths start from the same directory as this script
_thisDir = os.path.dirname(os.path.abspath(__file__))
os.chdir(_thisDir)

# Set up experiment files and info
dlg = gui.DlgFromDict(dictionary=expInfo, title=expName)
if dlg.OK == False: core.quit()

inFile = gui.fileOpenDlg(prompt='Select all 12 list files for the localizer:', allowed="CSV files (.csv)|*.csv", tryFilePath=_thisDir)
if inFile == None: core.quit()
if len(inFile) != 12:
    core.quit()

expInfo['date'] = data.getDateStr()
expInfo['expName'] = expName
expInfo['expVersion'] = expVersion
endExpNow = False # flag for experiment kill switch

# Set up data dir and file
if not os.path.isdir('__data'):
    os.makedirs('__data')
filenameLoc = _thisDir + os.sep + '__data' + os.path.sep + 's%s_%s_v%s__%s' %( expInfo.get('subject'), 'Loc', expVersion, expInfo['date'])
logFile = logging.LogFile(filenameLoc+'.log', level=logging.DEBUG)
logging.console.setLevel(logging.WARNING)

# Set up experiment manager
locExp = data.ExperimentHandler(
    name=expName,
    version=expVersion,
    extraInfo=expInfo,
    dataFileName=filenameLoc
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
catchClock = core.Clock()
stimClock = core.Clock()
globalClock = core.Clock()
routineTimer = core.CountdownTimer()

# Run and trial loop handlers



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
fixText = visual.TextStim(
    win=win,
    name='fixText',
    text='+',
    font='Arial',
    units='pix',
    height=fixhFontSize,
    bold=bStimTextBold,
    color=fontColor,
    colorSpace='rgb'
)
fixBox = visual.Rect(
    win=win,
    name='fixBox',
    width=imgW,
    height=imgH,
    lineWidth=1,
    lineColor=fixBoxColor,
    lineColorSpace='rgb',
    fillColor=fixBoxColor,
    fillColorSpace = 'rgb',
    opacity = 1.0,
    interpolate = True,
    units='pix'
)
stimImage = visual.ImageStim(
    win=win,
    name='stimImage',
    size=[imgW, imgH],
    units='pix',
    interpolate=True
)
stimWord = visual.TextStim(
    win=win,
    name='stimWord',
    text='WORD',
    font='Arial',
    pos=[0,0],
    units='pix',
    height=stimFontSize,
    color=stimFontColor,
    colorSpace='rgb'
)
stimBox = visual.Rect(
    win=win,
    name='stimBox',
    units='pix',
    width=imgW,
    height=imgH,
    lineWidth=1,
    lineColor=wordBoxColor,
    lineColorSpace='rgb',
    fillColor=wordBoxColor,
    fillColorSpace='rgb',
    opacity=1.0,
    interpolate = True
)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# Run experiment
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#~~| Loc Instructions |~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
if expInfo['counterbalance'] == 0:
    instructText.setText( sInstructionsC0)
elif expInfo['counterbalance'] == 1:
    instructText.setText( sInstructionsC1)
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
    contResp.keys = None
routineTimer.reset()

# Loop the fixation for 3 discard acquisitions at the beginning of each run
discardLoop = data.TrialHandler(
    nReps=nDiscard,
    method='sequential', 
    extraInfo=expInfo,
    trialList=[None],
    name='discardLoop')
thisDiscardLoop = discardLoop.trialList[0]
for thisDiscardLoop in discardLoop:
    t = 0
    catchClock.reset()
    frameN = -1
    event.clearEvents(eventType='keyboard')
    triggerResp = event.BuilderKeyResponse()
    triggerResp.status = NOT_STARTED
    catchComponents = []
    catchComponents.append(fixBox)
    catchComponents.append(fixText)
    catchComponents.append(triggerResp)
    for thisComponent in catchComponents:
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    continueRoutine = True
    while continueRoutine:
        t = catchClock.getTime()
        frameN = frameN + 1
        if t >= 0.0 and fixBox.status == NOT_STARTED:
            fixBox.tStart = t
            fixBox.frameNStart = frameN
            fixBox.setAutoDraw(True)
        if t >= 0.0 and fixText.status == NOT_STARTED:
            fixText.tStart = t
            fixText.frameNStart = frameN
            fixText.setAutoDraw(True)
        if t >= 0.0 and triggerResp.status == NOT_STARTED:
            triggerResp.tStart = t 
            triggerResp.frameNStart = frameN
            triggerResp.status = STARTED
            event.clearEvents(eventType='keyboard')
        if triggerResp.status == STARTED:
            theseKeys = event.getKeys(keyList=['lshift'])
            if "escape" in theseKeys:
                endExpNow = True
            if len(theseKeys) > 0:
                continueRoutine = False
        if not continueRoutine:
            break
        continueRoutine = False
        for thisComponent in catchComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break
        if endExpNow or event.getKeys(keyList=["escape"]):
            core.quit()
        if continueRoutine:
            win.flip()
    for thisComponent in catchComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    routineTimer.reset()

# Loop for 12 blocks
blockLoop = data.TrialHandler(
    nReps=12,
    method='sequential', 
    extraInfo=expInfo,
    trialList=[None],
    name='blockLoop'
)
#locExp.addLoop(blockLoop)
thisBlockLoop = blockLoop.trialList[0]
for thisBlockLoop in blockLoop:
    currentLoop = blockLoop
    activePhase = data.TrialHandler(
        nReps=1,
        method='sequential', 
        extraInfo=expInfo,
        trialList=data.importConditions( str( inFile[blockLoop.thisN] ) ),
        name='activePhase'
    )
    locExp.addLoop(activePhase)
    thisActivePhase = activePhase.trialList[0]
    
    for thisActivePhase in activePhase:
        currentLoop = activePhase
        if int(thisActivePhase['jitter']) > 0:
            # Loop jitter fixation for N times, set by input list
            jitterLoop = data.TrialHandler(
                nReps=int(thisActivePhase['jitter']), 
                method='sequential', 
                extraInfo=expInfo,
                trialList=[None],
                name='jitterLoop'
            )
            thisJitterLoop = jitterLoop.trialList[0]
            
            for thisJitterLoop in jitterLoop:
                t = 0
                catchClock.reset()
                frameN = -1
                event.clearEvents(eventType='keyboard')
                triggerResp = event.BuilderKeyResponse()
                triggerResp.status = NOT_STARTED
                catchComponents = []
                catchComponents.append(fixBox)
                catchComponents.append(fixText)
                catchComponents.append(triggerResp)
                for thisComponent in catchComponents:
                    if hasattr(thisComponent, 'status'):
                        thisComponent.status = NOT_STARTED
                continueRoutine = True
                while continueRoutine:
                    t = catchClock.getTime()
                    frameN = frameN + 1
                    if t >= 0.0 and fixBox.status == NOT_STARTED:
                        fixBox.tStart = t
                        fixBox.frameNStart = frameN
                        fixBox.setAutoDraw(True)
                    if t >= 0.0 and fixText.status == NOT_STARTED:
                        fixText.tStart = t
                        fixText.frameNStart = frameN
                        fixText.setAutoDraw(True)
                    if t >= 0.0 and triggerResp.status == NOT_STARTED:
                        triggerResp.tStart = t 
                        triggerResp.frameNStart = frameN
                        triggerResp.status = STARTED
                        event.clearEvents(eventType='keyboard')
                    if triggerResp.status == STARTED:
                        theseKeys = event.getKeys(keyList=['lshift'])
                        if "escape" in theseKeys:
                            endExpNow = True
                        if len(theseKeys) > 0:
                            continueRoutine = False
                    if not continueRoutine:
                        break
                    continueRoutine = False
                    for thisComponent in catchComponents:
                        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                            continueRoutine = True
                            break
                    if endExpNow or event.getKeys(keyList=["escape"]):
                        core.quit()
                    if continueRoutine:
                        win.flip()
                for thisComponent in catchComponents:
                    if hasattr(thisComponent, "setAutoDraw"):
                        thisComponent.setAutoDraw(False)
                routineTimer.reset()
        
#~~~| Stim Disp |~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
        
        # Load stimulus
        if str( thisActivePhase['trialType']) == 'word':
            stimWord.setText( str( thisActivePhase['stim'] ) )
        if str( thisActivePhase['trialType']) == 'image':
            stimImage.setImage( str( thisActivePhase['stim'] ) )
        
        t = 0
        stimClock.reset()
        frameN = -1
        routineTimer.add(stimTime)
        stimResp = event.BuilderKeyResponse()
        stimResp.status = NOT_STARTED
        stimComponents = []
        if str( thisActivePhase['trialType']) == 'word':
            stimComponents.append(stimWord)
            stimComponents.append(stimBox)
        if str( thisActivePhase['trialType']) == 'image':
            stimComponents.append(stimImage)
        stimComponents.append(stimResp)
        for thisComponent in stimComponents:
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        continueRoutine = True
        while continueRoutine and routineTimer.getTime() > 0:
            t = stimClock.getTime()
            frameN = frameN + 1
            if str( thisActivePhase['trialType']) == 'word':
                if t >= 0.0 and stimBox.status == NOT_STARTED:
                    stimBox.tStart = t
                    stimBox.frameNStart = frameN
                    stimBox.setAutoDraw(True)
                if stimBox.status == STARTED and t >= (0.0 + (stimTime-win.monitorFramePeriod*0.75)):
                    stimBox.setAutoDraw(False)
                if t >= 0.0 and stimWord.status == NOT_STARTED:
                    stimWord.tStart = t
                    stimWord.frameNStart = frameN
                    stimWord.setAutoDraw(True)
                if stimWord.status == STARTED and t >= (0.0 + (stimTime-win.monitorFramePeriod*0.75)):
                    stimWord.setAutoDraw(False)
            if str( thisActivePhase['trialType']) == 'image':
                if t >= 0.0 and stimImage.status == NOT_STARTED:
                    stimImage.tStart = t
                    stimImage.frameNStart = frameN
                    stimImage.setAutoDraw(True)
                if stimImage.status == STARTED and t >= (0.0 + (stimTime-win.monitorFramePeriod*0.75)):
                    stimImage.setAutoDraw(False)
            if t >= 0.0 and stimResp.status == NOT_STARTED:
                stimResp.tStart = t
                stimResp.frameNStart = frameN
                stimResp.status = STARTED
                stimResp.clock.reset()
                event.clearEvents(eventType='keyboard')
            if stimResp.status == STARTED and t >= (0.0 + (stimTime-win.monitorFramePeriod*0.75)):
                stimResp.status = STOPPED
            if stimResp.status == STARTED:
                theseKeys = event.getKeys(keyList=['2', '3', '4', '7', '8', '9'])
                if "escape" in theseKeys:
                    endExpNow = True
                if len(theseKeys) > 0:
                    stimResp.keys = theseKeys[-1]
                    stimResp.rt = stimResp.clock.getTime()
            if not continueRoutine:
                break
            continueRoutine = False
            for thisComponent in stimComponents:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break
            if endExpNow or event.getKeys(keyList=["escape"]):
                core.quit()
            if continueRoutine:
                win.flip()
        for thisComponent in stimComponents:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        if stimResp.keys in ['', [], None]:
           stimResp.keys=None
        activePhase.addData('loc.keys',stimResp.keys)
        if stimResp.keys != None:
            activePhase.addData('loc.rt', stimResp.rt)
        locExp.nextEntry()
        # end active phase list
        
#~| Passive Phase |~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
    passivePhase = data.TrialHandler(
        nReps=nPassive,
        method='sequential', 
        extraInfo=expInfo,
        trialList=[None],
        name='passivePhase'
    )
    thisPassivePhase = passivePhase.trialList[0]
    for thisPassivePhase in passivePhase:
        currentLoop = passivePhase
        t = 0
        catchClock.reset()
        frameN = -1
        event.clearEvents(eventType='keyboard')
        triggerResp = event.BuilderKeyResponse()
        triggerResp.status = NOT_STARTED
        catchComponents = []
        catchComponents.append(fixBox)
        catchComponents.append(fixText)
        catchComponents.append(triggerResp)
        for thisComponent in catchComponents:
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        continueRoutine = True
        while continueRoutine:
            t = catchClock.getTime()
            frameN = frameN + 1
            if t >= 0.0 and fixBox.status == NOT_STARTED:
                fixBox.tStart = t
                fixBox.frameNStart = frameN
                fixBox.setAutoDraw(True)
            if t >= 0.0 and fixText.status == NOT_STARTED:
                fixText.tStart = t
                fixText.frameNStart = frameN
                fixText.setAutoDraw(True)
            if t >= 0.0 and triggerResp.status == NOT_STARTED:
                triggerResp.tStart = t 
                triggerResp.frameNStart = frameN
                triggerResp.status = STARTED
                event.clearEvents(eventType='keyboard')
            if triggerResp.status == STARTED:
                theseKeys = event.getKeys(keyList=['lshift'])
                if "escape" in theseKeys:
                    endExpNow = True
                if len(theseKeys) > 0:
                    continueRoutine = False
            if not continueRoutine:
                break
            continueRoutine = False
            for thisComponent in catchComponents:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break
            if endExpNow or event.getKeys(keyList=["escape"]):
                core.quit()
            if continueRoutine:
                win.flip()
        for thisComponent in catchComponents:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        routineTimer.reset()
    # end passive phase
# end block, repeat if necessary

#~~| Final Screen |~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
instructText.setText( sFinishText )
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
        theseKeys = event.getKeys(keyList=['q','Q'])
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
    contResp.keys = None
routineTimer.reset()

win.close()
core.quit()
