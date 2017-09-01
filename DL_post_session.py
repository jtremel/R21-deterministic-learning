#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Deterministic Learning Post-Learning Behavioral Session (version 5.0.0)

XXXXX Description Here XXXXX

Note, input list files for the post tests from the ListGen v5+ require you to paste in the selected words from the 
DL scan session data file.

~~ Version Info ~~
5.0.0: Jan 27, 2017, pulled post-learning experiments out of main file to separate session script.

~~ PsychoPy Version Info and Citations ~~
Developed for PsychoPy2 v1.82.01
  Peirce, JW (2007) PsychoPy - Psychophysics software in Python. 
    Journal of Neuroscience Methods, 162(1-2), 8-13.
  Peirce, JW (2009) Generating stimuli for neuroscience using PsychoPy. 
    Frontiers in Neuroinformatics, 2:10. doi: 10.3389/neuro.11.010.2008




TODO:
    localizer imaging rating
    list for localizer images




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
expName = 'DL Behavioral Post-Scan Session v500 series'
# Experiment Info Collection
expInfo = {'subject':''}
# Experiment Version
expVersion='5.0.0'

# ~~~~~~ Window Properties ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# Window resolution width
displayW = 1680
# Window resolution height
displayH = 1050
# Background color
bgColor = [-0.7,-0.7,-0.7]
# Size of space to use on display, width
windowFractionW = 0.9
# Size of space to use on display, height
windowFractionH = 0.9

# ~~~~~~ Text Properties ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# Font size for stimuli (words and feedback text), in pixels
stimFontSize = 50
# Font size for normal text (instructions, break screen, finish), in pixels
textFontSize = 28
# Font size for fixation cross, in pixels
fixhFontSize = 100
# Set this to True if stimulus text should be bold
bStimTextBold=False
# Font color for normal text
fontColor = 'lightgray'

# ~~~~~~ Image Properties ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# Background image resolution
imgW = 1200
imgH = 800
# Size of semi-transparent background box for text display
boxW = 300
boxH = 300
# Opacity of background box (1.0 = opaque)
boxOpacity = 0.5

# Face Sort image size width and height
fsImgW = 300
fsImgH = 300

# ~~~~~~ Timing Properties ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# Length of inter-stimulus interval (fixation), in seconds
dmFixTime = 0.75
fsFixTime = 1.0
# Length of stimulus display (trial), in seconds
fsWordTime = 0.3
fsFaceTime = 1.5

# ~~~~~~ Experiment Properties ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# Number of runs for face sort task
nFsRuns = 2
# Number of times to repeat the face sort list within each run
fsListReps = 1

# ~~~~~~ Task Instructions ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
sDmInstructions = ('For this task, you will see one word at a time. You\'ll have to answer three '+
'questions about each word. First, you\'ll be asked if you recognize the word from the first task you did. '+
'Second, you\'ll be asked whether you made a correct or incorrect response the first time you saw the word. '+
'Last, you\'ll be asked whether the word was presented with a face image or a house image in the first task.\n\n'+
'The questions and response options will be on the screen, so no need to memorize anything now. You can press '+
'\'1\' for \'yes\' or \'2\' for \'no\'. If you have no idea whatsoever, you can press \'3\' for \'guess\'.\n\n'
'The experimenter will give you some additional instructions and let you know when you can start.')

sFsInstructions = ('Now, you are going to see pictures of faces and will make a judgment about them. Before you see the face, '+
'you will see a word flash up quickly. Read the word to yourself when you see it. After the word, you will see a face.\n\n'+
'These faces will be expressing a good or bad emotion. All you need to do is identify whether the person is feeling good or bad. '+
'When the face appears, you will have a limited amount of time to respond, so respond as quickly as possible.'+
'\n\nIf the face shows a GOOD emotion, press \'Left Ctrl\'.\nIf the face shows a BAD emotion, press \'Right Ctrl\'.\n\n'+
'Half-way through, you will be able to take a short break. After this break, the responses will switch, and '+
'you\'ll use \'Right Ctrl\' for \'good\' and \'Left Ctrl\' for \'bad\' (you\'ll be reminded at the break).\n\n'+
'The experimenter will give you some additional instructions and let you know when you can start.')

sFsBreakText = ('Take a short break.\n\nFor the rest of this task, the responses will switch.\n\n'+
'Press \'Left Ctrl\' if the face shows a BAD emotion.\nPress \'Right Ctrl\' if the face shows a GOOD emotion.\n\n'+
'When you\'re ready to continue, press SPACE')

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# Experiment Setup
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# Ensure that relative paths start from the same directory as this script
_thisDir = os.path.dirname(os.path.abspath(__file__))
os.chdir(_thisDir)

# Set up experiment files and info
dlg = gui.DlgFromDict(dictionary=expInfo, title=expName)
if dlg.OK == False: core.quit()

inFileDM = gui.fileOpenDlg(prompt='Select Delayed Memory List file', allowed="CSV files (.csv)|*.csv", tryFilePath=_thisDir)
if inFileDM == None: core.quit()
inFileDM = inFileDM[0]

inFileFS = gui.fileOpenDlg(prompt='Select FaceSort List file', allowed="CSV files (.csv)|*.csv", tryFilePath=_thisDir)
if inFileFS == None: core.quit()
inFileFS = inFileFS[0]

expInfo['date'] = data.getDateStr()
expInfo['expName'] = expName
expInfo['expVersion'] = expVersion
endExpNow = False # flag for experiment kill switch

# Set up extras for data caching
rcgResp = ''
rcgAcc = -1
rcgRt = 0
epiResp = ''
epiAcc = -1
epiRt = 0
ascResp = ''
ascAcc = -1
ascRt = 0

# Set up data directory and data file
if not os.path.isdir('__data'):
    os.makedirs('__data')
filenameDM = _thisDir + os.sep + '__data' + os.path.sep + 's%s_%s_v%s__%s' %( expInfo.get('subject'), 'DM', expVersion, expInfo['date'])
filenameFS = _thisDir + os.sep + '__data' + os.path.sep + 's%s_%s_v%s__%s' %( expInfo.get('subject'), 'FS', expVersion, expInfo['date'])
filenameLog = _thisDir + os.sep + '__data' + os.path.sep + 's%s_expt_v%s__%s' %( expInfo.get('subject'), expVersion, expInfo['date'])
logFile = logging.LogFile(filenameLog+'.log', level=logging.DEBUG)
logging.console.setLevel(logging.WARNING)

# Set up Experiment Managers
dmExp = data.ExperimentHandler(
    name='dm',
    version=expVersion,
    extraInfo=expInfo,
    dataFileName=filenameDM
)
fsExp = data.ExperimentHandler(
    name='fs',
    version=expVersion,
    extraInfo=expInfo,
    dataFileName=filenameFS
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
globalClock = core.Clock()
routineTimer = core.CountdownTimer()
instructClock = core.Clock()
goodbyeClock = core.Clock()
fixClock = core.Clock()
dmClock = core.Clock()
fsWordClock = core.Clock()
fsFaceClock = core.Clock()

fsRuns = data.TrialHandler(
    nReps=nFsRuns,
    method='sequential',
    extraInfo=expInfo,
    trialList=[None],
    name='fsRuns'
)

# Set up trial loops
dmTrials = data.TrialHandler(
    nReps=1,
    method='random',
    extraInfo=expInfo,
    trialList=data.importConditions( str(inFileDM) ),
    name='dmTrials'
)
fsTrials = data.TrialHandler(
    nReps=fsListReps,
    method='random',
    extraInfo=expInfo,
    trialList=data.importConditions( str(inFileFS) ),
    name='fsTrials'
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
dlWordTop = visual.TextStim(
    win=win,
    name='dlWordTop',
    text='',
    font='Arial',
    bold=bStimTextBold,
    pos=[0, (imgH*0.5 + 30)],
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
    size=[imgW, imgH],
    units='pix',
    interpolate=True
)
dmRcgText = visual.TextStim(
    win=win,
    name='dmRcgText',
    text='Do you recognize this from the first task? Yes (1) or No (2)',
    font='Arial',
    bold=bStimTextBold,
    pos=[0,(imgH*0.5 + 30)],
    units='pix',
    height=textFontSize,
    color=fontColor,
    colorSpace='rgb',
    wrapWidth=int( round( displayW*windowFractionW, -1) )
)
dmEpiText = visual.TextStim(
    win=win,
    name='dmEpiText',
    text='Did you respond correctly the first time you saw this? Yes (1) or No (2)',
    font='Arial',
    bold=bStimTextBold,
    pos=[0,(imgH*0.5 + 30)],
    units='pix',
    height=textFontSize,
    color=fontColor,
    colorSpace='rgb',
    wrapWidth=int( round( displayW*windowFractionW, -1) )
)
dmAscText = visual.TextStim(
    win=win,
    name='dmAscText',
    text='Is this a correct word + imaging pairing? Yes (1) or No (2)',
    font='Arial',
    bold=bStimTextBold,
    pos=[0,(imgH*0.5 + 30)],
    units='pix',
    height=textFontSize,
    color=fontColor,
    colorSpace='rgb',
    wrapWidth=int( round( displayW*windowFractionW, -1) )
)
fsText = visual.TextStim(
    win=win,
    name='fsText',
    text='WORD',
    font='Arial',
    bold=bStimTextBold,
    units='pix',
    height=stimFontSize,
    color=fontColor,
    colorSpace='rgb'
)
fsImage = visual.ImageStim(
    win=win,
    name='fsImage',
    size=[fsImgW, fsImgH],
    units='pix',
    interpolate=True
)
goodbyeText = visual.TextStim(
    win=win,
    name='goodbyeText',
    text='Congratulations! You are done!',
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
#~~| DM Instructions |~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
instructText.setText( sDmInstructions )
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

#~~| DM Trial Loop |~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
dmTrials = data.TrialHandler(
    nReps=1,
    method='random',
    extraInfo=expInfo,
    trialList=data.importConditions( str(inFileDM) ),
    name='dmTrials'
)
dmExp.addLoop(dmTrials)
thisDmTrial = dmTrials.trialList[0]

# Move word display to screen center
dlWordTop.setPos([0, 0])


for thisDmTrial in dmTrials:
    currentLoop = dmTrials
#~~~| DM Fixation |~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
    t = 0
    fixClock.reset() 
    frameN = -1
    routineTimer.add(dmFixTime)
    fixComponents = []
    fixComponents.append(fixText)
    for thisComponent in fixComponents:
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    continueRoutine = True
    while continueRoutine and routineTimer.getTime() > 0:
        t = fixClock.getTime()
        frameN = frameN + 1
        if t >= 0.0 and fixText.status == NOT_STARTED:
            fixText.tStart = t
            fixText.frameNStart = frameN
            fixText.setAutoDraw(True)
        if fixText.status == STARTED and t >= (0.0 + (dmFixTime-win.monitorFramePeriod*0.75)):
            fixText.setAutoDraw(False)
        if not continueRoutine:
            break
        continueRoutine = False
        for thisComponent in fixComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break
        if endExpNow or event.getKeys(keyList=["escape"]):
            core.quit()
        if continueRoutine:
            win.flip()
    for thisComponent in fixComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    
#~~~| DM Recognition Probe |~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
    # set word
    dlWordTop.setText( str(thisDmTrial['word']) )
    # set image
    dlImage.setImage( str( thisDmTrial['image'] ) )
    
    # check trial type
    if str( thisDmTrial['trialType'] ) == 'word' and str( thisDmTrial['ascCorr'] ) == 'no':
        dlImage.setImage( str( thisDmTrial['altStim'] ) )
    if str( thisDmTrial['trialType'] ) == 'image' and str( thisDmTrial['ascCorr'] ) == 'no':
        dlWordTop.setText( str( thisDmTrial['altStim'] ) )
    
    rcgResp = ''
    rcgAcc = 0
    rcgRt = 0
    t = 0
    dmClock.reset()
    frameN = -1
    trialResp = event.BuilderKeyResponse()
    trialResp.status = NOT_STARTED
    event.clearEvents('keyboard')
    dmRecogComponents = []
    dmRecogComponents.append(dmRcgText)
    dmRecogComponents.append(dlWordTop)
    dmRecogComponents.append(dlImage)
    dmRecogComponents.append(trialResp)
    for thisComponent in dmRecogComponents:
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    continueRoutine = True
    while continueRoutine:
        t = dmClock.getTime()
        frameN = frameN + 1
        if t >= 0.0 and dmRcgText.status == NOT_STARTED:
            dmRcgText.tStart = t
            dmRcgText.frameNStart = frameN
            dmRcgText.setAutoDraw(True)
        if str( thisDmTrial['trialType'] ) == 'word':
            if t >= 0.0 and dlWordTop.status == NOT_STARTED:
                dlWordTop.tStart = t
                dlWordTop.frameNStart = frameN
                dlWordTop.setAutoDraw(True)
        if str( thisDmTrial['trialType'] ) == 'image':
            if t >= 0.0 and dlImage.status == NOT_STARTED:
                dlImage.tStart = t
                dlImage.frameNStart = frameN
                dlImage.setAutoDraw(True)
        if t >= 0.0 and trialResp.status == NOT_STARTED:
            trialResp.tStart = t
            trialResp.frameNStart = frameN
            trialResp.status = STARTED
            trialResp.clock.reset()
            event.clearEvents(eventType='keyboard')
        if trialResp.status == STARTED:
            theseKeys = event.getKeys(keyList=['1','2','3'])
            if "escape" in theseKeys:
                endExpNow = True
            if len(theseKeys) > 0:
                trialResp.keys = theseKeys[-1]
                trialResp.rt = trialResp.clock.getTime()
                rcgRt = trialResp.rt
                # Check and set accuracy
                if trialResp.keys == '1':
                    rcgResp = 'yes'
                    if str( thisDmTrial['rcgCorr']) == 'yes':
                        rcgAcc = 1
                elif trialResp.keys == '2':
                    rcgResp = 'no'
                    if str( thisDmTrial['rcgCorr']) == 'no':
                        rcgAcc = 1
                elif trialResp.keys == '3':
                    rcgResp = 'guess'
                    rcgAcc = -1
                continueRoutine = False
        if not continueRoutine:
            break
        continueRoutine = False
        for thisComponent in dmRecogComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break
        if endExpNow or event.getKeys(keyList=["escape"]):
            core.quit()
        if continueRoutine:
            win.flip()
    for thisComponent in dmRecogComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    dmTrials.addData('dl.selection', dlWordTop.text)
    dmTrials.addData('recog.keys', trialResp.keys)
    dmTrials.addData('recog.resp', rcgResp)
    dmTrials.addData('recog.acc', rcgAcc)
    dmTrials.addData('recog.rt', rcgRt)
    routineTimer.reset()
    
#~~~| DM Fixation |~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
    t = 0
    fixClock.reset() 
    frameN = -1
    routineTimer.add(dmFixTime)
    fixComponents = []
    fixComponents.append(fixText)
    for thisComponent in fixComponents:
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    continueRoutine = True
    while continueRoutine and routineTimer.getTime() > 0:
        t = fixClock.getTime()
        frameN = frameN + 1
        if t >= 0.0 and fixText.status == NOT_STARTED:
            fixText.tStart = t
            fixText.frameNStart = frameN
            fixText.setAutoDraw(True)
        if fixText.status == STARTED and t >= (0.0 + (dmFixTime-win.monitorFramePeriod*0.75)):
            fixText.setAutoDraw(False)
        if not continueRoutine:
            break
        continueRoutine = False
        for thisComponent in fixComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break
        if endExpNow or event.getKeys(keyList=["escape"]):
            core.quit()
        if continueRoutine:
            win.flip()
    for thisComponent in fixComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)

#~~~| DM Episodic Probe |~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
    epiResp = ''
    epiAcc = 0
    epiRt = 0
    t = 0
    dmClock.reset()
    frameN = -1
    trialResp = event.BuilderKeyResponse()
    trialResp.status = NOT_STARTED
    event.clearEvents('keyboard')
    dmEpiComponents = []
    dmEpiComponents.append(dmEpiText)
    dmEpiComponents.append(dlWordTop)
    dmEpiComponents.append(dlImage)
    dmEpiComponents.append(trialResp)
    for thisComponent in dmEpiComponents:
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    continueRoutine = True
    while continueRoutine:
        t = dmClock.getTime()
        frameN = frameN + 1
        if t >= 0.0 and dmEpiText.status == NOT_STARTED:
            dmEpiText.tStart = t
            dmEpiText.frameNStart = frameN
            dmEpiText.setAutoDraw(True)
        if str( thisDmTrial['trialType'] ) == 'word':
            if t >= 0.0 and dlWordTop.status == NOT_STARTED:
                dlWordTop.tStart = t
                dlWordTop.frameNStart = frameN
                dlWordTop.setAutoDraw(True)
        if str( thisDmTrial['trialType'] ) == 'image':
            if t >= 0.0 and dlImage.status == NOT_STARTED:
                dlImage.tStart = t
                dlImage.frameNStart = frameN
                dlImage.setAutoDraw(True)
        if t >= 0.0 and trialResp.status == NOT_STARTED:
            trialResp.tStart = t
            trialResp.frameNStart = frameN
            trialResp.status = STARTED
            trialResp.clock.reset()
            event.clearEvents(eventType='keyboard')
        if trialResp.status == STARTED:
            theseKeys = event.getKeys(keyList=['1','2','3'])
            if "escape" in theseKeys:
                endExpNow = True
            if len(theseKeys) > 0:
                trialResp.keys = theseKeys[-1]
                trialResp.rt = trialResp.clock.getTime()
                epiRt = trialResp.rt
                # Check and set accuracy
                if trialResp.keys == '1':
                    epiResp = 'yes'
                    if str( thisDmTrial['epiCorr']) == 'yes':
                        epiAcc = 1
                elif trialResp.keys == '2':
                    epiResp = 'no'
                    if str( thisDmTrial['epiCorr'])== 'no':
                        epiAcc = 1
                elif trialResp.keys == '3':
                    epiResp = 'guess'
                    epiAcc = -1
                continueRoutine = False
        if not continueRoutine:
            break
        continueRoutine = False
        for thisComponent in dmEpiComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break
        if endExpNow or event.getKeys(keyList=["escape"]):
            core.quit()
        if continueRoutine:
            win.flip()
    for thisComponent in dmEpiComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    dmTrials.addData('episodic.keys', trialResp.keys)
    dmTrials.addData('episodic.resp', epiResp)
    dmTrials.addData('episodic.acc', epiAcc)
    dmTrials.addData('episodic.rt', epiRt)
    routineTimer.reset()
    
#~~~| DM Fixation |~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
    t = 0
    fixClock.reset() 
    frameN = -1
    routineTimer.add(dmFixTime)
    fixComponents = []
    fixComponents.append(fixText)
    for thisComponent in fixComponents:
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    continueRoutine = True
    while continueRoutine and routineTimer.getTime() > 0:
        t = fixClock.getTime()
        frameN = frameN + 1
        if t >= 0.0 and fixText.status == NOT_STARTED:
            fixText.tStart = t
            fixText.frameNStart = frameN
            fixText.setAutoDraw(True)
        if fixText.status == STARTED and t >= (0.0 + (dmFixTime-win.monitorFramePeriod*0.75)):
            fixText.setAutoDraw(False)
        if not continueRoutine:
            break
        continueRoutine = False
        for thisComponent in fixComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break
        if endExpNow or event.getKeys(keyList=["escape"]):
            core.quit()
        if continueRoutine:
            win.flip()
    for thisComponent in fixComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    
#~~~| DM Associative Probe |~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
    ascResp = ''
    ascAcc = 0
    ascRt = 0
    t = 0
    dmClock.reset()
    frameN = -1
    trialResp = event.BuilderKeyResponse()
    trialResp.status = NOT_STARTED
    event.clearEvents('keyboard')
    dmAssocComponents = []
    dmAssocComponents.append(dmAscText)
    dmAssocComponents.append(dlWordTop)
    dmAssocComponents.append(dlImage)
    dmAssocComponents.append(dlBox)
    dmAssocComponents.append(trialResp)
    for thisComponent in dmAssocComponents:
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    continueRoutine = True
    while continueRoutine:
        t = dmClock.getTime()
        frameN = frameN + 1
        if t >= 0.0 and dmAscText.status == NOT_STARTED:
            dmAscText.tStart = t
            dmAscText.frameNStart = frameN
            dmAscText.setAutoDraw(True)
        if t >= 0.0 and dlImage.status == NOT_STARTED:
            dlImage.tStart = t
            dlImage.frameNStart = frameN
            dlImage.setAutoDraw(True)
        if t >= 0.0 and dlBox.status == NOT_STARTED:
            dlBox.tStart = t
            dlBox.frameNStart = frameN
            dlBox.setAutoDraw(True)
        if t >= 0.0 and dlWordTop.status == NOT_STARTED:
            dlWordTop.tStart = t
            dlWordTop.frameNStart = frameN
            dlWordTop.setAutoDraw(True)
        if t >= 0.0 and trialResp.status == NOT_STARTED:
            trialResp.tStart = t
            trialResp.frameNStart = frameN
            trialResp.status = STARTED
            trialResp.clock.reset()
            event.clearEvents(eventType='keyboard')
        if trialResp.status == STARTED:
            theseKeys = event.getKeys(keyList=['1','2','3'])
            if "escape" in theseKeys:
                endExpNow = True
            if len(theseKeys) > 0:
                trialResp.keys = theseKeys[-1]
                trialResp.rt = trialResp.clock.getTime()
                ascRt = trialResp.rt
                # Check and set accuracy
                if trialResp.keys == '1':
                    ascResp = 'yes'
                    if str( thisDmTrial['ascCorr']) == 'yes':
                        ascAcc = 1
                elif trialResp.keys == '2':
                    ascResp = 'no'
                    if str( thisDmTrial['ascCorr']) == 'no':
                        ascAcc = 1
                elif trialResp.keys == '3':
                    ascResp = 'guess'
                    ascAcc = -1
                continueRoutine = False
        if not continueRoutine:
            break
        continueRoutine = False
        for thisComponent in dmAssocComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break
        if endExpNow or event.getKeys(keyList=["escape"]):
            core.quit()
        if continueRoutine:
            win.flip()
    for thisComponent in dmAssocComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    dmTrials.addData('assoc.keys', trialResp.keys)
    dmTrials.addData('assoc.resp', ascResp)
    dmTrials.addData('assoc.acc', ascAcc)
    dmTrials.addData('assoc.rt', ascRt)
    routineTimer.reset()
    
    # Next Trial
    dmExp.nextEntry()
    
#~~| FS Instructions |~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
instructText.setText( sFsInstructions )
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

#~~| FS Run Loop |~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
fsRuns = data.TrialHandler(
    nReps=nFsRuns,
    method='sequential', 
    extraInfo=expInfo,
    trialList=[None],
    name='fsRuns'
)
fsExp.addLoop(fsRuns)
thisFsRun = fsRuns.trialList[0]

# Set responses for good and bad, switch every run, starting with 1 good, 2 bad
fsGoodResp = 'rctrl'
fsBadResp = 'lctrl'

for thisFsRun in fsRuns:
    currentLoop = fsRuns
    # Switch responses every run
    if str(fsGoodResp) == 'rctrl':
        fsGoodResp = 'lctrl'
        fsBadResp = 'rctrl'
    else:
        fsGoodResp = 'rctrl'
        fsBadResp = 'lctrl'
        
#~~~| FS Trial Loop |~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
    fsTrials = data.TrialHandler(
        nReps=fsListReps,
        method='random',
        extraInfo=expInfo,
        trialList=data.importConditions( str(inFileFS) ),
        name='fsTrials'
    )
    fsExp.addLoop(fsTrials)
    thisFsTrial = fsTrials.trialList[0]

    for thisFsTrial in fsTrials:
        currentLoop = fsTrials
#~~~~~~~| FS Fixation |~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
        fsText.setText( str( thisFsTrial['word'] ) )
        fsImage.setImage( str( thisFsTrial['image'] ) )
        fsResp = ''
        fsAcc = 0
        fsRt = 0
        t = 0
        fixClock.reset() 
        frameN = -1
        routineTimer.add(fsFixTime)
        fixComponents = []
        fixComponents.append(fixText)
        for thisComponent in fixComponents:
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        continueRoutine = True
        while continueRoutine and routineTimer.getTime() > 0:
            t = fixClock.getTime()
            frameN = frameN + 1
            if t >= 0.0 and fixText.status == NOT_STARTED:
                fixText.tStart = t
                fixText.frameNStart = frameN
                fixText.setAutoDraw(True)
            if fixText.status == STARTED and t >= (0.0 + (fsFixTime-win.monitorFramePeriod*0.75)):
                fixText.setAutoDraw(False)
            if not continueRoutine:
                break
            continueRoutine = False
            for thisComponent in fixComponents:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break
            if endExpNow or event.getKeys(keyList=["escape"]):
                core.quit()
            if continueRoutine:
                win.flip()
        for thisComponent in fixComponents:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        
#~~~~~~~| FS Word Disp |~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
        t = 0
        fsWordClock.reset()
        frameN = -1
        routineTimer.add(fsWordTime)
        fsWordComponents = []
        fsWordComponents.append(fsText)
        for thisComponent in fsWordComponents:
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        continueRoutine = True
        while continueRoutine and routineTimer.getTime() > 0:
            t = fsWordClock.getTime()
            frameN = frameN + 1
            if t >= 0.0 and fsText.status == NOT_STARTED:
                fsText.tStart = t
                fsText.frameNStart = frameN
                fsText.setAutoDraw(True)
            if fsText.status == STARTED and t >= (0.0 + (fsWordTime-win.monitorFramePeriod*0.75)):
                fsText.setAutoDraw(False)
            if not continueRoutine:
                break
            continueRoutine = False
            for thisComponent in fsWordComponents:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break
            if endExpNow or event.getKeys(keyList=["escape"]):
                core.quit()
            if continueRoutine:
                win.flip()
        for thisComponent in fsWordComponents:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        
#~~~~~~~| FS Face Disp |~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
        t = 0
        fsFaceClock.reset()
        frameN = -1
        trialResp = event.BuilderKeyResponse()
        trialResp.status = NOT_STARTED
        event.clearEvents('keyboard')
        routineTimer.add(fsFaceTime)
        fsFaceComponents = []
        fsFaceComponents.append(fsImage)
        fsFaceComponents.append(trialResp)
        for thisComponent in fsFaceComponents:
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        continueRoutine = True
        while continueRoutine and routineTimer.getTime() > 0:
            t = fsFaceClock.getTime()
            frameN = frameN + 1
            if t >= 0.0 and fsImage.status == NOT_STARTED:
                fsImage.tStart = t
                fsImage.frameNStart = frameN
                fsImage.setAutoDraw(True)
            if fsImage.status == STARTED and t >= (0.0 + (fsFaceTime-win.monitorFramePeriod*0.75)):
                fsImage.setAutoDraw(False)
            if t >= 0.0 and trialResp.status == NOT_STARTED:
                trialResp.tStart = t
                trialResp.frameNStart = frameN
                trialResp.status = STARTED
                trialResp.clock.reset()
                event.clearEvents(eventType='keyboard')
            if trialResp.status == STARTED and t >= (0.0 + (fsFaceTime-win.monitorFramePeriod*0.75)):
                trialResp.status = STOPPED
            if trialResp.status == STARTED:
                theseKeys = event.getKeys(keyList=['lctrl','rctrl'])
                if "escape" in theseKeys:
                    endExpNow = True
                if len(theseKeys) > 0:
                    trialResp.keys = theseKeys[-1]
                    trialResp.rt = trialResp.clock.getTime()
                    fsRt = trialResp.rt
                    # Check and set accuracy
                    if trialResp.keys == str(fsGoodResp):
                        fsResp = 'good'
                        if str(thisFsTrial['emotion']) == 'good':
                            fsAcc = 1
                    elif trialResp.keys == str(fsBadResp):
                        fsResp = 'bad'
                        if str(thisFsTrial['emotion']) == 'bad':
                            fsAcc = 1
                    else:
                        fsResp = 'noresp'
                        fsRt = 0
                    continueRoutine = False
            if not continueRoutine:
                break
            continueRoutine = False
            for thisComponent in fsFaceComponents:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break
            if endExpNow or event.getKeys(keyList=["escape"]):
                core.quit()
            if continueRoutine:
                win.flip()
        for thisComponent in fsFaceComponents:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        fsTrials.addData('fs.word', fsText.text)
        fsTrials.addData('fs.keys', trialResp.keys)
        fsTrials.addData('fs.resp', fsResp)
        fsTrials.addData('fs.acc', fsAcc)
        fsTrials.addData('fs.rt', fsRt)

        # Next Trial
        fsExp.nextEntry()

#~~~| FS Run Break Screen |~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
    if ( fsRuns.thisN + 1 ) < nFsRuns:
        instructText.setText( sFsBreakText )
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

#~~| Goodbye Screen |~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
t = 0
goodbyeClock.reset()
frameN = -1
event.clearEvents(eventType='keyboard')
goodbyeResp = event.BuilderKeyResponse()
goodbyeResp.status = NOT_STARTED
goodbyeComponents = []
goodbyeComponents.append(goodbyeText)
goodbyeComponents.append(goodbyeResp)
for thisComponent in goodbyeComponents:
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED
continueRoutine = True
while continueRoutine:
    t = goodbyeClock.getTime()
    frameN = frameN + 1
    if t >= 0.0 and goodbyeText.status == NOT_STARTED:
        goodbyeText.tStart = t
        goodbyeText.frameNStart = frameN
        goodbyeText.setAutoDraw(True)
    if t >= 0.0 and goodbyeResp.status == NOT_STARTED:
        goodbyeResp.tStart = t
        goodbyeResp.frameNStart = frameN
        goodbyeResp.status = STARTED
        event.clearEvents(eventType='keyboard')
    if goodbyeResp.status == STARTED:
        theseKeys = event.getKeys(keyList=['q', 'Q'])
        if "escape" in theseKeys:
            endExpNow = True
        if len(theseKeys) > 0:
            continueRoutine = False
    if not continueRoutine:
        break
    continueRoutine = False
    for thisComponent in goodbyeComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break
    if endExpNow or event.getKeys(keyList=["escape"]):
        core.quit()
    if continueRoutine:
        win.flip()
for thisComponent in goodbyeComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
routineTimer.reset()

# Safely close and quit
win.close()
core.quit()
