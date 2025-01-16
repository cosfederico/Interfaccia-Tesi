from __future__ import division
from __future__ import print_function

import datetime
import os
import pylink

import subprocess
import pandas as pd

class EyeTracker:
    
    RIGHT_EYE = 1
    LEFT_EYE = 0
    BINOCULAR = 2
    
    def __init__(self, save_folder, edf_file_name='eye.edf'):
        
        self.save_folder = save_folder
        self.edf_file_name = edf_file_name
       
        if not os.path.exists(self.save_folder):
            os.makedirs(self.save_folder)
            
        try:
            self.el_tracker = pylink.EyeLink("100.1.1.1")
        except RuntimeError as error:
            print(error)
            raise RuntimeError('Error connecting to the eye-tracker Host PC. Is the ethernet cable connected? Is the local IP Address setup correctly (100.1.1.2 / 255.255.255.0)')
        
        disp = pylink.getDisplayInformation()
        self.SCN_WIDTH = disp.width
        self.SCN_HEIGHT = disp.height
        pylink.openGraphics((self.SCN_WIDTH, self.SCN_HEIGHT), 32)
        
        self.el_tracker.openDataFile(edf_file_name)

        # add a preamble text (data file header)
        preamble_text = 'RECORDED BY %s' % os.path.basename(__file__)
        self.el_tracker.sendCommand("add_file_preamble_text '%s'" % preamble_text)        
        
    def setup_tracking(self):
        # we first flush all key presses and put the tracker in the offline mode
        pylink.flushGetkeyQueue()
        self.el_tracker.setOfflineMode()

        # The tracker needs to know the resolution of the screen the
        # subject is viewing
        pix_msg = "screen_pixel_coords 0 0 %d %d" % (self.SCN_WIDTH - 1, self.SCN_HEIGHT - 1)
        self.el_tracker.sendCommand(pix_msg)
        # The Data Viewer software also needs to know the screen
        # resolution for correct visualization
        dv_msg = "DISPLAY_COORDS  0 0 %d %d" % (self.SCN_WIDTH - 1, self.SCN_HEIGHT - 1)
        self.el_tracker.sendMessage(dv_msg)

        # Get the software version:  1-EyeLink I, 2-EyeLink II, 3/4-EyeLink 1000,
        # 5-EyeLink 1000 Plus, 6-Portable DUO
        vstr = self.el_tracker.getTrackerVersionString()
        eyelink_ver = int(vstr.split()[-1].split('.')[0])
        # print out some version info in the shell
        print('Running experiment on %s, version %d' % (vstr, eyelink_ver))

        # Select what data to save in the EDF file, for a detailed discussion
        # of the data flags, see the EyeLink User Manual, "Setting File Contents"
        file_event_flags = 'LEFT,RIGHT,FIXATION,SACCADE,BLINK,MESSAGE,BUTTON,INPUT'
        file_sample_flags = 'LEFT,RIGHT,GAZE,HREF,RAW,AREA,HTARGET,GAZERES,BUTTON,STATUS,INPUT'
        if eyelink_ver < 4:
            file_sample_flags = 'LEFT,RIGHT,GAZE,HREF,RAW,AREA,GAZERES,BUTTON,STATUS,INPUT'
        self.el_tracker.sendCommand("file_event_filter = %s" % file_event_flags)
        self.el_tracker.sendCommand("file_sample_data = %s" % file_sample_flags)

        # Select what data is available over the link (for online data accessing)
        link_event_flags = 'LEFT,RIGHT,FIXATION,SACCADE,BLINK,BUTTON,FIXUPDATE,INPUT'
        link_sample_flags = 'LEFT,RIGHT,GAZE,GAZERES,AREA,HTARGET,STATUS,INPUT'
        if eyelink_ver < 4:
            link_sample_flags = 'LEFT,RIGHT,GAZE,GAZERES,AREA,STATUS,INPUT'
        self.el_tracker.sendCommand("link_event_filter = %s" % link_event_flags)
        self.el_tracker.sendCommand("link_sample_data = %s" % link_sample_flags)

        # Set the calibration target and background color
        pylink.setCalibrationColors((0, 0, 0), (128, 128, 128))

        # select best size for calibration target
        pylink.setTargetSize(int(self.SCN_WIDTH/70.0), int(self.SCN_WIDTH/300.))

        # Set the calibration and drift correction sound
        pylink.setCalibrationSounds("", "", "")
        pylink.setDriftCorrectSounds("", "", "")

        # Step 5: Do the tracker setup at the beginning of the experiment.
        self.el_tracker.doTrackerSetup()
                
    def start_recording(self, participant_id, drift_check=False):
        if not self.el_tracker.isConnected():
            raise RuntimeError("Unable to start eye-tracking trial - The tracker is not connected or lost connection")
        if self.el_tracker.breakPressed():
            raise RuntimeError("Unable to start eye-tracking trial - A break key was pressed (CTRL+C, ESC, ..)")
        
        """ Run a single trial """

        # get the currently active tracker object (connection)
        el_active = pylink.getEYELINK()

        # log a TRIALID message to mark trial start, before starting to record.
        # EyeLink Data Viewer defines the start of a trial by the TRIALID message.
        self.el_tracker.sendMessage("TRIALID %d" % participant_id)

        # clear tracker display to black
        self.el_tracker.sendCommand("clear_screen 0")

        # perform a drift-check(/correction) at the start of each trial
        if drift_check:
            while True:
                # check whether we are still connected to the tracker
                if not self.el_tracker.isConnected():
                    return pylink.ABORT_EXPT

                # drift-check; re-do camera setup, if needed
                try:
                    error = self.el_tracker.doDriftCorrect(int(self.SCN_WIDTH/2.0),
                                                    int(self.SCN_HEIGHT/2.0), 1, 1)
                    # if the "ESC" key is pressed, get back to Camera Setup
                    if error != pylink.ESC_KEY:
                        break
                    else:
                        self.el_tracker.doTrackerSetup()
                except:
                    pass

        # switch tracker to idle mode
        self.el_tracker.setOfflineMode()

        # start recording samples and events; save them to the EDF file and
        # make them available over the link
        error = self.el_tracker.startRecording(1, 1, 1, 1)
        if error:
            return error

        # begin the real-time mode
        pylink.beginRealTimeMode(100)

        # INSERT CODE TO DRAW INITIAL DISPLAY HERE

        # wait for link data to arrive
        try:
            self.el_tracker.waitForBlockStart(100, 1, 1)
        except RuntimeError:
            # wait time expired without link data
            if pylink.getLastError()[0] == 0:
                self.stop_recording()
                print("ERROR: No link data received!")
                return pylink.TRIAL_ERROR
            # for any other status simply re-raise the exception
            else:
                raise

        # determine which eye(s) is/are available
        eye_used = self.el_tracker.eyeAvailable()
        if eye_used == EyeTracker.RIGHT_EYE:
            self.el_tracker.sendMessage("EYE_USED 1 RIGHT")
        elif eye_used == EyeTracker.LEFT_EYE or eye_used == EyeTracker.BINOCULAR:
            self.el_tracker.sendMessage("EYE_USED 0 LEFT")
            eye_used = EyeTracker.LEFT_EYE
        else:
            print("Error in getting the eye information!")
            return pylink.TRIAL_ERROR

        # reset keys and buttons on tracker
        self.el_tracker.flushKeybuttons(0)

    def stop_recording(self):
        """Ends recording

        We add 100 msec of data to catch final events"""
        
        # get the currently active tracker object (connection)
        el_active = pylink.getEYELINK()

        pylink.endRealTimeMode()
        pylink.pumpDelay(100)
        el_active.stopRecording()
        self.log("TIMEOUT")

        while el_active.getkey():
            pass
        
        self.close()
        
    def close(self):
        if self.el_tracker is not None:
            self.el_tracker.setOfflineMode()
            pylink.msecDelay(1000)

            # Close the edf data file on the Host
            self.el_tracker.closeDataFile()

            # transfer the edf file to the Display PC and rename it
            local_file_name = os.path.join(self.save_folder, self.edf_file_name)

            try:
                self.el_tracker.receiveDataFile(self.edf_file_name, local_file_name)
            except RuntimeError as error:
                print(error)
                raise RuntimeError("Unable to receive data file from Eye-tracker Host PC.")

        # Step 8: close EyeLink connection and quit display-side graphics
        self.el_tracker.close()
        # Close the experiment graphics
        pylink.closeGraphics()
        
    def log(self, message):
        self.el_tracker.sendMessage(message)

    def time(self):
        el_active = pylink.getEYELINK()
        return el_active.trackerTime()