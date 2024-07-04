import sys
import pandas as pd
from PyQt6.QtWidgets import QGridLayout,QLineEdit,QFrame,QDateEdit, QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QRadioButton, QWidget, QLabel, QButtonGroup, QPushButton
from PyQt6.QtCore import Qt, QDate
import matplotlib
matplotlib.use('QtAgg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from scipy.stats import linregress
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
from etc import *
from mpl_interactions import panhandler, zoom_factory
from datetime import datetime
import os
plt.rcParams['font.family'] = 'Malgun Gothic'  # 한글 폰트로 나눔고딕 설정
plt.rcParams['axes.unicode_minus'] =False



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        #변수 초기화
        self.a = 0.0
        self.b = 0.0
        self.sf = 0.0
        self.so=0.0
        self.data = None

        self.setWindowTitle("침하량 데이터 분석")
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout(main_widget) #메인 세로
        top_layout = QVBoxLayout() #세로 레이아웃
        one_layout = QHBoxLayout() #가로 레이아웃
        two_layout = QHBoxLayout()
        self.three_layout = QHBoxLayout()
        #업로드
        upload = QLabel('Upload : ')
        upload.setAlignment(Qt.AlignmentFlag.AlignCenter)
        one_layout.addWidget(upload)
        upload_button = QPushButton('Upload File')
        upload_button.clicked.connect(lambda: open_file_dialog(self)) 
        one_layout.addWidget(upload_button)

        #예측 날짜
        time = QLabel('예측할 날짜 : ')
        time.setAlignment(Qt.AlignmentFlag.AlignCenter)
        one_layout.addWidget(time)
        self.line_edit = QLineEdit(self)
        self.line_edit.setPlaceholderText("숫자를 입력하세요")
        one_layout.addWidget(self.line_edit)
        top_layout.addLayout(one_layout)  # 여기서 addWidget 대신 addLayout 사용

        #분석 시작 종료 날짜
        start = QLabel('Start Date : ')
        start.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.start_date2 = QDateEdit()
        self.start_date2.setCalendarPopup(True)
        end = QLabel('End Date : ')
        end.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.end_date2 = QDateEdit()
        self.end_date2.setCalendarPopup(True)
        two_layout.addWidget(start)
        two_layout.addWidget( self.start_date2)
        two_layout.addWidget(end)
        two_layout.addWidget(self.end_date2)
        top_layout.addLayout(two_layout)

        #분석 방법
        method_label = QLabel('Analysis method')
        method_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.button_group = QButtonGroup()
        self.button_group.setExclusive(True)
        self.rb1 = QRadioButton("Hyperbolic 방법",self)
        self.rb2 = QRadioButton("Hosino 방법",self)
        self.rb3 = QRadioButton("Asaoka 방법",self)
        self.rb3.toggled.connect(lambda checked: show_time_interval(self, checked))
        self.three_layout.addWidget(self.rb1)
        self.three_layout.addWidget(self.rb2)
        self.three_layout.addWidget(self.rb3)     
        self.button_group.addButton(self.rb1)
        self.button_group.addButton(self.rb2)
        self.button_group.addButton(self.rb3)
        self.button_group.buttonClicked.connect(lambda button : check_method(self,button))
        top_layout.addLayout(self.three_layout)
        main_layout.addLayout(top_layout)


        
        four_layout = QHBoxLayout()
        five_layout = QVBoxLayout()
        grid_layout = QGridLayout()
        utils_layout = QHBoxLayout()

        self.canvas = MplCanvas(self, width=10, height=8, dpi=100)
        self.canvas2 = MplCanvas2(self, width=4, height=1.5, dpi=100)
        self.canvas.setFixedSize(800, 600)
        self.canvas2.setFixedSize(400, 370)
        self.selected_button = self.button_group.checkedButton()


        self.alpha = QLabel('α:')
        self.beta = QLabel('β:')
        self.alpha_input = QLabel(str(self.a))
        self.beta_input = QLabel(str(self.b))
        start = QLabel('Start Settlemint(ST)')
        self.start_input = QLabel(str(self.so))
        final = QLabel('Final Settlement(Sf)')
        self.final_input = QLabel(str(self.sf))

        
        grid_layout.addWidget(self.alpha, 0, 0)
        grid_layout.addWidget(self.alpha_input, 0, 1)
        grid_layout.addWidget(self.beta, 1, 0)
        grid_layout.addWidget(self.beta_input, 1, 1)
        grid_layout.addWidget(start, 2, 0)
        grid_layout.addWidget(self.start_input, 2, 1)
        grid_layout.addWidget(final, 3, 0)
        grid_layout.addWidget(self.final_input, 3, 1)

        save = QPushButton('Save')
        save.clicked.connect(self.savefile)
        line = QPushButton('Draw regression_line')
        line.clicked.connect(self.clear_specific_graph)

        utils_layout.addWidget(save)
        utils_layout.addWidget(line)

        four_layout.addWidget(self.canvas)
        five_layout.addLayout(utils_layout)
        five_layout.addWidget(self.canvas2)
        five_layout.addLayout(grid_layout)
        four_layout.addLayout(five_layout)

        main_layout.addLayout(four_layout)



        # 레이아웃에 스타일 시트 적용

        self.setStyleSheet("""
            QLabel {
                font-size: 14px;
                color: #333;
                margin-bottom: 5px;
            }
            QLineEdit {
                font-size: 14px;
                padding: 5px;
                border: 1px solid #ccc;
                border-radius: 3px;
            }
            QPushButton {
                background-color: #4CAF50;
                border: none;
                color: white;
                padding: 10px 20px;
                text-align: center;
                text-decoration: none;
                font-size: 16px;
                margin: 4px 2px;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
    def savefile(self):
        folder_path = "C:/settlement/"
        if not os.path.exists(folder_path):
            os.mkdir(folder_path)
        current_date = datetime.now().strftime("%Y-%m-%d")  # 날짜 형식을 YYYY-MM-DD로 설정
        self.selected_button = self.button_group.checkedButton()

        if self.selected_button == self.rb1:
            file = pd.DataFrame({
                '초기 실측침하량': [self.so],
                '최종 실측침하량': [self.sl],
                'α': [self.a],
                'β': [self.b],
                '최종 침하량': [self.S_final],
                '잔류침하량': [self.S_final-self.sl],
                '압밀도': [self.sl/self.S_final*100]
            })
            file.to_csv(os.path.join(folder_path, f"{current_date}_Hyperbolic.csv"), index=False, encoding='cp949')
            self.canvas.figure.savefig(os.path.join(folder_path, f"{current_date}_Hyperbolic.png"))

        elif self.selected_button == self.rb2:
            file = pd.DataFrame({
                '초기 실측침하량': [self.so],
                '최종 실측침하량': [self.sl],
                'α': [self.a],
                'β': [self.b],
                '최종 침하량': [self.S_final],
                '잔류침하량': [self.S_final-self.sl],
                '압밀도': [self.sl/self.S_final*100]
            })
            file.to_csv(os.path.join(folder_path, f"{current_date}_Hosino.csv"), index=False, encoding='cp949')
            self.canvas.figure.savefig(os.path.join(folder_path, f"{current_date}_Hosino.png"))

        elif self.selected_button == self.rb3:
            file = pd.DataFrame({
                '초기 실측침하량': [self.so],
                '최종 실측침하량': [self.sl],
                'β2': [self.a],
                'β1': [self.b],
                '최종 침하량': [self.S_final],
                '잔류침하량': [self.S_final-self.sl],
                '압밀도': [self.sl/self.S_final*100]
            })
            file.to_csv(os.path.join(folder_path, f"{current_date}_Asaoka.csv"), index=False, encoding='cp949')
            self.canvas.figure.savefig(os.path.join(folder_path, f"{current_date}_Asaoka.png"))


        QMessageBox.information(self, "Success", "파일이 성공적으로 저장되었습니다.")


    def clear_specific_graph(self):
        self.points= []
        self.alpha_input.setText('0.0')
        self.beta_input.setText('0.0')
        self.start_input.setText('0.0')
        self.final_input.setText('0.0')
        if hasattr(self, 'regression_line') and self.regression_line is not None:
            self.regression_line.remove()
            self.regression_line = None
            self.canvas2.draw()
        self.selected_button = self.button_group.checkedButton()
        if self.selected_button==self.rb3:
            self.inter.remove()
            self.xcross.remove()
            self.ycross.remove()
            self.text.remove()
            self.text=None
            self.inter = None
            self.xcross = None
            self.ycross = None
            self.canvas2.draw()

        self.canvas2.mpl_connect('button_press_event', self.onclick)

    def onclick(self,event):
        if event.inaxes == self.canvas2.axes:
            x = event.xdata
            y = event.ydata
            if x is not None and y is not None:
                if len(self.points)<2:
                    if hasattr(self, 'regression_line') and self.regression_line is not None:
                        # 기존의 선을 업데이트
                        self.points.append((x, y))
                        x_data, y_data = zip(*self.points)
                        self.regression_line.set_data(x_data, y_data)
                    else:
                        # 새로운 선을 그리는 경우
                        self.points = [(x, y)]
                        x_data, y_data = zip(*self.points)
                        self.regression_line, = self.canvas2.axes.plot(x_data, y_data,'r-')
                self.canvas2.draw()
        if len(self.points)==2:
            slope = (y_data[1] - y_data[0]) / (x_data[1] - x_data[0])
            intercept = y_data[0] - slope * x_data[0]
            self.a = intercept
            self.b = slope
            update_graph(self)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    window = MainWindow()
    window.show()
    
    app.exec()
