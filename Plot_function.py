import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import pyqtgraph as QtGraph         #Added to support plotting graphs in PyQt
import math
import numpy

class Plot_window(QWidget):
    def __init__(self, parent=None):
        #Initialize class variables
        #--------------------------
        self.x_min=0
        self.x_max=0
        self.N_points=0
        self.X_LogScale=0
        self.Y_LogScale=0
        self.F_choose=0
        self.A_value=0
        self.B_value=0
        self.C_value=0
        self.x_values=0
        self.y_values=0
        self.holdplot=0
        
        super(Plot_window, self).__init__(parent)
        vbox_1=QVBoxLayout()
        
        #Column 1: 'Select the signal parameters'
        #----------------------------------------
        vbox1_l1=QLabel()
        vbox1_l1.setText('Select the signal parameters')
        vbox1_l1.setFont(QFont("Arial",12))
        vbox_1.addWidget(vbox1_l1)
        vbox_1.addStretch()
        
        # X-axis parameters
        vbox1_l2=QLabel()
        vbox1_l2.setText('X-axis parameters')
        vbox1_l2.setFont(QFont("Arial",10))
        vbox_1.addWidget(vbox1_l2)
        X_axis_form=QFormLayout()
        # X_min
        self.e_min=QLineEdit()
        self.e_min.setValidator(QDoubleValidator(-1e12,1e12,5))
        self.e_min.setAlignment(Qt.AlignRight)
        self.e_min.setFont(QFont("Arial",8))
        self.e_min.textEdited.connect(self.Get_min_x)        
        X_axis_form.addRow("Minimum value of X:", self.e_min)
        # X_max
        self.e_max=QLineEdit()
        self.e_max.setValidator(QDoubleValidator(-1e12,1e12,5))
        self.e_max.setAlignment(Qt.AlignRight)
        self.e_max.setFont(QFont("Arial",8))
        self.e_max.textEdited.connect(self.Get_max_x)
        X_axis_form.addRow("Maximum value of X:", self.e_max)
        vbox_1.addLayout(X_axis_form)
        #N_points
        self.e_N=QLineEdit()
        self.e_N.setValidator(QIntValidator())
        self.e_N.setAlignment(Qt.AlignRight)
        self.e_N.setFont(QFont("Arial",8))
        self.e_N.textEdited.connect(self.Get_N)
        X_axis_form.addRow("Number of points:", self.e_N)
        # Select the x-axis scale (Linear/logarithmic) via QComboBox environment
        self.XLLOG_cb = QComboBox()
        self.XLLOG_cb.addItem("Linear")
        self.XLLOG_cb.addItem("Logarithmic")
        self. XLLOG_cb.setFont(QFont("Arial",8))
        self.XLLOG_cb.currentIndexChanged.connect(self.XLLOG_cb_Selectionchange)
        X_axis_form.addRow("X-axis spacing", self.XLLOG_cb)
        vbox_1.addLayout(X_axis_form)
        vbox_1.addStretch()
        
        #'Y-axis parameters'
        vbox1_l3=QLabel()
        vbox1_l3.setText('Y-axis parameters')
        vbox1_l3.setFont(QFont("Arial",10))
        vbox_1.addWidget(vbox1_l3)
        # Select the Y-axis scale (Linear/logarithmic) via QComboBox environment
        self.YLLOG_cb = QComboBox()
        self.YLLOG_cb.addItem("Linear")
        self.YLLOG_cb.addItem("Logarithmic")
        self.YLLOG_cb.setFont(QFont("Arial",8))
        self.YLLOG_cb.currentIndexChanged.connect(self.YLLOG_cb_Selectionchange)
        Y_axis_form=QFormLayout()
        Y_axis_form.addRow("Y-axis spacing", self.YLLOG_cb)
        vbox_1.addLayout(Y_axis_form)
        vbox_1.addStretch()

        #'Select signal shape and parameters'
        vbox1_l4=QLabel()
        vbox1_l4.setText('Select signal')
        vbox1_l4.setFont(QFont("Arial",10))
        vbox_1.addWidget(vbox1_l4)
        # Create function choices via QComboBox environment
        self.F_cb= QComboBox()
        self.F_cb.addItem("y= a sin( b x + c)")
        self.F_cb.addItem("y= a x^2 + b x + c")
        self.F_cb.addItem("y=a log(b x)+ c")
        self.F_cb.currentIndexChanged.connect(self.F_cb_Selectionchange)
        vbox_1.addWidget(self.F_cb)
        # Input parameter values
        Param_form=QFormLayout()
        self.e_a=QLineEdit()
        self.e_a.setValidator(QDoubleValidator(-1e12,1e12,5))
        self.e_a.setAlignment(Qt.AlignRight)
        self.e_a.setFont(QFont("Arial",8))
        self.e_a.textEdited.connect(self.Get_a)
        Param_form.addRow("Value of a =", self.e_a)
        self.e_b=QLineEdit()
        self.e_b.setValidator(QDoubleValidator(-1e12,1e12,5))
        self.e_b.setAlignment(Qt.AlignRight)
        self.e_b.setFont(QFont("Arial",8))
        self.e_b.textEdited.connect(self.Get_b)
        Param_form.addRow("Value of b =", self.e_b)
        self.e_c=QLineEdit()
        self.e_c.setValidator(QDoubleValidator(-1e12,1e12,5))
        self.e_c.setAlignment(Qt.AlignRight)
        self.e_c.setFont(QFont("Arial",8))
        self.e_c.textEdited.connect(self.Get_c)
        Param_form.addRow("Value of c =", self.e_c)
        vbox_1.addLayout(Param_form)
        vbox_1.addStretch()
        # Plot function Push Button 
        self.b_plot=QPushButton("Button1")
        #self.b_plot.setCheckable(True)
        self.b_plot.setFont(QFont("Arial",12))
        self.b_plot.setText('Plot function')
        #self.b_plot.toggle()
        self.b_plot.clicked.connect(self.Evaluate_function)
        vbox_1.addWidget(self.b_plot)


        #Column 2: Plot Window
        #----------------------------------------
        # QtGraph Window
        vbox_2=QVBoxLayout()
        self.myPlotWidget = QtGraph.PlotWidget()
        vbox_2.addWidget(self.myPlotWidget)
        vbox_2.addStretch()
        # Clear graph button
        hbox_c2=QHBoxLayout()
        self.b_clear_plot=QPushButton("Clear Plot")
        #self.b_clear_plot.setCheckable(True)
        self.b_clear_plot.setFont(QFont("Arial",10))
        self.b_clear_plot.setText('Clear Graph')
        self.b_clear_plot.clicked.connect(self.ClearGraph)
        hbox_c2.addWidget(self.b_clear_plot)
        hbox_c2.addStretch()
        # Hold graph button
        layout = QVBoxLayout()
        self.b_holdplot=QPushButton("Hold Plot")
        self.b_holdplot.setCheckable(True)
        self.b_holdplot.clicked.connect(self.b_holdplot_state)
        hbox_c2.addWidget(self.b_holdplot)


        
        vbox_2.addLayout(hbox_c2)
        

         
         
        #Column 3: Functionality buttons
        #----------------------------------------
        # TBD: Adding functions like "Find maximum" "Find minimum"


        # Group vertical columns
        Hbox=QHBoxLayout()
        Hbox.addLayout(vbox_1)
        Hbox.addStretch()
        Hbox.addLayout(vbox_2)
        self.setLayout(Hbox)


 
        
        self.setLayout(vbox_1)
        self.setWindowTitle("ThinkRF signal display")


    def Get_min_x(self,text):     
        self.x_min=float(text)
     
    def Get_max_x(self,text):
        self.x_max=float(text)
    
    def Get_N(self,text):
         self.N_points=int(text)
           
    def XLLOG_cb_Selectionchange(self,i):
        self.X_LogScale=i

    def YLLOG_cb_Selectionchange(self,i):
        self.Y_LogScale=i
 
    def F_cb_Selectionchange(self,i):
        self.F_choose=i

    def Get_a(self,text):
        self.A_value=float(text)

    def Get_b(self,text):
        self.B_value=float(text)

    def Get_c(self,text):
        self.C_value=float(text)
        
    def Evaluate_function(self):
        if self.X_LogScale:
            self.x_min_log=math.log10(self.x_min)
            self.x_max_log=math.log10(self.x_max)
            self.x_values=numpy.logspace(self.x_min_log,self.x_max_log,self.N_points)
        else:
            self.x_values=numpy.linspace(self.x_min,self.x_max,self.N_points)

        y_tmp=[]    
        if self.F_choose==0:
            for index in range(self.N_points):
                y_tmp.append(self.A_value*math.sin(self.B_value* self.x_values[index]+self.C_value))
        elif self.F_choose==1:
            for index in range(self.N_points):
                y_tmp.append((self.A_value* self.x_values[index]**2)+ (self.B_value* self.x_values[index])+(self.C_value))
        elif self.F_choose==2:
            for index in range(self.N_points):
                y_tmp.append(self.A_value*math.log(self.B_value* self.x_values[index])+self.C_value)
        self.y_values=y_tmp
        if self.holdplot==0:
            self.myPlotWidget.clear()
        self.myPlotWidget.plot(self.x_values, self.y_values)
        if self.X_LogScale:
            self.myPlotWidget.setLogMode(x=True)
        if self.Y_LogScale:
            self.myPlotWidget.setLogMode(y=True)

    def ClearGraph(self):
        self.myPlotWidget.clear()

    def b_holdplot_state(self):
        if self.b_holdplot.isChecked():
            self.holdplot=1
        else:
            self.holdplot=0
    
 

def main():
    app = QApplication(sys.argv)
    Plotwin= Plot_window()
    Plotwin.show()
    sys.exit(app.exec_())

    


if __name__ == '__main__':
    main()
