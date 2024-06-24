import sys
import pandas as pd
from PyQt6.QtWidgets import QSpinBox, QDateEdit, QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QRadioButton, QWidget, QLabel, QButtonGroup, QPushButton, QFileDialog
from PyQt6.QtCore import Qt, QDate
import matplotlib
matplotlib.use('QtAgg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure

class MplCanvas(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)

class MplCanvas2(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas2, self).__init__(fig)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("침하량 데이터 분석")
        
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout(main_widget)

        # 파일 업로드 버튼
        upload = QLabel('파일 업로드')
        upload.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(upload)
        self.upload_button = QPushButton("Upload File")
        self.upload_button.clicked.connect(self.open_file_dialog)
        main_layout.addWidget(self.upload_button)    

        # 날짜 선택 위젯 추가
        v_layout = QVBoxLayout()
        start = QLabel('분석 시작일 선택')
        start.setAlignment(Qt.AlignmentFlag.AlignCenter)
        v_layout.addWidget(start)
        self.start_date = QDateEdit()
        self.start_date.setCalendarPopup(True)
        v_layout.addWidget(self.start_date)
        end = QLabel('분석 종료일 선택')
        end.setAlignment(Qt.AlignmentFlag.AlignCenter)
        v_layout.addWidget(end)
        self.end_date = QDateEdit()
        self.end_date.setCalendarPopup(True)
        v_layout.addWidget(self.end_date)
        main_layout.addLayout(v_layout)
        
        #분석 방법 선택
        method_label = QLabel('Analysis method')
        method_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(method_label)

        self.h_layout = QHBoxLayout()
        self.button_group = QButtonGroup()
        self.button_group.setExclusive(True)  # Exclusive를 True로 설정
        self.rb1 = QRadioButton("Hyperbolic 방법")
        self.rb2 = QRadioButton("Hosino 방법")
        self.rb3 = QRadioButton("Asaoka 방법")
        self.rb3.toggled.connect(self.show_time_interval)
        self.h_layout.addWidget(self.rb1)
        self.h_layout.addWidget(self.rb2)
        self.h_layout.addWidget(self.rb3)     
        main_layout.addLayout(self.h_layout)
        self.button_group.addButton(self.rb1)
        self.button_group.addButton(self.rb2)
        self.button_group.addButton(self.rb3)
        self.button_group.buttonClicked.connect(self.check_method)
        
        #데이터 그리기
        self.canvas = MplCanvas(self, width=5, height=4, dpi=100)
        main_layout.addWidget(self.canvas)
        self.canvas2 = MplCanvas2(self, width=5, height=4, dpi=100)
        main_layout.addWidget(self.canvas2)        
        self.data = None  # 데이터 초기화
        
    def check_method(self, button):
        if button == self.rb1:
            self.Hyperbolic_plot()
            self.Hyperbolic_plot2()

        elif button == self.rb2:
            self.Hosino_plot()
            self.Hosino_plot2()
        elif button == self.rb3:
            self.Asaoka_plot()
            self.Asaoka_plot2()

    def show_time_interval(self, checked):
        if checked:
            time = QLabel('Time interval')
            time.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.h_layout.addWidget(time)
            self.interval = QSpinBox()
            self.interval.setValue(1)
            self.h_layout.addWidget(self.interval)
        else:
            for i in reversed(range(self.h_layout.count())): 
                widget = self.h_layout.itemAt(i).widget()
                if widget is not None: 
                    widget.setParent(None)
            self.h_layout.addWidget(self.rb1)
            self.h_layout.addWidget(self.rb2)
            self.h_layout.addWidget(self.rb3)

    def open_file_dialog(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Open Excel File", "", "Excel Files (*.xlsx);;All Files (*)")
        if file_name:
            self.data = pd.read_excel(file_name)
            self.data['측정일'] = pd.to_datetime(self.data['측정일'])
            if '측정일' in self.data.columns:
                start_date = self.data['측정일'].iloc[0]
                end_date = self.data['측정일'].iloc[-1]
                self.start_date.setDate(QDate(start_date.year, start_date.month, start_date.day))
                self.end_date.setDate(QDate(end_date.year, end_date.month, end_date.day))
            else:
                print("'측정일' 열이 데이터에 없습니다.")
    def qdate_to_datetime(self, qdate):
        return pd.to_datetime(f"{qdate.year()}-{qdate.month()}-{qdate.day()}")


    def Hyperbolic_plot(self):
        self.canvas.axes.clear()
        if self.data is not None:
            start_date = self.qdate_to_datetime(self.start_date.date())
            end_date = self.qdate_to_datetime(self.end_date.date())
            Hyperbolic_data = self.data[(self.data['측정일']>=start_date) &(self.data['측정일']<=end_date) ]
            self.canvas.axes.plot(Hyperbolic_data['측정일'], Hyperbolic_data['성토고'], label='Hyperbolic Method')
        else:
            self.canvas.axes.plot([1, 2, 3, 4, 5], [1, 2, 3, 4, 5], label='Example Data')
        
        self.canvas.axes.set_title('Hyperbolic Method')
        self.canvas.axes.set_xlabel('Time')
        self.canvas.axes.set_ylabel('H(m)')
        self.canvas.axes.legend()
        self.canvas.draw()

    def Hyperbolic_plot2(self):
        self.canvas2.axes.clear()
        if self.data is not None:
            start_date = self.qdate_to_datetime(self.start_date.date())
            end_date = self.qdate_to_datetime(self.end_date.date())
            Hyperbolic_data = self.data[(self.data['측정일']>=start_date) &(self.data['측정일']<=end_date) ]
            self.canvas2.axes.plot(Hyperbolic_data['측정일'], Hyperbolic_data['침하량'], label='Hyperbolic Method')
        else:
            self.canvas.axes.plot([1, 2, 3, 4, 5], [1, 2, 3, 4, 5], label='Example Data')
        
        self.canvas2.axes.set_title('Hyperbolic Method')
        self.canvas2.axes.set_xlabel('Time')
        self.canvas2.axes.set_ylabel('Settlement(mm)')
        self.canvas2.axes.legend()
        self.canvas2.draw()

    def Hosino_plot(self):
        self.canvas.axes.clear()
        start_date = self.qdate_to_datetime(self.start_date.date())
        end_date = self.qdate_to_datetime(self.end_date.date())
        Hosino_data = self.data[(self.data['측정일']>=start_date) &(self.data['측정일']<=end_date) ]
        self.canvas.axes.plot(Hosino_data['측정일'], Hosino_data['성토고'], label='Hyperbolic Method')

        
        self.canvas.axes.set_title('Hosino Method')
        self.canvas.axes.set_xlabel('Time')
        self.canvas.axes.set_ylabel('H(m)')
        self.canvas.axes.legend()
        self.canvas.draw()

    def Hosino_plot2(self):
        self.canvas2.axes.clear()

        start_date = self.qdate_to_datetime(self.start_date.date())
        end_date = self.qdate_to_datetime(self.end_date.date())
        Hosino_data = self.data[(self.data['측정일']>=start_date) &(self.data['측정일']<=end_date) ]
        self.canvas2.axes.plot(Hosino_data['측정일'], Hosino_data['침하량'], label='Hyperbolic Method')

        
        self.canvas2.axes.set_title('Hosino Method')
        self.canvas2.axes.set_xlabel('Time')
        self.canvas2.axes.set_ylabel('Settlement(mm)')
        self.canvas2.axes.legend()
        self.canvas2.draw()

    def Asaoka_plot(self):
        self.canvas.axes.clear()

        start_date = self.qdate_to_datetime(self.start_date.date())
        end_date = self.qdate_to_datetime(self.end_date.date())
        Asaoka_data = self.data[(self.data['측정일']>=start_date) &(self.data['측정일']<=end_date) ]
        self.canvas.axes.plot(Asaoka_data['측정일'], Asaoka_data['성토고'], label='Hyperbolic Method')
        
        self.canvas.axes.set_title('Asaoka Method')
        self.canvas.axes.set_xlabel('Time')
        self.canvas.axes.set_ylabel('H(m)')
        self.canvas.axes.legend()
        self.canvas.draw()

    def Asaoka_plot2(self):
        self.canvas2.axes.clear()

        start_date = self.qdate_to_datetime(self.start_date.date())
        end_date = self.qdate_to_datetime(self.end_date.date())
        Asaoka_data = self.data[(self.data['측정일']>=start_date) &(self.data['측정일']<=end_date) ]
        self.canvas2.axes.plot(Asaoka_data['측정일'], Asaoka_data['침하량'], label='Hyperbolic Method')
        
        self.canvas2.axes.set_title('Asaoka Method')
        self.canvas2.axes.set_xlabel('Time')
        self.canvas2.axes.set_ylabel('Settlement(mm)')
        self.canvas2.axes.legend()
        self.canvas2.draw()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    window = MainWindow()
    window.setGeometry(450,30, 900, 1000)
    window.show()
    
    app.exec()