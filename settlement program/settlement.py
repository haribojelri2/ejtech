import sys
import pandas as pd
from PyQt6.QtWidgets import QGridLayout,QLineEdit,QFrame,QDateEdit, QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QRadioButton, QWidget, QLabel, QButtonGroup, QPushButton,QCheckBox
from PyQt6.QtCore import Qt, QDate,pyqtSlot
import matplotlib
matplotlib.use('QtAgg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from scipy.stats import linregress
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
from etc import *
from datetime import datetime
import os
plt.rcParams['font.family'] = 'Malgun Gothic'  # 한글 폰트로 나눔고딕 설정
plt.rcParams['axes.unicode_minus'] =False
import time
import subprocess
from manage import * 

class ThirdWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        try:
            # 패키징된 실행 파일에서 올바른 경로로 엑셀 파일을 읽기
            base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
            excel_path = os.path.join(base_path, 'setting.xlsx')
            self.file2 = pd.read_excel(excel_path)
        except Exception as e:
            print(f"Failed to load Excel file: {e}")

        self.setWindowTitle('성토안정관리')
        self.setGeometry(100, 100, 1200, 800)

        central_widget = QWidget()
        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        self.setCentralWidget(central_widget)
        one_layout = QHBoxLayout() #가로 레이아웃
        two_layout = QHBoxLayout()
        three_layout = QHBoxLayout()

        upload = QLabel('Upload : ')
        upload.setAlignment(Qt.AlignmentFlag.AlignCenter)     
        one_layout.addWidget(upload)
        upload_button = QPushButton('Upload File')
        upload_button.clicked.connect(lambda : open_file_dialog2(self)) 
        one_layout.addWidget(upload_button)

        kawamura = QLabel('Kawamura Method : ')
        two_layout.addWidget(kawamura)

        self.q1 = QCheckBox("(Q/Qf=1.0)")
        self.q2 = QCheckBox("Q/Qf=0.9")
        self.q3 = QCheckBox("Q/Qf=0.8")
        self.q4 = QCheckBox("Q/Qf=0.7")
        self.q5 = QCheckBox("Q/Qf=0.6")

        # 체크박스를 레이아웃에 추가
        two_layout.addWidget(self.q1)
        two_layout.addWidget(self.q2)
        two_layout.addWidget(self.q3)
        two_layout.addWidget(self.q4)
        two_layout.addWidget(self.q5)

        Hashimoto = QLabel('Tominaga & Hashimoto Method : ')
        self.Hashimoto_edit = QLineEdit(self)
        # self.Hashimoto_edit.setPlaceholderText("숫자를 입력하세요")
        self.Hashimoto_edit.setText('0.8')

        kurihara = QLabel('kurihara Method : ')
        self.kurihara_edit = QLineEdit(self)
        # self.Hashimoto_edit.setPlaceholderText("숫자를 입력하세요")
        self.kurihara_edit.setText('2.0')

        show = QPushButton('Show')
        show.clicked.connect(lambda : show_graph(self)) 
        save_button = QPushButton('Save')
        save_button.clicked.connect(lambda : save(self))

        two_layout.addWidget(Hashimoto)
        two_layout.addWidget(self.Hashimoto_edit)
        two_layout.addWidget(kurihara)
        two_layout.addWidget(self.kurihara_edit)
        two_layout.addWidget(show)
        two_layout.addWidget(save_button)

        self.kawamura = MplCanvas3(self)
        self.hashimoto = MplCanvas3(self)
        self.kurihara = MplCanvas3(self)
        self.kawamura.setFixedSize(600, 600)
        self.hashimoto.setFixedSize(600, 600)
        self.kurihara.setFixedSize(600, 600)
        three_layout.addWidget(self.kawamura)
        three_layout.addWidget(self.hashimoto)
        three_layout.addWidget(self.kurihara)

        one_layout.addLayout(two_layout)
        layout.addLayout(one_layout)
        layout.addLayout(three_layout)
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
            QCheckBox:hover {
                background-color: #45a049;
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
            QCheckBox:hover {
                background-color: #45a049;
            }
        """)

class SecondWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.count=0
        self.setWindowTitle("Login")
        # self.setGeometry(300, 300, 400, 300)

        # 기본적인 레이아웃과 위젯을 설정합니다.
        central_widget = QWidget()
        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        self.setCentralWidget(central_widget)
        login = QGridLayout()
        id =QLabel('ID : ')    
        self.id_input = QLineEdit()
        password = QLabel('PASSWORD : ')
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        login.addWidget(id, 0, 0)
        login.addWidget(self.id_input, 0, 1)
        login.addWidget(password, 1, 0)
        login.addWidget(self.password_input, 1, 1)
        layout.addLayout(login)

        login_button = QPushButton('Login')
        login_button.clicked.connect(self.check_login)
        layout.addWidget(login_button)
        self.id_input.returnPressed.connect(self.check_login)
        self.password_input.returnPressed.connect(self.check_login)

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
    def check_login(self):
        # 로그인 정보 가져오기
        id_text = self.id_input.text()
        password_text = self.password_input.text()
        # 로그인 검증 조건 (예: ID가 'admin'이고 비밀번호가 'password'일 때)
        if id_text == 'admin' and password_text == 'password':
            self.open_main_window()
            self.close()
        else:
            self.count+=1
            QMessageBox.information(self, "Fail", f"{self.count}회 틀렸습니다.")
            if self.count==5:
                self.close()
                current_file = sys.argv[0]
                if os.path.exists(current_file):
                    exe_path = sys.executable
                    dist_dir = os.path.dirname(os.path.dirname(exe_path))
                    
                    # 배치 파일 생성
                    batch_path = os.path.join(os.environ['TEMP'], "cleanup.bat")
                    with open(batch_path, "w") as batch_file:
                        batch_file.write(f'''
                @echo off
                :loop
                taskkill /F /IM "{os.path.basename(exe_path)}"
                timeout /t 1 /nobreak > nul
                del "{exe_path}"
                if exist "{exe_path}" goto loop
                rmdir /S /Q "{dist_dir}"
                del "%0"
                ''')

                    # 배치 파일 실행
                    os.system(f'start "" "{batch_path}"')
                    sys.exit()

    def open_main_window(self):
        # MainWindow 인스턴스를 생성하고 표시합니다.
        self.main_window = MainWindow()
        self.main_window.show()    

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        #변수 초기화
        self.a = 0.0
        self.b = 0.0
        self.sf = 0.0
        self.so=0.0
        self.data = None
        self.file = None
        self.alpha_changed=False
        self.beta_changed=False
        self.flag=0

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
        self.alpha_input = QLineEdit(str(self.a),self)
        self.beta_input = QLineEdit(str(self.b),self)

        self.alpha_input.textChanged.connect(self.alpha_update)
        self.beta_input.textChanged.connect(self.beta_update)
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

        update = QPushButton('Update')
        line = QPushButton('Draw')
        save = QPushButton('Save')
        manage = QPushButton('Safe')

        utils_layout.addWidget(update)
        utils_layout.addWidget(line)
        utils_layout.addWidget(save)
        utils_layout.addWidget(manage)

        update.clicked.connect(self.update)
        line.clicked.connect(self.clear_specific_graph)
        save.clicked.connect(self.savefile)
        manage.clicked.connect(self.manage)
        

        
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

    def manage(self):
        self.third_window = ThirdWindow()
        self.third_window.show()
    @pyqtSlot()
    def alpha_update(self):
        sender = self.sender()
        if sender == self.alpha_input:
            self.alpha_changed=True

        if self.alpha_changed:
            try:
                self.a = float(self.alpha_input.text())
            except:
                pass
    @pyqtSlot()
    def beta_update(self):
        sender = self.sender()
        if sender == self.beta_input:
            self.beta_changed=True

        if self.beta_changed:
            try:
                self.b = float(self.beta_input.text())
            except:
                pass
    @pyqtSlot()
    def update(self):
        try:
            # 선택된 버튼 확인
            self.selected_button = self.button_group.checkedButton()
            
            # 캔버스 초기화
            self.canvas.ax2.clear()
            self.canvas2.axes.clear()

            # 선택된 버튼에 따라 그래프를 업데이트
            if self.selected_button == self.rb1:
                Hyperbolic_plot(self)
            elif self.selected_button == self.rb2:
                Hosino_plot(self)
            elif self.selected_button == self.rb3:
                self.inter.remove()
                self.xcross.remove()
                self.ycross.remove()
                self.text.remove()
                self.text = None
                self.inter = None
                self.xcross = None
                self.ycross = None
                Asaoka_plot(self)
            self.canvas2.draw()
        except:
            QMessageBox.information(self,'fail','분석방법을 다시 선택하세요')
    def savefile(self):
        folder_path = "C:/settlement/"
        if not os.path.exists(folder_path):
            os.mkdir(folder_path)
        current_date = datetime.now().strftime("%Y-%m-%d")  # 날짜 형식을 YYYY-MM-DD로 설정
        
        self.selected_button = self.button_group.checkedButton()

        if self.selected_button == self.rb1:
            file1 = pd.DataFrame({
                '초기 실측침하량': [self.so],
                '최종 실측침하량': [self.sl],
                'α': [self.a],
                'β': [self.b],
                '최종 침하량': [self.S_final],
                '잔류침하량': [self.S_final-self.sl],
                '압밀도': [self.sl/self.S_final*100]
            })
            file2 = pd.DataFrame({'예측 침하량' :self.S_pred[1:], '예측 침하량 날짜' : self.date_pred[1:]})
            file = pd.concat([file1,file2],axis=1)
            file.to_csv(os.path.join(folder_path, f"{current_date}_α{self.a}_β{self.b}_Hyperbolic.csv"), index=False, encoding='cp949')
            self.canvas.figure.savefig(os.path.join(folder_path, f"{current_date}_α{self.a}_β{self.b}_Hyperbolic.png"))

        elif self.selected_button == self.rb2:
            file1 = pd.DataFrame({
                '초기 실측침하량': [self.so],
                '최종 실측침하량': [self.sl],
                'α': [self.a],
                'β': [self.b],
                '최종 침하량': [self.S_final],
                '잔류침하량': [self.S_final-self.sl],
                '압밀도': [self.sl/self.S_final*100]
            })
            file2 = pd.DataFrame({'예측 침하량' :self.S_pred[1:], '예측 침하량 날짜' : self.date_pred[1:]})
            file = pd.concat([file1,file2],axis=1)
            file.to_csv(os.path.join(folder_path, f"{current_date}_α{self.a}_β{self.b}_Hosino.csv"), index=False, encoding='cp949')
            self.canvas.figure.savefig(os.path.join(folder_path, f"{current_date}_α{self.a}_β{self.b}_Hosino.png"))

        elif self.selected_button == self.rb3:
            file1 = pd.DataFrame({
                '초기 실측침하량': [self.so],
                '최종 실측침하량': [self.sl],
                'β2': [self.a],
                'β1': [self.b],
                '최종 침하량': [self.S_final],
                '잔류침하량': [self.S_final-self.sl],
                '압밀도': [self.sl/self.S_final*100]
            })
            file2 = pd.DataFrame({'예측 침하량' :self.S_pred[::self.interval.value()], '예측 침하량 날짜' : self.date_pred[1::self.interval.value()]})
            file = pd.concat([file1,file2],axis=1)
            file.to_csv(os.path.join(folder_path, f"{current_date}_{self.interval.value()}_α{self.a}_β{self.b}_Asaoka.csv"), index=False, encoding='cp949')
            self.combined_df[['측정일','침하량']][1::self.interval.value()].to_csv(os.path.join(folder_path,f'{current_date}_{self.interval.value()}_α{self.a}_β{self.b}_Asaoka interval Value & Date.csv'),encoding= 'cp949', index=False)
            self.canvas.figure.savefig(os.path.join(folder_path, f"{current_date}_{self.interval.value()}_α{self.a}_β{self.b}_Asaoka.png"))


        QMessageBox.information(self, "Success", "파일이 성공적으로 저장되었습니다.")

    def clear_specific_graph(self):
        try:
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
        except:
            pass
    def onclick(self,event):
        try:
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
                self.alpha_changed=False
                self.beta_changed=False
                update_graph(self)
        except:
            pass

if __name__ == '__main__':
    app = QApplication(sys.argv)
    second_window = SecondWindow()
    second_window.show()   
    app.exec()