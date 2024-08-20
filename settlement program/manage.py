from PyQt6.QtWidgets import  QFileDialog,QLabel,QSpinBox,QMessageBox
from PyQt6.QtCore import Qt, QDate
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


# pd.set_option('future.no_silent_downcasting', True)

class MplCanvas3(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas3, self).__init__(fig)

def show_graph(self):
    import matplotlib.pyplot as plt
    import numpy as np
    import pandas as pd
    # try:
    if self.Hashimoto_edit.text()=='':
        QMessageBox.information(self, "faile", "숫자를 입력하세요.")
    self.kawamura.axes.clear()
    self.hashimoto.axes.clear()
    self.kurihara.axes.clear()
    self.file['측정일']=pd.to_datetime(self.file['측정일'])
    day = self.file['측정일'].diff().dt.days
    self.file['Sh1_누적(m)'] = self.file['경사계(mm)']/1000
    self.file['ΔSh1/Δt_속도(m)'] = np.abs(self.file['Sh1_누적(m)'].diff()/day)
    self.file['ΔSh1/Δt_속도(cm)'] = np.abs(self.file['Sh1_누적(m)'].diff()/day)*100
    self.file=self.file.infer_objects(copy=False).fillna(0)

    self.file['ΔSh1/Δt_속도(m)']=np.round(self.file['ΔSh1/Δt_속도(m)'],5)
    self.file['ΔSh1/Δt_속도(cm)']=np.round(self.file['ΔSh1/Δt_속도(cm)'],3)
    self.file['Sv_누적(m)']=self.file['침하판(cm)']/100
    self.file['ΔSv/Δt_속도(m)'] = np.abs(self.file['Sv_누적(m)'].diff()/day)
    self.file['ΔSv/Δt_속도(cm)'] = np.abs(self.file['Sv_누적(m)'].diff()/day)*100
    self.file=self.file.infer_objects(copy=False).fillna(0)
    self.file['ΔSv/Δt_속도(m)']=np.round(self.file['ΔSv/Δt_속도(m)'],3)
    self.file['ΔSv/Δt_속도(cm)']=np.round(self.file['ΔSv/Δt_속도(cm)'],2)
    self.file['Sh1/Sv'] = np.where(self.file['Sv_누적(m)'] > 0, 
                          np.round(self.file['Sh1_누적(m)'] / self.file['Sv_누적(m)'], 2), 
                          0)
    self.file['Sh1/Sv'] = self.file['Sh1/Sv'].replace([np.inf, -np.inf], 0)

    self.kawamura.axes.plot(self.file['Sh1/Sv'],self.file['Sv_누적(m)'],label='Sh1/Sv')
    if self.q1.isChecked():
        self.kawamura.axes.plot(self.file2['dh/DSv'],self.file2['(Q/Qf)=1.0'], label='(Q/Qf)=1.0')
        # self.kawamura.axes.annotate(
        #     '주의',
        #     (self.)
        # )
    if self.q2.isChecked():
        self.kawamura.axes.plot(self.file2['dh/DSv.1'],self.file2['(Q/Qf)=0.9'], label='(Q/Qf)=0.9')
    if self.q3.isChecked():
        self.kawamura.axes.plot(self.file2['dh/DSv.2'],self.file2['(Q/Qf)=0.8'], label='(Q/Qf)=0.8')
    if self.q4.isChecked():
        self.kawamura.axes.plot(self.file2['dh/DSv.3'],self.file2['(Q/Qf)=0.7'], label='(Q/Qf)=0.7')
    if self.q5.isChecked():
        self.kawamura.axes.plot(self.file2['dh/DSv.4'],self.file2['(Q/Qf)=0.6'], label='(Q/Qf)=0.6')

    self.kawamura.axes.legend()
    self.kawamura.axes.set_ylim(0,3)
    self.kawamura.axes.set_xlim(0,1.2)
    self.kawamura.axes.grid(True)
    self.kawamura.axes.set_xlabel('Sh1/Sv')
    self.kawamura.axes.set_ylabel('Sv(m)')
    self.kawamura.axes.set_title('Mutsuo & Kawamura Method')
    self.kawamura.draw()

    self.hashimoto.axes.plot(self.file['Sh1_누적(m)'],self.file['Sv_누적(m)'],label='Sh1/Sv')
    self.hashimoto.axes.plot(self.file2['기준선:1'],self.file2['기준선:1'],label='기준선:1')
    self.hashimoto.axes.plot(self.file2['기준선:1']*float(self.Hashimoto_edit.text()),self.file2['기준선:1'],label='기준선:'+self.Hashimoto_edit.text())
    self.hashimoto.axes.annotate(
            '기준선:1',
            (self.file2['기준선:1'][np.round(len(self.file2['기준선:1'])/2)], self.file2['기준선:1'][np.round(len(self.file2['기준선:1'])/2)]),
            xytext=(10, 10),
            textcoords='offset points',
            bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.3')
            # arrowprops=dict(facecolor='black', shrink=0.05)
        )
    self.hashimoto.axes.annotate(
            '기준선:2',
            (self.file2['기준선:1'][np.round(len(self.file2['기준선:1'])/2)]*0.5*float(self.Hashimoto_edit.text()), self.file2['기준선:1'][np.round(len(self.file2['기준선:1'])/2)]*1.4),
            xytext=(10, 10),
            textcoords='offset points',
            bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.3')
            # arrowprops=dict(facecolor='black', shrink=0.05)
        )
    self.hashimoto.axes.set_xlim(0,2.5)
    self.hashimoto.axes.set_ylim(0,2.5)
    self.hashimoto.axes.invert_yaxis()
    self.hashimoto.axes.legend()
    self.hashimoto.axes.grid(True)
    self.hashimoto.axes.set_xlabel('수평변위(Sh)')
    self.hashimoto.axes.set_ylabel('침하(Sv)')
    self.hashimoto.axes.set_title('Tominaga & Hashimoto Method')
    self.hashimoto.draw()

    self.kurihara.axes.plot(self.file['측정일'],self.file['ΔSh1/Δt_속도(cm)'],label='ΔSh1/Δt')
    a = [float(self.kurihara_edit.text()) for i in range(len(self.file['ΔSh1/Δt_속도(cm)']))]
    self.kurihara.axes.plot(self.file['측정일'],a,label='ΔSh1/Δt 기준선')
    self.kurihara.axes.legend()
    self.kurihara.axes.grid(True)
    self.kurihara.axes.set_ylim(-0.5,3)
    self.kurihara.axes.set_xlabel('일자(day)')
    self.kurihara.axes.set_ylabel('변위속도(cm)/계측일자(day)')
    self.kurihara.axes.set_title('Kurihara Method')
    self.kurihara.draw()
    print(self.file)
    # except:
    #     pass

def save(self):
    import os
    from datetime import datetime

    folder_path = "C:/settlement/"
    if not os.path.exists(folder_path):
        os.mkdir(folder_path)
    current_date = datetime.now().strftime("%Y-%m-%d")
    self.file.to_csv(os.path.join(folder_path, f"{current_date}_성토안정관리.csv"), index=False, encoding='cp949')
    QMessageBox.information(self, "Success", "파일이 성공적으로 저장되었습니다.")
