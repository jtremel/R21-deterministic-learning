#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
XXXXXXXXXXXXXXXXXXXXXX change the following XXXXXXXXXXXXXXXXXXXXXX


~~ Version History ~~
0.1.0: Feb 9, 2017: development,

XXXXXXXXXXXXXXXXXXXXXX Change above XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

~~ PsychoPy Version information and Citations ~~
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
expName = 'DL Pre-scan Practice Session'
# Experiment Info Collection
expInfo = {'subject':''}
# Experiment Version
expVersion='1.0.0'

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
# Font color for positive feedback
corColor = 'lime'
# Font color for negative feedback
errColor = 'red'

# ~~~~~~ Image Properties ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# Background image resolution
imgW = 1200
imgH = 800
# Size of semi-transparent background box for text display
boxW = 300
boxH = 300
# Opacity of background box (1.0 = opaque)
boxOpacity = 0.5

# ~~~~~~ Timing Properties ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# Length of inter-stimulus interval (fixation), in seconds
dlFixTime = 2.0
# Length of stimulus display (trial), in seconds
dlStimTime = 4.0
# Length of feedback display, in seconds
dlFdbkTime = 2.0

nbTrialTime = 1.0
nbFixTime = 1.0

# ~~~~~~ Task Instructions ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
sDlInstructions = ("You're going to see a pair of words with an image in the background. There are a total of 80 pairs that you\'ll go through twice.\n\n"+
"In each of these pairs, one of the words is arbitrarily designated to be a \'correct\' choice, and the other to be an \'incorrect\' choice. "+
"Your goal is to learn which words are correct and to later make as many correct choices as you can.\n\n"+
"When you see a word pair, you will have to select one of the words and will see feedback. The feedback will indicate whether you chose "+
"correctly or incorrectly. You will gain points for correct choices and lose points for incorrect choices.\n\nThis first time through is trial and "+
"error, since you have no information about which words might be right and wrong. After this first round, you will go through a second "+
"time with words you selected but paired with new words. At this point, you will want to select words that were correct in the first round "+
"and avoid ones that were incorrect.\n\nFor example, if you choose the word ARM in the first round and learn that it was correct, you "+
"will want to select the word ARM in the second round when you see it to earn points. Likewise, if you choose the word LEG in the first round "+
"and learn that it was incorrect, you will want to choose the other word when you see LEG in the second round to earn points.\n\n"+
"Press the LEFT CTRL key to select the TOP word, or press the RIGHT CTRL key to select the BOTTOM word.\n\n"+
"The words will be on the screen for a maximum of 3.0 seconds--please respond while they are on the screen.\n\n"+
"The experimenter will give you some additional instructions and let you know when you can start.")

sDlInstructions2 = ("This time, you are going to see the same words that you selected in Round 1, but this time paired with a new word. "+
"The words from Round 1 will retain their value. So, any word that was correct in Round 1 is still correct this time, and any word that was "+
"incorrect is still incorrect this time. Try to make as many correct choices and earn as many points as possible.\n\n"+
"You will not get feedback this time, but will see a final score at the end.\n\n"+
"As before, the words will be on the screen for up to 3.0 seconds--please make your response while they are on the screen. "+
"Press the LEFT CTRL key to select the TOP word, or press the RIGHT CTRL key to select the BOTTOM word.\n\n"+
"The experimenter will give you some additional instructions and let you know when you can start.")

sDlFinalDisplay = ('Congratulations, you have finished this section! There are two more parts to complete.')

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# Experiment Setup
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# Ensure that relative paths start from the same directory as this script
_thisDir = os.path.dirname(os.path.abspath(__file__))
os.chdir(_thisDir)

# Set up experiment files and info
dlg = gui.DlgFromDict(dictionary=expInfo, title=expName)
if dlg.OK == False: core.quit()

inFileDL = gui.fileOpenDlg(prompt='Select Deterministic Learning List file', allowed="CSV files (.csv)|*.csv", tryFilePath=_thisDir)
if inFileDL ==None: core.quit()
inFileDL = inFileDL[0]

expInfo['date'] = data.getDateStr()
expInfo['expName'] = expName
expInfo['expVersion'] = expVersion
endExpNow = False # flag for experiment kill switch

# Set up extras for data caching
selection = ''
trialAcc = 0
rewValue = 10
curReward = 0

# Set up data directory and data file
if not os.path.isdir('__data'):
    os.makedirs('__data')
filenameDL = _thisDir + os.sep + '__data' + os.path.sep + 's%s_%s_v%s__%s' %( expInfo.get('subject'), 'DL', expVersion, expInfo['date'])
filenameLog = _thisDir + os.sep + '__data' + os.path.sep + 's%s_expt_v%s__%s' %( expInfo.get('subject'), expVersion, expInfo['date'])
logFile = logging.LogFile(filenameLog+'.log', level=logging.DEBUG)
logging.console.setLevel(logging.WARNING)

# Set up Experiment Managers
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
globalClock = core.Clock()
routineTimer = core.CountdownTimer()
instructClock = core.Clock()
goodbyeClock = core.Clock()
fixClock = core.Clock()
dlTrialClock = core.Clock()
dlFeedbackClock = core.Clock()
nBackDispClock = core.Clock()
nBackFixClock = core.Clock()


# Set up trial loops
dlTrials = data.TrialHandler(
    nReps=1,
    method='random',
    extraInfo=expInfo,
    trialList=data.importConditions( str(inFileDL) ),
    name='dlTrials'
)
# Total number of items for DL
nPairs = dlTrials.nTotal

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
    size=[imgW, imgH],
    units='pix',
    interpolate=True
)
dlReward = visual.TextStim(
    win=win,
    name='dlReward',
    text='- - -',
    font='Arial',
    bold=bStimTextBold,
    pos=[0, 0],
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
#~~| DL R1 Instructions |~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
instructText.setText( sDlInstructions )
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


#~~| DL R1 Trial Loop |~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
dlTrials = data.TrialHandler(
    nReps=1,
    method='random', 
    extraInfo=expInfo,
    trialList=data.importConditions(str(inFileDL)),
    name='dlTrials'
)
dlExp.addLoop(dlTrials)
thisDlTrial = dlTrials.trialList[0]

selectedWords = dict()

for thisDlTrial in dlTrials:
    currentLoop = dlTrials
#~~~| DL fixation |~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
    jitterLoop = data.TrialHandler(
        nReps=int(thisDlTrial['jitter']),
        method='sequential',
        extraInfo=expInfo,
        trialList=[None],
        name='JitterLoop'
    )
    thisJitterLoop = jitterLoop.trialList[0]
    
    for thisJitterLoop in jitterLoop:
        t = 0
        fixClock.reset() 
        frameN = -1
        routineTimer.add(dlFixTime)
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
            if fixText.status == STARTED and t >= (0.0 + (dlFixTime-win.monitorFramePeriod*0.75)):
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
        routineTimer.reset()
    
#~~~| DL trial |~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
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
    dlImage.setImage( str( thisDlTrial['image'] ) )
    # Set up reward value
    rewValue = thisDlTrial['reward']
    trialAcc = -1
    action = ''
    selWord = ''
    
    # Begin trial routine
    t = 0
    dlTrialClock.reset() 
    frameN = -1
    routineTimer.add(dlStimTime)
    trialResp = event.BuilderKeyResponse()
    trialResp.status = NOT_STARTED
    event.clearEvents('keyboard')
    dlTrialComponents = []
    dlTrialComponents.append(dlImage)
    dlTrialComponents.append(dlBox)
    dlTrialComponents.append(dlWordTop)
    dlTrialComponents.append(dlWordBtm)
    dlTrialComponents.append(trialResp)
    for thisComponent in dlTrialComponents:
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    continueRoutine = True
    while continueRoutine and routineTimer.getTime() > 0:
        t = dlTrialClock.getTime()
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
            theseKeys = event.getKeys(keyList=['lctrl', 'rctrl'])
            if "escape" in theseKeys:
                endExpNow = True
            if len(theseKeys) > 0:
                trialResp.keys = theseKeys[-1]
                trialResp.rt = trialResp.clock.getTime()
                # Set accuracy for feedback
                if str(thisDlTrial['feedback']) == 'cor':
                    trialAcc = 1
                else:
                    trialAcc = 0
                # Figure out which word was chosen
#                action = '--'
#                selWord = '--'
                if trialResp.keys == 'lctrl':
                    action = 'top'
                    selWord = str( dlWordTop.text )
                elif trialResp.keys == 'rctrl':
                    action = 'btm'
                    selWord = str( dlWordBtm.text )
                selectedWords[str(thisDlTrial['pair'])] = str(selWord)
#            else:
#                trialAcc = -1
#                selectedWords[str(thisDlTrial['pair'])] = str(thisDlTrial['word1'])
        if not continueRoutine:
            break
        continueRoutine = False
        for thisComponent in dlTrialComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break
        if endExpNow or event.getKeys(keyList=["escape"]):
            core.quit()
        if continueRoutine:
            win.flip()
    for thisComponent in dlTrialComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    dlTrials.addData('dl.selection', selWord)
    dlTrials.addData('dl.keys', trialResp.keys)
    dlTrials.addData('dl.action', action)
    if trialResp.keys != None:
        dlTrials.addData('dl.acc', trialAcc)
        dlTrials.addData('dl.rt', trialResp.rt)
    else:
        trialAcc = -1 # for feedback display
        selectedWords[str(thisDlTrial['pair'])] = str(thisDlTrial['word1'])
        dlTrials.addData('dl.acc', 'noresp')
        dlTrials.addData('dl.rt', 0)
    
#~~~| DL feedback |~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
    if str(trialAcc) == '1':
        dlReward.setText( u'+$%s!' %(rewValue) )
        dlReward.setColor( corColor )
    elif str(trialAcc) == '0':
        dlReward.setText(u'-$%s' %(rewValue) )
        dlReward.setColor( errColor )
    else:
        dlReward.setText('- - -')
        dlReward.setColor( fontColor )
    
    # Begin feedback routine
    t = 0
    dlFeedbackClock.reset()
    frameN = -1
    routineTimer.add(dlFdbkTime)
    dlFeedbackComponents = []
    dlFeedbackComponents.append(dlImage)
    dlFeedbackComponents.append(dlBox)
    dlFeedbackComponents.append(dlReward)
    for thisComponent in dlFeedbackComponents:
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    continueRoutine = True
    while continueRoutine and routineTimer.getTime() > 0:
        t = dlFeedbackClock.getTime()
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
        for thisComponent in dlFeedbackComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break
        if endExpNow or event.getKeys(keyList=["escape"]):
            core.quit()
        if continueRoutine:
            win.flip()
    for thisComponent in dlFeedbackComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    
    #~~~| DL fix (pre NBack) |~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
    t = 0
    fixClock.reset() 
    frameN = -1
    routineTimer.add(dlFixTime)
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
        if fixText.status == STARTED and t >= (0.0 + (dlFixTime-win.monitorFramePeriod*0.75)):
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
    routineTimer.reset()

    #~~~| NBack Loop |~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
    nBackWords = [ str( thisDlTrial['nBackWord1'] ), str( thisDlTrial['nBackWord2'] ), str( thisDlTrial['nBackWord3'] ), str( thisDlTrial['nBackWord4'] ), str( thisDlTrial['nBackWord5'] ), str( thisDlTrial['nBackWord6'] ), str( thisDlTrial['nBackWord7'] )]
    # Set up NBack Loop
    nBackLoop = data.TrialHandler(
        nReps=7,
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
                theseKeys = event.getKeys(keyList=['lctrl','rctrl'])
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
    
    # Next Trial
    dlExp.nextEntry()

#~~| DL Instructions 2 |~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
instructText.setText( sDlInstructions2 )
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

#~~~| DL Trial Loop |~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
dlTrials = data.TrialHandler(
    nReps=1,
    method='random',
    extraInfo=expInfo,
    trialList=data.importConditions( str(inFileDL) ),
    name='dlTrials'
)
dlExp.addLoop(dlTrials)
thisDlTrial = dlTrials.trialList[0]

for thisDlTrial in dlTrials:
    currentLoop = dlTrials
#~~~| DL fixation |~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
    jitterLoop = data.TrialHandler(
        nReps=int(thisDlTrial['jitter']),
        method='sequential',
        extraInfo=expInfo,
        trialList=[None],
        name='JitterLoop'
    )
    thisJitterLoop = jitterLoop.trialList[0]
    
    for thisJitterLoop in jitterLoop:
        t = 0
        fixClock.reset() 
        frameN = -1
        routineTimer.add(dlFixTime)
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
            if fixText.status == STARTED and t >= (0.0 + (dlFixTime-win.monitorFramePeriod*0.75)):
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
        routineTimer.reset()
    
#~~~| DL trial |~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
    # Randomize and set item positions
    rand = randint(0,2)
    corResp = 'none'
    if rand == 1:
        dlWordTop.setText( str( selectedWords[ str(thisDlTrial['pair']) ] ) )
        dlWordBtm.setText( str(thisDlTrial['word3']) )
        if str(thisDlTrial['feedback']) == 'cor':
            corResp = 'lctrl'
        else:
            corResp = 'rctrl'
    else:
        dlWordTop.setText( str(thisDlTrial['word3']) )
        dlWordBtm.setText( str( selectedWords[ str(thisDlTrial['pair']) ] ) )
        if str(thisDlTrial['feedback']) == 'cor':
            corResp = 'rctrl'
        else:
            corResp = 'lctrl'
    
    # Reset font colors
    dlWordTop.setColor(fontColor)
    dlWordBtm.setColor(fontColor)

    # Set up reward value
    rewValue = thisDlTrial['reward']
    trialAcc = -1
    action = ''
    selWord = ''
    
    # Init trial routine
    t = 0
    dlTrialClock.reset() 
    frameN = -1
    routineTimer.add(dlStimTime)
    trialResp = event.BuilderKeyResponse()
    trialResp.status = NOT_STARTED
    event.clearEvents('keyboard')
    dlTrialComponents = []
    dlTrialComponents.append(dlWordTop)
    dlTrialComponents.append(dlWordBtm)
    dlTrialComponents.append(trialResp)
    for thisComponent in dlTrialComponents:
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # Run trial routine
    continueRoutine = True
    while continueRoutine and routineTimer.getTime() > 0:
        t = dlTrialClock.getTime()
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
            theseKeys = event.getKeys(keyList=['lctrl', 'rctrl'])
            if "escape" in theseKeys:
                endExpNow = True
            if len(theseKeys) > 0:
                trialResp.keys = theseKeys[-1]
                trialResp.rt = trialResp.clock.getTime()
#                action = '--'
#                selWord = '--'
                if trialResp.keys == 'lctrl':
                    action = 'top'
                    selWord = str( dlWordTop.text )
                elif trialResp.keys == 'rctrl':
                    action = 'btm'
                    selWord = str( dlWordBtm.text )
                if trialResp.keys == str(corResp):
                    trialAcc = 1
                    curReward += rewValue
                else:
                    trialAcc = 0
                    curReward -= rewValue
                continueRoutine = False
#            else:
#                trialAcc = -1
        if not continueRoutine:
            break
        continueRoutine = False
        for thisComponent in dlTrialComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break
        if endExpNow or event.getKeys(keyList=["escape"]):
            core.quit()
        if continueRoutine:
            win.flip()
    for thisComponent in dlTrialComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    dlTrials.addData('dl.selection', selWord)
    dlTrials.addData('dl.keys', trialResp.keys)
    dlTrials.addData('dl.action', action)
    if trialResp.keys != None:
        dlTrials.addData('dl.acc', trialAcc)
        dlTrials.addData('dl.rt', trialResp.rt)
    else:
        trialAcc = -1 # for feedback display
        dlTrials.addData('dl.acc', 'noresp')
        dlTrials.addData('dl.rt', 0)
        
    #~~~| DL fix (pre NBack) |~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
    t = 0
    fixClock.reset() 
    frameN = -1
    routineTimer.add(dlFixTime)
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
        if fixText.status == STARTED and t >= (0.0 + (dlFixTime-win.monitorFramePeriod*0.75)):
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
    routineTimer.reset()

    #~~~| NBack Loop |~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
    nBackWords = [ str( thisDlTrial['nBackWord1'] ), str( thisDlTrial['nBackWord2'] ), str( thisDlTrial['nBackWord3'] ), str( thisDlTrial['nBackWord4'] ), str( thisDlTrial['nBackWord5'] ), str( thisDlTrial['nBackWord6'] ), str( thisDlTrial['nBackWord7'] )]
    # Set up NBack Loop
    nBackLoop = data.TrialHandler(
        nReps=7,
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
                theseKeys = event.getKeys(keyList=['lctrl','rctrl'])
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
    
    # Next Trial
    dlExp.nextEntry()

#~~~| DL Run Break Screen |~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
if curReward > 15:
    curReward = 15.0
    
if curReward < 0:
    sDlFinalDisplay = ('If this were the real version, you unfortunately wouldn\'t have earned any bonus.\n\nBut you made it through the practice! Good luck with the scan!')
else:
    sDlFinalDisplay = ('If this were the real version, you would have made $%s!\n\nNice job. Good luck with the scan!' %(curReward) )

instructText.setText( sDlFinalDisplay )
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

win.close()
core.quit()