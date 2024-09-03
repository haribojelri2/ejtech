let ctxBasic;
let ctxMain;
let ctxSub;
let points = [];
let dates;
let values;
document.querySelectorAll('input[type="radio"]').forEach(function (radio) {
    radio.addEventListener('click', function () {
        const timeInput = document.getElementById('timeInput');
        
        if (this.id === 'asaoka') {
            timeInput.style.display = 'block';
            document.getElementById('timeInterval').value = 1;
            document.getElementById('remove').value = 10;
            document.getElementById('alpha_label').textContent = 'β0 : ';
            document.getElementById('beta_label').textContent = 'β1 : ';
        } else {
            timeInput.style.display = 'none';
            document.getElementById('remove').value = 10;
            document.getElementById('alpha_label').textContent = 'α : ';
            document.getElementById('beta_label').textContent = 'β : ';
        }
    });
    });
document.addEventListener("DOMContentLoaded", function () {    
    async function fetchData() {
        const response = await fetch('/upload', {
            method: 'POST',
            body: new FormData(document.getElementById('uploadForm')) // 폼 데이터를 전송
        });
        data = await response.json();
        if (!response.ok) {
            alert(`Error: ${data.error}`);
        }
        if (ctxBasic) ctxBasic.destroy();
        if (ctxMain) ctxMain.destroy();
        if (ctxSub) ctxSub.destroy();
        const alphaValue = data.a; // 기본값 0 할당
        const betaValue = data.b; // 기본값 0 할당
        const soValue = data.so;
        const sfValue = data.sf; 
        const timeIntervalValue = data.timeInterval
        document.getElementById('alpha').value = alphaValue;
        document.getElementById('beta').value = betaValue;
        document.getElementById('st').textContent = soValue;
        document.getElementById('sf').textContent = Math.round(-sfValue*100)/100;
        document.getElementById('timeInterval').value = timeIntervalValue;
        document.getElementById('Compaction Density').textContent = Math.round((data.sl/-sfValue * 100)*100)/100;
        document.getElementById('residual').textContent = Math.round((-sfValue-data.sl)*100)/100;
        var remove = parseFloat($('#remove').val());

        if (data.plottype ==='hyperbolic'){
            hyperbolic(data)
            const index = data.ori_y2.findIndex(num=> num<-sfValue+remove);
            const date = new Date(data.ori_x[index]);
            const formattedDate = date.toLocaleDateString('ko-KR', {
                year: 'numeric',
                month: '2-digit',
                day: '2-digit'
              });
            document.getElementById('removal data').textContent =formattedDate; 

        }else if (data.plottype ==='hosino'){
            hosino(data)
            const index = data.ori_y2.findIndex(num=> num<-sfValue+remove);
            const date = new Date(data.ori_x[index]);
            const formattedDate = date.toLocaleDateString('ko-KR', {
                year: 'numeric',
                month: '2-digit',
                day: '2-digit'
              });
            document.getElementById('removal data').textContent =formattedDate; 

        }else if (data.plottype ==='asaoka'){
            asaoka(data)
            document.getElementById('sf').textContent = Math.round(sfValue*100)/100;
            document.getElementById('Compaction Density').textContent = Math.round((data.sl/sfValue * 100)*100)/100;
            document.getElementById('residual').textContent = Math.round((sfValue-data.sl)*100)/100;
            const index = data.ori_y2.findIndex(num=> num<sfValue+remove);
            const date = new Date(data.ori_x[index]);
            const formattedDate = date.toLocaleDateString('ko-KR', {
                year: 'numeric',
                month: '2-digit',
                day: '2-digit'
              });
            document.getElementById('removal data').textContent =formattedDate; 
        }
    }
    document.getElementById('save').addEventListener('click', function() {
        // 메인 데이터 처리
        const saveData = dates.map((date, i) => {
            const parsedDate = new Date(date); // 각 항목을 Date 객체로 변환
            return {
                date: parsedDate.toLocaleDateString('ko-KR', {
                    year: 'numeric',
                    month: '2-digit',
                    day: '2-digit'
                }),
                value: values[i]
            };
        }).filter(item => item.value !== null && item.value !== undefined);
        
        const mainWorksheet = XLSX.utils.json_to_sheet(saveData);
        const mainWorkbook = XLSX.utils.book_new();
        XLSX.utils.book_append_sheet(mainWorkbook, mainWorksheet, 'saveData');
    
        // 현재 시간을 문자열로 변환하여 파일 이름에 포함
        const now = new Date();
        const formattedDate = now.toISOString().replace(/T/, '').replace(/:/g, '').split('.')[0]; // 예: 2024-09-02_14-30-45
        const mainFilename = `${data.plottype}-${formattedDate}.xlsx`; // 파일 이름 생성
        XLSX.writeFile(mainWorkbook, mainFilename); // 파일 저장
        
        if (data.plottype === 'asaoka') {
            // 서브 데이터 처리
            const subData = data.real_dates.map((date, i) => {
                const parsedDate = new Date(date); 
                return {
                    date: parsedDate.toLocaleDateString('ko-KR', {
                        year: 'numeric',
                        month: '2-digit',
                        day: '2-digit'
                    }),
                    value: data.real_values[i]
                };
            });
            
            const subWorksheet = XLSX.utils.json_to_sheet(subData);
            const subWorkbook = XLSX.utils.book_new();
            XLSX.utils.book_append_sheet(subWorkbook, subWorksheet, 'subData');
        
            const subFilename = `${data.plottype}-sub-${formattedDate}.xlsx`; // 파일 이름 생성
            XLSX.writeFile(subWorkbook, subFilename); // 파일 저장
        }
    
        console.log('Successfully Saved File');
    });
    
    document.querySelector('button[type="submit"]').addEventListener('click', function (event) {
        event.preventDefault(); // 폼 전송 방지
        fetchData();
    });
});

$(document).ready(function () {
    $('#update').click(function () {
        if (!data) {
            console.error('Data is not loaded yet.');
            return;
        }

        // 입력값 가져오기
        var alpha = $('#alpha').val();
        var beta = $('#beta').val();

        // 서버로 데이터 전송
        $.ajax({
            url: '/update',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({
                alpha: alpha,
                beta: beta,
            }),
            success: function (response) {
                const {alpha, beta } = response;
                alpha_beta_update(alpha, beta);
            },
            error: function (xhr, status, error) {
                console.error('Error:', error);
            }
        });
    });
});
