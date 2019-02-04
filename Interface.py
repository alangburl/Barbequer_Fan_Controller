import sys,os,time
import PID as pid
from PyQt5.QtWidgets import (QApplication, QPushButton,QWidget,
                             QSizePolicy,QVBoxLayout,QLineEdit,
                            QProgressBar,QMessageBox,QDial,QGridLayout,
                            QLCDNumber,QRadioButton,QLabel)
from PyQt5.QtGui import QFont,QIcon
from PyQt5.QtCore import QThread,pyqtSignal,Qt


class Window(QWidget):
    def __init__(self):
        super().__init__()
        
        self.showMaximized()
        self.setWindowTitle('Barbequer')
        self.setWindowIcon(QIcon('BBQ.png'))
        self.init()
        
    def init(self):
        
        self.size_policy=(QSizePolicy.Expanding,QSizePolicy.Expanding)
        self.font=QFont()
        self.font.setPointSize(16)
        
        self.temp_display_label=QLabel(self)
        self.temp_display_label.setText('Current Temperature:')
        self.temp_display_label.setSizePolicy(self.size_policy[0],self.size_policy[1])
        self.temp_display_label.setFont(self.font)
#        self.temp_display_label.setAlignment(Qt.AlignRight)
        
        self.temp_display=QLCDNumber(self)
        self.temp_display.setSizePolicy(self.size_policy[0],self.size_policy[1])
        self.temp_display.setFont(self.font)
        
        self.temp_set_label=QLabel(self)
        self.temp_set_label.setText('Set Temperature:')
        self.temp_set_label.setSizePolicy(self.size_policy[0],self.size_policy[1])
        self.temp_set_label.setFont(self.font)
#        self.temp_set_label.setAlignment(Qt.AlignRight)

        self.temp_set=QLCDNumber(self)
        self.temp_set.setSizePolicy(self.size_policy[0],self.size_policy[1])
        self.temp_set.setFont(self.font)
        
        self.temp_dial=QDial(self)
        self.temp_dial.setSizePolicy(self.size_policy[0],self.size_policy[1])
        self.temp_dial.setProperty('value',0)
        self.temp_dial.setSliderPosition(0)
        self.temp_dial.setNotchesVisible(True)
        self.temp_dial.setMaximum(600)
        self.temp_dial.setToolTip('Set Desired Temperature in Fahrenheit')
        self.temp_dial.valueChanged.connect(self.update_temperature)
        
        self.exhasut_fan=QRadioButton('&Enable Exhaust Fan')
        self.exhasut_fan.setSizePolicy(self.size_policy[0],self.size_policy[1])
        self.exhasut_fan.setFont(self.font)
        self.exhasut_fan.setToolTip('Enable exhaust fan')
        
        self.intake_fan=QRadioButton('&Enable Intake Fan')
        self.intake_fan.setSizePolicy(self.size_policy[0],self.size_policy[1])
        self.intake_fan.setFont(self.font)
        self.intake_fan.setToolTip('Enable intake fan')
        
        self.start_button=QPushButton('Start',self)
        self.start_button.setSizePolicy(self.size_policy[0],self.size_policy[1])
        self.start_button.setFont(self.font)
        self.start_button.setToolTip('Start Maintaining Temperature')
        self.start_button.clicked.connect(self.maintain_temperature)
        
        self.timer_button=QPushButton('Timer',self)
        self.timer_button.setSizePolicy(self.size_policy[0],self.size_policy[1])
        self.timer_button.setFont(self.font)
        self.timer_button.setToolTip('Cook Time')       
        
        #add the grid layout to the interface
        self.layout=QGridLayout(self)
        self.layout.addWidget(self.temp_dial,0,0,2,2)
        self.layout.addWidget(self.temp_set_label,2,0)
        self.layout.addWidget(self.temp_set,2,1,1,2)
        self.layout.addWidget(self.temp_display_label,3,0)
        self.layout.addWidget(self.temp_display,3,1)
        self.layout.addWidget(self.exhasut_fan,4,0)
        self.layout.addWidget(self.intake_fan,4,1)
        self.layout.addWidget(self.start_button,5,0)
        self.layout.addWidget(self.timer_button,5,1)
        self.setLayout(self.layout)
        
    def update_temperature(self):
        self.temp_set.display(str(self.temp_dial.sliderPosition()))
    
    def maintain_temperature(self):
        Temp=temp_operation(self.temp_dial.sliderPosition(),self)
        if Temp.isRunning==False:
            Temp.isRunning=True
            Temp.display_update.connect(self.temp_display.display)
            Temp.start()
        
class temp_operation(QThread):
    display_update=pyqtSignal(int)
    
    def __init__(self, set_temp,parent=None):
        '''Setting up the thread'''
        QThread.__init__(self, parent=parent)
        self.set_temp=set_temp
        self.isRunning=False
    def run(self):
        '''run the thread to maintain constant internal temperature'''
        past_time=time.time()
        start_time=time.time()
        ut=0
        ui=0
        error=0
        
        while self.isRunning:
            #start the timer
            start_time=time.time()
            #read the current temperature
            #set as an arbitrary value for testing purposes
            current_temperature=250
            #update the display with the current temperature
            self.display_update.emit(current_temperature)
            delta=past_time-start_time
            [ut,ui,error]=pid.calculate(self.set_temp,current_temperature,delta)
            time.sleep(1)
            past_time=time.time()
            print(ut)
            
    
if __name__=='__main__':
    app = QApplication(sys.argv)
    ex = Window()
    ex.show()
    sys.exit(app.exec_())
        