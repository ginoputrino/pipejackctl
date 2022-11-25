# python 3.x
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import subprocess
from functools import partial
from utils import _execute_shell_command, readConfig, getConfigFileName
from constants import *

class SampleMonitor(QObject):
  sendOutput = pyqtSignal(str)

  def __init__(self, config):
    super(SampleMonitor, self).__init__()
    self.process = QProcess()
    self.config = config
    self.setupProcess()

  def __del__(self):
    self.process.terminate()
    if not self.process.waitForFinished(100000):
      self.process.kill()

  def setupProcess(self):
    self.process.setProcessChannelMode(QProcess.MergedChannels)
    self.process.readyReadStandardOutput.connect(self.readStdOutput)
    getRate = self.config.get(CONFIG_SECTION_MAIN, CONFIG_OPTION_MAIN_PWMETACOMMAND) + ' ' + \
      self.config.get(CONFIG_SECTION_MAIN, CONFIG_OPTION_MAIN_MONITOR_FLAGS)
    self.process.start(getRate)

  @pyqtSlot()
  def readStdOutput(self):
    output = str(self.process.readAllStandardOutput())
    valueStart = output.find(PW_MONITOR_VALUE_SYMBOL)
    valueEnd = output[valueStart+7::].find("'")
    valueSubString = ""
    if (valueEnd > 0):
        valueSubString = output[valueStart+7:valueStart+7+valueEnd]
    else:
      valueEnd = output[valueStart+8::].find("'")
      valueSubString = output[valueStart+8:valueStart+7+valueEnd]

    self.sendOutput.emit(valueSubString)




class App(QDialog):
    def __init__(self):
      super().__init__()
      self.config = readConfig()
      self.title = 'Pipewire jackd Helper'
      self.left =  self.config.getint(CONFIG_SECTION_MAIN, CONFIG_OPTION_MAIN_LEFT)
      self.top = self.config.getint(CONFIG_SECTION_MAIN, CONFIG_OPTION_MAIN_TOP)
      self.width = self.config.getint(CONFIG_SECTION_MAIN, CONFIG_OPTION_MAIN_WIDTH)
      self.height = self.config.getint(CONFIG_SECTION_MAIN, CONFIG_OPTION_MAIN_HEIGHT)
      self.thread = QThread()
      self.initUI()
    
    def createGridLayout(self):
        self.horizontalGroupBox = QGroupBox("Audio Settings")
        layout = QGridLayout()
        layout.setColumnStretch(1, 4)
        layout.setColumnStretch(2, 4)

        # Create Resolution Entry
        self.samplingRateBox = QComboBox()

        for aRate in RECOMMENDED_RATES:
          self.samplingRateBox.addItem(str(aRate))
        self.samplingRateBox.setCurrentText(self.config.get(CONFIG_SECTION_AUDIO, CONFIG_OPTION_AUDIO_DEFAULT_SAMPLE_RATE))
        
        #Sample Rate
        layout.addWidget(QLabel('Choose sample rate: ', self),0,0)
        layout.addWidget(self.samplingRateBox, 0,1)
        
        setGlobalSampleRate = QPushButton('Force Global Sample Rate')
        setGlobalSampleRate.setToolTip('This forces all devices to the chosen sample rate - even if some devices do not support it.')
        setGlobalSampleRate.clicked.connect(self.setSampleRate)
        layout.addWidget(setGlobalSampleRate, 1, 0)

        self.currentSampleLabel = QLabel(CURRENT_SAMPLE_RATE_LABEL , self)
        layout.addWidget(self.currentSampleLabel, 2, 0)
        self.currentSampleText = QLabel('Monitoring' , self)
        layout.addWidget(self.currentSampleText, 2, 1)

        self.horizontalGroupBox.setLayout(layout)

        #Applications to Launch
        self.applicationGroupBox = QGroupBox("Application Launcher")
        applicationLayout = QGridLayout()
        self.applications = self.config.get(CONFIG_SECTION_APPLICATIONS, CONFIG_OPTION_APPLICATION_LOCATIONS).split(',')
        row = 0
        column = 0
        for anApp in self.applications:
          anAppButton = QPushButton(anApp)
          anAppButton.setToolTip('Launches: '+ anApp)
          anAppButton.clicked.connect(partial(self.launchApp, anApp))
          applicationLayout.addWidget(anAppButton, row, column)
          column = column+1
          if (column > 1):
            row = row+1
            column = 0
        anAppButton = QPushButton('Launch All')
        anAppButton.setToolTip('Launches all registered jackd apps')
        anAppButton.clicked.connect(self.launchAllApps)
        applicationLayout.addWidget(anAppButton, row, column)

        self.applicationGroupBox.setLayout(applicationLayout)


    def launchAllApps(self):
      for anApp in self.applications:
        self.launchApp(anApp)

    @pyqtSlot(str)
    def launchApp(self, anApp):
      print(anApp)
      print("Launching: " + anApp)
      pwjackCmd = self.config.get(CONFIG_SECTION_MAIN, CONFIG_OPTION_MAIN_PWJACK)
      theCmd = [pwjackCmd] + PW_JACK_OPTIONS  + [self.currentSampleText.text().strip()] + [anApp]
      sp = subprocess.Popen(theCmd)
      
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.createGridLayout()

        windowLayout = QVBoxLayout()
        windowLayout.addWidget(self.horizontalGroupBox)
        windowLayout.addWidget(self.applicationGroupBox)

        configFileLocation = QLabel("Config location: " + getConfigFileName(), self)
        windowLayout.addWidget(configFileLocation)


        self.setLayout(windowLayout)

        self.monitorSampleRate = SampleMonitor(self.config)
        self.thread.finished.connect(self.monitorSampleRate.deleteLater)
        self.monitorSampleRate.sendOutput.connect(self.showSampleRate)
        self.monitorSampleRate.moveToThread(self.thread)
        self.thread.start()
        
        self.show()
    
    def __del__(self):
      if self.thread.isRunning():
        self.thread.quit()
      
    def setSampleRate(self):
        samplingRate = self.samplingRateBox.currentText()
        cmd = [self.config.get(CONFIG_SECTION_MAIN, CONFIG_OPTION_MAIN_PWMETACOMMAND)]
        setRate = cmd + CLOCKRATE_FLAGS + [samplingRate]
        stdout, _ = _execute_shell_command(command=setRate, verbose=True)

        print(stdout)
    
    @pyqtSlot(str)
    def showSampleRate(self, output):
      self.currentSampleText.setText(output)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())






