import pandas as pd
from PyQt6.QtWidgets import  QFileDialog,QLabel,QSpinBox,QMessageBox
from PyQt6.QtCore import Qt, QDate
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from scipy.stats import linregress
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np
class MplCanvas(FigureCanvas):
    def __init__(self, parent=None, width=10, height=8, dpi=100):
        fig, (self.ax1, self.ax2) = plt.subplots(2, 1, figsize=(width, height), sharex=True)

        super(MplCanvas, self).__init__(fig)

class MplCanvas2(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas2, self).__init__(fig)

def open_file_dialog(self):
    file_name, _ = QFileDialog.getOpenFileName(self, "Open Excel File", "", "Excel Files (*.xlsx);;All Files (*)")
    if file_name:
        self.data = pd.read_excel(file_name)
        self.data['측정일'] = pd.to_datetime(self.data['측정일'])
        if '측정일' in self.data.columns:
            start_date = self.data['측정일'].iloc[0]
            end_date = self.data['측정일'].iloc[-1]
            self.start_date2.setDate(QDate(start_date.year, start_date.month, start_date.day))
            self.end_date2.setDate(QDate(end_date.year, end_date.month, end_date.day))
            QMessageBox.information(self, "Success", "파일이 성공적으로 업로드되었습니다.")
        else:
            print("'측정일' 열이 데이터에 없습니다.")
    else:
        print('파일 업로드 실패')

def show_time_interval(self, checked):
    if checked:
        self.time = QLabel('Time interval')
        self.time.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.three_layout.addWidget(self.time)
        self.interval = QSpinBox()
        self.interval.setValue(1)
        self.three_layout.addWidget(self.interval)
    else:
        for i in reversed(range(self.three_layout.count())): 
            widget = self.three_layout.itemAt(i).widget()
            if widget is not None: 
                widget.setParent(None)
        self.three_layout.addWidget(self.rb1)
        self.three_layout.addWidget(self.rb2)
        self.three_layout.addWidget(self.rb3)

def basic_plot(self):
    self.canvas.ax1.clear()
    self.canvas.ax2.clear()
    self.canvas2.axes.clear()

    if self.data is not None:
        start_date = self.start_date2.date()
        end_date = self.end_date2.date()
        self.start_date = pd.to_datetime(start_date.toString("yyyy-MM-dd"))
        self.end_date = pd.to_datetime(end_date.toString("yyyy-MM-dd"))
        self.predict_data = self.data[(self.data['측정일'] >= self.start_date) & (self.data['측정일'] <= self.end_date)]
    
    self.locator = mdates.AutoDateLocator()
    self.formatter = mdates.DateFormatter('%Y-%m-%d')
    self.canvas.ax1.plot(self.data['측정일'],self.data['성토고'])
    self.canvas.ax1.grid(True)
    self.canvas.ax1.set_ylabel('성토고 높이 (m)')
    self.canvas.ax1.xaxis.set_major_locator(self.locator)
    self.canvas.ax1.xaxis.set_major_formatter(self.formatter)
    plt.setp(self.canvas.ax1.xaxis.get_majorticklabels(), rotation=45, ha='right')
    self.canvas.ax1.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False)

def update_graph(self):
    self.canvas.ax2.clear()

    if self.selected_button == self.rb1:    

        self.S_final = 1 / self.b - self.so

        self.alpha_input.setText("{:.4f}".format(self.a))
        self.beta_input.setText("{:.4f}".format(self.b))
        self.start_input.setText('{:.4f}cm'.format(self.so))
        self.final_input.setText("{:.4f}cm".format(self.S_final))
        self.t_pred = (self.date_pred - self.start_date).days

        self.S_pred = self.so - self.t_pred / (self.a + self.b * self.t_pred)

        self.canvas.ax2.xaxis.set_major_locator(self.locator)
        self.canvas.ax2.xaxis.set_major_formatter(self.formatter)
        plt.setp(self.canvas.ax2.xaxis.get_majorticklabels(), rotation=45, ha='right')
        self.canvas.ax2.plot(self.date_pred, self.S_pred, 'r-', label='Predicted')

        self.canvas.ax2.scatter(self.date['측정일'], self.raw_settlements,  marker='o',   edgecolors='blue',   facecolors='none',     s=20,  label='Measured')
        self.canvas.ax2.set_ylabel('Settlement (cm)')
        self.canvas.ax2.set_title('Settlement Curve')
        self.canvas.ax2.legend()
        self.canvas.ax2.grid(True)
        plt.tight_layout()

    elif self.selected_button == self.rb2:

        self.S_final = np.sqrt(1 / self.b) - self.so

        self.alpha_input.setText("{:.4f}".format(self.a))
        self.beta_input.setText("{:.4f}".format(self.b))
        self.start_input.setText('{:.4f}cm'.format(self.so))
        self.final_input.setText("{:.4f}cm".format(self.S_final))
        self.date_pred = pd.date_range(start=self.start_date, end=self.end_date + pd.Timedelta(days=int(self.line_edit.text())), freq='D')
        self.t_pred = (self.date_pred - self.start_date).days

        self.S_pred = self.so-np.sqrt(self.t_pred/(self.a + self.b*self.t_pred))
        print(self.S_pred[-3:-1])

        self.canvas.ax2.xaxis.set_major_locator(self.locator)
        self.canvas.ax2.xaxis.set_major_formatter(self.formatter)
        plt.setp(self.canvas.ax2.xaxis.get_majorticklabels(), rotation=45, ha='right')
        self.canvas.ax2.plot(self.date_pred, self.S_pred, 'r-', label='Predicted')

        self.canvas.ax2.scatter(self.date['측정일'], self.raw_settlements,  marker='o',   edgecolors='blue',   facecolors='none',     s=20,  label='Measured')
        self.canvas.ax2.set_ylabel('Settlement (cm)')
        self.canvas.ax2.set_title('Settlement Curve')
        self.canvas.ax2.legend()
        self.canvas.ax2.grid(True)
        plt.tight_layout()
    self.canvas.draw()

def Hyperbolic_plot(self):
    self.t_s=(-self.t[1:]/self.s_diff[1:])
    slope ,intercept,r,p,e = linregress(self.t[1:],self.t_s)
    self.a = intercept
    self.b = slope

    self.S_final = 1 / self.b - self.so

    self.alpha_input.setText("{:.4f}".format(self.a))
    self.beta_input.setText("{:.4f}".format(self.b))
    self.start_input.setText('{:.4f}cm'.format(self.so))
    self.final_input.setText("{:.4f}cm".format(self.S_final))
    self.date_pred = pd.date_range(start=self.start_date, end=self.end_date + pd.Timedelta(days=int(self.line_edit.text())), freq='D')
    self.t_pred = (self.date_pred - self.start_date).days

    self.S_pred = self.so - self.t_pred / (self.a + self.b * self.t_pred)

    self.canvas.ax2.xaxis.set_major_locator(self.locator)
    self.canvas.ax2.xaxis.set_major_formatter(self.formatter)
    plt.setp(self.canvas.ax2.xaxis.get_majorticklabels(), rotation=45, ha='right')
    self.canvas.ax2.plot(self.date_pred, self.S_pred, 'r-', label='Predicted')

    self.canvas.ax2.scatter(self.date['측정일'], self.raw_settlements,  marker='o',   edgecolors='blue',   facecolors='none',     s=20,  label='Measured')
    self.canvas.ax2.set_ylabel('Settlement (cm)')
    self.canvas.ax2.set_title('Settlement Curve')
    self.canvas.ax2.legend()
    self.canvas.ax2.grid(True)
    plt.tight_layout()
    self.canvas.draw()

    self.canvas2.axes.scatter(self.t[1:], self.t_s, label='Measured')
    self.regression_line, = self.canvas2.axes.plot(self.t[1:], self.a + self.b * self.t[1:], 'r-', label='Regression Line')
    self.canvas2.axes.set_xlabel('(t - to) day')
    self.canvas2.axes.set_ylabel('(t - to) / (St - So)')
    self.canvas2.axes.set_title('Hyperbolic Method: Date vs t/(St-So)')
    self.canvas2.axes.legend()
    self.canvas2.axes.grid(True)
    self.canvas2.draw()

def Hosino_plot(self):
    self.t_s=(self.t[1:]/(self.s_diff[1:])**2)
    slope, intercept, r_value, p_value, std_err = linregress(self.t[1:], self.t_s)
    self.a = intercept
    self.b = slope

    self.S_final = np.sqrt(1 / self.b) - self.so

    self.alpha_input.setText("{:.4f}".format(self.a))
    self.beta_input.setText("{:.4f}".format(self.b))
    self.start_input.setText('{:.4f}cm'.format(self.so))
    self.final_input.setText("{:.4f}cm".format(self.S_final))
    self.date_pred = pd.date_range(start=self.start_date, end=self.end_date + pd.Timedelta(days=int(self.line_edit.text())), freq='D')
    self.t_pred = (self.date_pred - self.start_date).days
    self.S_pred = self.so-np.sqrt(self.t_pred/(self.a + self.b*self.t_pred))
    self.canvas.ax2.xaxis.set_major_locator(self.locator)
    self.canvas.ax2.xaxis.set_major_formatter(self.formatter)
    plt.setp(self.canvas.ax2.xaxis.get_majorticklabels(), rotation=45, ha='right')
    self.canvas.ax2.plot(self.date_pred, self.S_pred, 'r-', label='Predicted')
 
    self.canvas.ax2.scatter(self.date['측정일'], self.raw_settlements,  marker='o',   edgecolors='blue',   facecolors='none',     s=20,  label='Measured')
    self.canvas.ax2.set_ylabel('Settlement (cm)')
    self.canvas.ax2.set_title('Settlement Curve')
    self.canvas.ax2.legend()
    self.canvas.ax2.grid(True)
    plt.tight_layout()
    self.canvas.draw()
    self.canvas2.axes.scatter(self.t[1:], self.t_s, label='Measured')
    self.regression_line, = self.canvas2.axes.plot(self.t[1:], self.a + self.b * self.t[1:], 'r-', label='Regression Line')
    self.canvas2.axes.set_xlabel('(t - to) day')
    self.canvas2.axes.set_ylabel('(t - to) / (St - So)^2')
    self.canvas2.axes.set_title('Hosino Method: Date vs t/(St-So)^2')
    self.canvas2.axes.legend()
    self.canvas2.axes.grid(True)
    self.canvas2.draw()

def Asaoka_plot(self):
    self.s1 = self.Settlements[:-1:self.interval.value()]
    self.s2 = self.Settlements[1::self.interval.value()]

    b0, a0, r_value, p_value, std_err = linregress(self.s1, self.s2)
    b1, a1, r_value, p_value, std_err = linregress(self.s2, self.s1)

    self.canvas2.axes.plot( self.s1,a0+b0*self.s1)
    self.canvas2.axes.plot( self.s2,a1+b1*self.s2)
    self.canvas2.axes.plot(self.s1,self.s2)
    # self.regression_line, = self.canvas2.axes.plot(self.t[1:], self.a + self.b * self.t[1:], 'r-', label='Regression Line')
    self.canvas2.axes.set_xlabel('Si (cm)')
    self.canvas2.axes.set_ylabel('Si-1 (cm)')
    self.canvas2.axes.set_title('Asaoka Method')
    self.canvas2.axes.legend()
    self.canvas2.axes.grid(True)
    self.canvas2.draw()

def check_method(self, button):
    basic_plot(self)
    self.date=self.data[self.data['측정일']<self.end_date]
    self.raw_settlements = self.date['침하량']
    self.Settlements = self.predict_data['침하량']
    self.t = (self.predict_data['측정일']-self.start_date).dt.days
    self.so = self.Settlements.iloc[0]
    self.s_diff = self.Settlements - self.so
    if button == self.rb1:
        Hyperbolic_plot(self)
    elif button == self.rb2:
        Hosino_plot(self)
    elif button == self.rb3:
        Asaoka_plot(self)
