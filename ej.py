import sys
import pandas as pd
from PyQt6.QtWidgets import QGridLayout,QLineEdit,QFrame,QSpinBox, QDateEdit, QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QRadioButton, QWidget, QLabel, QButtonGroup, QPushButton, QFileDialog
from PyQt6.QtCore import Qt, QDate
import matplotlib
matplotlib.use('QtAgg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from scipy.stats import linregress
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams['font.family'] = 'Malgun Gothic'  # 한글 폰트로 나눔고딕 설정
plt.rcParams['axes.unicode_minus'] =False
class MplCanvas(FigureCanvas):
    def __init__(self, parent=None, width=10, height=8, dpi=100):
        fig, (self.ax1, self.ax2) = plt.subplots(2, 1, figsize=(width, height), sharex=True)

        super(MplCanvas, self).__init__(fig)

class MplCanvas2(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas2, self).__init__(fig)

        self.cid = self.mpl_connect('button_press_event', self.on_click)
        self.points = []

    def on_click(self, event):
        if event.inaxes != self.axes:
            return

        # 클릭된 점의 처리
        if event.button == 1:  # 좌클릭일 때
            self.points.append((event.xdata, event.ydata))
            self.axes.plot(event.xdata, event.ydata, 'ro')

        elif event.button == 3 and self.points:  # 우클릭일 때
            self.remove_regression_line()  # 회귀선 제거
            self.points.pop()  # 마지막 점 제거

        # 두 점이 있을 때 회귀선 그리기
        if len(self.points) == 2:
            x_coords, y_coords = zip(*self.points)
            self.axes.plot(x_coords, y_coords, 'r-')

        self.draw()

    def remove_regression_line(self):
        if hasattr(self, 'regression_line'):
            for line in self.regression_line:
                line.remove()
            self.regression_line = None
            self.draw()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("침하량 데이터 분석")

        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout(main_widget)
        main_layout.setContentsMargins(10, 10, 10, 10)  # 레이아웃 여백 설정
        main_layout.setSpacing(10)  # 위젯 간 간격 설정

        hline = QFrame()
        hline.setFrameShape(QFrame.Shape.HLine)
        hline.setFrameShadow(QFrame.Shadow.Sunken)

        vline = QFrame()
        vline.setFrameShape(QFrame.Shape.VLine)
        vline.setFrameShadow(QFrame.Shadow.Sunken)

        layout = QVBoxLayout()
        layout.setContentsMargins(5, 5, 5, 5)  # 레이아웃 여백 설정
        layout.setSpacing(5)  # 위젯 간 간격 설정

        upload_layout = QHBoxLayout()
        upload_layout.setContentsMargins(5, 5, 5, 5)  # 레이아웃 여백 설정
        upload_layout.setSpacing(5)  # 위젯 간 간격 설정

        #파일 업로드
        upload_label = QLabel('파일 업로드')
        upload_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        upload_label.setFixedSize(120, 20)  # 레이블 크기 설정
        upload_layout.addWidget(upload_label)
        upload_layout.addWidget(vline)
        self.upload_button = QPushButton("Upload File")
        self.upload_button.clicked.connect(self.open_file_dialog)
        upload_layout.addWidget(self.upload_button)
        layout.addLayout(upload_layout) 

        # 예측할 날짜 입력
        time_layout = QHBoxLayout()
        time_layout.setContentsMargins(5, 5, 5, 5)  # 레이아웃 여백 설정
        time_layout.setSpacing(5)  # 위젯 간 간격 설정

        time_label = QLabel('예측할 날짜')
        time_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        time_label.setFixedSize(120, 20)  # 레이블 크기 설정
        time_layout.addWidget(time_label)
        self.line_edit = QLineEdit(self)
        self.line_edit.setPlaceholderText("숫자를 입력하세요")
        time_layout.addWidget(self.line_edit)
        layout.addLayout(time_layout)  # 여기서 addWidget 대신 addLayout 사용

        # 날짜 선택 위젯 추가
        v_layout = QHBoxLayout()
        v_layout.setContentsMargins(5, 5, 5, 5)  # 레이아웃 여백 설정
        v_layout.setSpacing(5)  # 위젯 간 간격 설정

        start = QLabel('분석 시작일 선택')
        start.setAlignment(Qt.AlignmentFlag.AlignCenter)
        start.setFixedSize(120, 20)  # 레이블 크기 설정
        v_layout.addWidget(start)
        self.start_date2 = QDateEdit()
        self.start_date2.setCalendarPopup(True)
        v_layout.addWidget(self.start_date2)
        v_layout.addWidget(vline)
        end = QLabel('분석 종료일 선택')
        end.setAlignment(Qt.AlignmentFlag.AlignCenter)
        end.setFixedSize(120, 20)  # 레이블 크기 설정
        v_layout.addWidget(end)
        self.end_date2 = QDateEdit()
        self.end_date2.setCalendarPopup(True)
        v_layout.addWidget(self.end_date2)

        layout.addLayout(v_layout)
        main_layout.addLayout(layout)
        main_layout.addWidget(hline)

        # 분석 방법 선택
        method_layout = QHBoxLayout()
        method_label = QLabel('Analysis method')
        method_label.setFixedSize(1200, 20)  # 레이블 크기 설정
        method_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(method_label)

        self.h_layout = QHBoxLayout()
        self.h_layout.setContentsMargins(5, 5, 5, 5)  # 레이아웃 여백 설정
        self.h_layout.setSpacing(5)  # 위젯 간 간격 설정

        self.button_group = QButtonGroup()
        self.button_group.setExclusive(True)
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
        
        # 데이터 그리기
        draw_layout = QHBoxLayout()
        regression_layout = QVBoxLayout()
        grid = QGridLayout()
        self.canvas = MplCanvas(self, width=10, height=8, dpi=100)
        self.canvas2 = MplCanvas2(self, width=4, height=1.5, dpi=100)
        self.canvas.setFixedSize(800, 600)
        self.canvas2.setFixedSize(400, 370)
        draw_layout.addWidget(self.canvas)

        save = QPushButton('Save')
        regression_layout.addWidget(save)
        regression_layout.addWidget(self.canvas2)
        self.a = 0.0  # 초기값 설정
        self.b = 0.0  # 초기값 설정
        self.S_final = 0.0
        alpha = QLabel('α:')
        self.alpha_input = QLabel(str(self.a))

        beta = QLabel('β:')
        self.beta_input = QLabel(str(self.b))

        final = QLabel('Final Settlement(Sf)')
        self.final_input = QLabel(str(self.S_final))

        alpha.setFixedSize(120, 20)  # 레이블 크기 설정
        beta.setFixedSize(120, 20)  # 레이블 크기 설정
        final.setFixedSize(120, 20)  # 레이블 크기 설정


        grid.addWidget(alpha, 0, 0)
        grid.addWidget(self.alpha_input, 0, 1)
        grid.addWidget(beta, 1, 0)
        grid.addWidget(self.beta_input, 1, 1)
        grid.addWidget(final, 2, 0)
        grid.addWidget(self.final_input, 2, 1)
        grid.setSpacing(30)
        regression_layout.addLayout(grid)
        draw_layout.addLayout(regression_layout)
        main_layout.addLayout(draw_layout)
        
        self.data = None  # 데이터 초기화
        
    def check_method(self, button):
        if button == self.rb1:
            self.Hyperbolic_plot()

        elif button == self.rb2:
            self.Hosino_plot()
        # elif button == self.rb3:
        #     self.Asaoka_plot()
        #     self.Asaoka_plot2()

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
                self.start_date2.setDate(QDate(start_date.year, start_date.month, start_date.day))
                self.end_date2.setDate(QDate(end_date.year, end_date.month, end_date.day))

            else:
                print("'측정일' 열이 데이터에 없습니다.")


    def basic_plot(self):
        if self.data is not None:
            start_date = self.start_date2.date()
            end_date = self.end_date2.date()
            self.start_date = pd.to_datetime(start_date.toString("yyyy-MM-dd"))
            self.end_date = pd.to_datetime(end_date.toString("yyyy-MM-dd"))
            self.common_data = self.data[(self.data['측정일'] >= self.start_date) & (self.data['측정일'] <= self.end_date)]
        
        self.locator = mdates.AutoDateLocator()
        self.formatter = mdates.DateFormatter('%Y-%m-%d')
        self.canvas.ax1.plot(self.data['측정일'],self.data['성토고'])
        self.canvas.ax1.grid(True)
        self.canvas.ax1.set_ylabel('성토고 높이 (m)')
        self.canvas.ax1.xaxis.set_major_locator(self.locator)
        self.canvas.ax1.xaxis.set_major_formatter(self.formatter)
        plt.setp(self.canvas.ax1.xaxis.get_majorticklabels(), rotation=45, ha='right')
        self.canvas.ax1.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False)

    def Hyperbolic_plot(self):
        self.canvas.ax1.clear()
        self.canvas.ax2.clear()
        self.canvas2.axes.clear()

        self.basic_plot()
        settlements = self.data['침하량']
        settlements2 = self.common_data['침하량']
        t = (self.common_data['측정일'] - self.start_date).dt.days
        So = settlements2.iloc[0]

        # St-So 계산
        S_diff = settlements2 - So

        t_s=(-t[1:]/S_diff[1:])
        slope, intercept, r_value, p_value, std_err = linregress(t[1:], t_s)
        self.a = intercept
        self.b = slope
        self.S_final = 1 / self.b + So*-1
        self.alpha_input.setText("{:.4f}".format(self.a))
        self.beta_input.setText("{:.4f}".format(self.b))
        self.final_input.setText("{:.4f}cm".format(self.S_final))
        date_pred = pd.date_range(start=self.start_date, end=self.end_date + pd.Timedelta(days=int(self.line_edit.text())), freq='D')
        t_pred = (date_pred - self.start_date).days
        S_pred = So - t_pred / (self.a + self.b * t_pred)
        # 원본 침하 곡선

        self.canvas.ax2.xaxis.set_major_locator(self.locator)
        self.canvas.ax2.xaxis.set_major_formatter(self.formatter)
        plt.setp(self.canvas.ax2.xaxis.get_majorticklabels(), rotation=45, ha='right')
        self.canvas.ax2.plot(date_pred, S_pred, 'r-', label='Predicted')
        self.canvas.ax2.scatter(self.data['측정일'], settlements, label='Measured')
        self.canvas.ax2.set_ylabel('Settlement (cm)')
        self.canvas.ax2.set_title('Settlement Curve')
        self.canvas.ax2.legend()
        self.canvas.ax2.grid(True)

        plt.tight_layout()
        self.canvas.draw()

        self.canvas2.axes.scatter(t[1:], t_s, label='Measured')
        self.regression_line = self.canvas2.axes.plot(t[1:], self.a + self.b * t[1:], 'r-', label='Regression Line')
        self.canvas2.axes.set_xlabel('(t - to) day')
        self.canvas2.axes.set_ylabel('(t - to) / (St - So)')
        self.canvas2.axes.set_title('Hyperbolic Method: Date vs t/(St-So)')
        self.canvas2.axes.legend()
        self.canvas2.axes.grid(True)
        self.canvas2.draw()

    def Hosino_plot(self):
        self.canvas.ax1.clear()
        self.canvas.ax2.clear()
        self.canvas2.axes.clear()

        self.basic_plot()
        settlements = self.data['침하량']
        settlements2 = self.common_data['침하량']
        t = (self.common_data['측정일'] - self.start_date).dt.days
        So = settlements2.iloc[0]
        S_diff = settlements2 - So
        t_s=(t[1:]/(S_diff[1:])**2)
        print(t_s)

        slope, intercept, r_value, p_value, std_err = linregress(t[1:], t_s)
        self.a = intercept
        self.b = slope
        self.S_final = np.sqrt(1 / self.b) + So
        self.alpha_input.setText("{:.4f}".format(self.a))
        self.beta_input.setText("{:.4f}".format(self.b))
        self.final_input.setText("{:.4f}cm".format(self.S_final))

        date_pred = pd.date_range(start=self.start_date, end=self.end_date + pd.Timedelta(days=int(self.line_edit.text())), freq='D')
        prediction_df = pd.DataFrame({'Date': t ,'settlements':settlements2})
        prediction_df.to_csv('predicted_settlement.csv', index=False)    

        t_pred = (date_pred - self.start_date).days
        S_pred = So + (self.S_final - So) * (t_pred / (t_pred + ((self.S_final - So) ** 2) / self.b))
        self.canvas.ax2.xaxis.set_major_locator(self.locator)
        self.canvas.ax2.xaxis.set_major_formatter(self.formatter)
        plt.setp(self.canvas.ax2.xaxis.get_majorticklabels(), rotation=45, ha='right')
        self.canvas.ax2.plot(date_pred, S_pred, 'r-', label='Predicted')
        self.canvas.ax2.scatter(self.data['측정일'], settlements, label='Measured')
        self.canvas.ax2.set_ylabel('Settlement (cm)')
        self.canvas.ax2.set_title('Settlement Curve')
        self.canvas.ax2.legend()
        self.canvas.ax2.grid(True)

        plt.tight_layout()
        self.canvas.draw()
        
        
        
        self.canvas2.axes.scatter(t[1:], t_s, label='Measured')
        self.regression_line = self.canvas2.axes.plot(t[1:], self.a + self.b * t[1:], 'r-', label='Regression Line')
        self.canvas2.axes.set_xlabel('(t - to) day')
        self.canvas2.axes.set_ylabel('(t - to) / (St - So)^2')
        self.canvas2.axes.set_title('Hosino Method: Date vs t/(St-So)^2')
        self.canvas2.axes.legend()
        self.canvas2.axes.grid(True)
        self.canvas2.draw()



    # def Asaoka_plot(self):
    #     self.canvas.axes.clear()

    #     start_date = self.qdate_to_datetime(self.start_date.date())
    #     end_date = self.qdate_to_datetime(self.end_date.date())
    #     Asaoka_data = self.data[(self.data['측정일']>=start_date) &(self.data['측정일']<=end_date) ]
    #     self.canvas.axes.plot(Asaoka_data['측정일'], Asaoka_data['성토고'], label='Hyperbolic Method')
        
    #     self.canvas.axes.set_title('Asaoka Method')
    #     self.canvas.axes.set_xlabel('Time')
    #     self.canvas.axes.set_ylabel('H(m)')
    #     self.canvas.axes.legend()
    #     self.canvas.draw()
if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    window = MainWindow()
    window.resize(1200,900)
    window.show()
    
    app.exec()