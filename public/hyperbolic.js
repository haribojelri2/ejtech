
function hyperbolic(data) {        
    asaoka_check = false;
    hosino_check = false;
    dates=data.ori_x;
    values=data.ori_y;
    ctxBasic = new Chart(document.getElementById('basic_plot').getContext('2d'), {
        type: 'line',
        data: {
            labels: dates.map(dateStr => new Date(dateStr)),
            datasets: [{
                label: 'Fill Height(m)',
                data: data.basic_y,
                borderColor: 'rgba(75, 192, 192, 1)',
                borderWidth: 2,
                fill: false
            }]
        },
        options: {
            scales: {
                x: {
                    display: false,
                    type: 'time',
                    time: {
                        unit: 'day',
                        displayFormats: { day: 'yyyy-MM-dd' }
                    },
                    title: {
                        display: false                            
                    }
                },
                y: {
                    title: {
                        display: true,
                        text: 'Fill Height(m)'
                    }   
                }
            }
        }
    });

    // Main Plot
    ctxMain = new Chart(document.getElementById('main_plot').getContext('2d'), {
        type: 'line',
        data: {
            labels: dates.map(dateStr => new Date(dateStr)),
            datasets: [{
                label: 'Predicted',
                data: values,
                borderColor: 'rgba(75, 192, 192, 1)',
                borderWidth: 2,
                fill: false
            }, {
                label: 'Measured',
                data: data.ori_y2,
                borderColor: 'rgba(255, 99, 132, 1)',
                borderWidth: 2,
                fill: false
            }]
        },
        options: {
            plugins: {
                title: {
                    display: true, // 제목 표시 여부
                    text: 'Settlement Curve', // 제목 텍스트
                    font: {
                        size: 20, // 제목 폰트 크기
                        weight: 'bold' // 제목 폰트 두께
                    },
                    color: '#333', // 제목 색상
                    padding: {
                        top: 10, // 제목과 차트 사이의 여백 (위쪽)
                        bottom: 10 // 제목과 차트 사이의 여백 (아래쪽)
                    },
                }
            },
            scales: {
                x: {
                    type: 'time',
                    time: {
                        unit: 'day',
                        displayFormats: { day: 'yyyy-MM-dd' }
                    },
                    title: {
                        display: false,
                        text: '측정일'
                    }
                },
                y: {
                    title: {
                        display: true,
                        text: 'Settlement (cm)'
                    }
                }
            }
        }
    });

    // Sub Plot
    ctxSub = new Chart(document.getElementById('sub_plot').getContext('2d'), {
        type: 'scatter',
        data: {
            datasets: [{
                label: 'Measured',
                type: 'scatter',
                data: data.reg_y.map((y, i) => ({ x: data.reg_x[i], y })),
                borderColor: 'rgba(153, 102, 255, 1)',
                borderWidth: 2,
                fill: false
            }, {
                label: 'Regression Line',
                type: 'line',
                data: data.reg_y2.map((y, i) => ({ x: data.reg_x[i], y })),
                borderColor: 'rgba(255, 159, 64, 1)',
                borderWidth: 2,
                fill: false
            }]
        },
        options: {
            plugins: {
                legend: {
                    display: true, // 범례 표시
                    labels: {
                        generateLabels: function(chart) {
                            // 기본 레이블 생성 함수 사용
                            const original = Chart.defaults.plugins.legend.labels.generateLabels(chart);
                            return original.filter(label => label.text.trim() !== ""); // 빈 레이블 제거
                        }
                    }
                },
                title: {
                    display: true,
                    text: 'Hyperbolic Method',
                    font: {
                        size: 20,
                        weight: 'bold'
                    },
                    color: '#333',
                    padding: {
                        top: 10,
                        bottom: 10
                    }
                }
            },
            scales: {
                x: {
                    type: 'linear', // x축의 타입
                    position: 'bottom', // x축의 위치
                    title: {
                        display: true,
                        text: '(t-to)day'
                    },
                    ticks: {
                        // x축의 ticks 설정
                        autoSkip: true,
                        maxRotation: 0,
                        minRotation: 0
                    }
                },
                y: {
                    type: 'linear', // y축의 타입
                    title: {
                        display: true,
                        text: '(t-to)/(St-So)'
                    },
                    ticks: {
                        autoSkip: true
                    }
                }
            }
        }
    });


    // 캔버스 클릭 이벤트 리스너 추가
    document.getElementById('sub_plot').removeEventListener('click', asaoka_clicked_event);
    document.getElementById('sub_plot').removeEventListener('click', hosino_clicked_event);
    document.getElementById('sub_plot').addEventListener('click', hyperbolic_clicked_event);
}