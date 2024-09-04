
function asaoka(data) {
    hosino_check = false;
    hyperbolic_check = false;  
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
                label: 'y=x',
                type: 'line',
                data: [{x: data.x_min, y: data.x_min}, {x: data.x_max, y: data.x_max}],
                borderColor: 'rgba(153, 102, 255, 1)',
                borderWidth: 1,
                fill: false
            }, {
                label: 'Regression Line',
                type: 'line',
                data: data.x_range.map(x => ({x, y: data.a + data.b * x})),
                borderColor: 'rgba(255, 159, 64, 1)',
                borderWidth: 1,
                fill: false
            }, {
                label: 'Intersection',
                data: [{x: data.x_cross, y: data.y_cross}],
                backgroundColor: 'red',
                pointRadius: 8
            }, {
                label: '',
                data: [
                    {x: data.x_min, y: data.y_cross}, 
                    {x: data.x_cross, y: data.y_cross}
                ],
                type: 'line',
                borderColor: 'rgba(255, 159, 64, 1)',
                borderWidth: 2,
                borderDash: [5, 5],
                fill: false
            }, {
                label: '',
                data: [
                    {x: data.x_cross, y: data.x_min}, 
                    {x: data.x_cross, y: data.y_cross}
                ],
                type: 'line',
                borderColor: 'rgba(255, 159, 64, 1)',
                borderWidth: 2,
                borderDash: [5, 5],
                fill: false
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    display: true,
                    labels: {
                        generateLabels: function(chart) {
                            const original = Chart.defaults.plugins.legend.labels.generateLabels(chart);
                            return original.filter(label => label.text.trim() !== ""); // 빈 레이블 제거
                        }
                    }
                },
                title: {
                    display: true,
                    text: 'Asaoka Method',
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
                        text: 'S(n)' // x축 제목
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
                        text: 'S(n+1)' // y축 제목
                    },
                    ticks: {
                        autoSkip: true
                    }
                }
            }
        }
    });
    
    // 캔버스 클릭 이벤트 리스너 추가

    document.getElementById('sub_plot').removeEventListener('click', hosino_clicked_event);
    document.getElementById('sub_plot').removeEventListener('click', hyperbolic_clicked_event);
    document.getElementById('sub_plot').addEventListener('click', asaoka_clicked_event);
}