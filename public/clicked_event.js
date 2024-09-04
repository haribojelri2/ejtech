function asaoka_clicked_event(event) {
    const rect = ctxSub.canvas.getBoundingClientRect();
    const x = event.clientX - rect.left;
    const y = event.clientY - rect.top;
    var remove = parseFloat($('#remove').val());

    // 클릭된 좌표를 데이터로 변환
    const xScale = ctxSub.scales.x.getValueForPixel(x);
    const yScale = ctxSub.scales.y.getValueForPixel(y);

    points.push({ x: xScale, y: yScale });
    if (points.length == 2) {
        ctxSub.data.datasets.find(dataset => dataset.label === 'Regression Line').data = points;
        let slope = calculateSlope(points[0].x, points[0].y, points[1].x, points[1].y);
        let intercept = calculateIntercept(points[0].x, points[0].y, slope);
        let x_cross = intercept / (1-slope);
        let y_cross = x_cross
        let x_min = Math.min(...data.s1.map(val => val * -1));
        let x_max = Math.max(Math.max(...data.s1.map(val => val * -1)), x_cross);
        const sf = intercept/(1-slope)*-1;
        ctxSub.data.datasets[2].data = [{x:x_cross,y:y_cross}];
        ctxSub.data.datasets[3].data=[{x: x_min, y: y_cross}, {x: x_cross, y: y_cross}];
        ctxSub.data.datasets[4].data=[{x: x_cross, y:x_min}, {x: x_cross, y: y_cross}];
        ctxSub.update();

        document.getElementById('alpha').value = intercept;         
        document.getElementById('beta').value = slope;          
        document.getElementById('sf').textContent = Math.round(sf*100)/100;
        document.getElementById('Compaction Density').textContent = Math.round((data.sl/sf * 100)*100)/100;
        document.getElementById('residual').textContent =Math.round((sf - data.sl)*100)/100;
        const index = data.ori_y2.findIndex(num=> num<sf+remove);
        const date = new Date(data.ori_x[index]);
        const formattedDate = date.toLocaleDateString('ko-KR', {
            year: 'numeric',
            month: '2-digit',
            day: '2-digit'
          });
        document.getElementById('removal data').textContent =formattedDate; 
        let s_pred = data.t_pred.slice(1).map(t=>sf - (sf - data.s1[0])* Math.exp(t*Math.log(slope)/data.timeInterval))
        const indicesToKeep = new Set(Array.from({ length: s_pred.length }, (_, i) => i).filter(i => i % data.timeInterval === 0));
        s_pred = s_pred.map((value, i) => indicesToKeep.has(i) ? value : null);
        let none = new Array(data.ori_x.length - s_pred.length).fill(null);
        values = none.concat(s_pred);


        ctxMain.data.datasets.find(dataset => dataset.label === 'Predicted').data =  dates.map((dateStr, index) => ({
            x: new Date(dateStr),
            y: values[index]}));
        ctxMain.update();
        points = [];
    }
};

function hosino_clicked_event(event) {
    const rect = ctxSub.canvas.getBoundingClientRect();
    const x = event.clientX - rect.left;
    const y = event.clientY - rect.top;
    var remove = parseFloat($('#remove').val());

    // 클릭된 좌표를 데이터로 변환
    const xScale = ctxSub.scales.x.getValueForPixel(x);
    const yScale = ctxSub.scales.y.getValueForPixel(y);

    points.push({ x: xScale, y: yScale });

    // Predicted 데이터 업데이트

    if (points.length == 2) {

        ctxSub.data.datasets.find(dataset => dataset.label === 'Regression Line').data = points;
        ctxSub.update();

        let slope = calculateSlope(points[0].x, points[0].y, points[1].x, points[1].y);
        let intercept = calculateIntercept(points[0].x, points[0].y, slope);
        let sf = (Math.sqrt(1/slope) - data.so);
        document.getElementById('alpha').value =  intercept;            
        document.getElementById('beta').value =  slope;   
        document.getElementById('sf').textContent =  Math.round(-sf*100)/100   
        document.getElementById('Compaction Density').textContent = Math.round((data.sl/-sf * 100)*100)/100;
        document.getElementById('residual').textContent =Math.round((-sf - data.sl)*100)/100;
        const index = data.ori_y2.findIndex(num=> num<-sf+remove);
        console.log(remove)
        const date = new Date(data.ori_x[index]);
        const formattedDate = date.toLocaleDateString('ko-KR', {
            year: 'numeric',
            month: '2-digit',
            day: '2-digit'
          });
        document.getElementById('removal data').textContent =formattedDate; 
        let s_pred = data.t_pred.map(t => data.so - Math.sqrt(t / (intercept + slope * t))); 
        let none = new Array(data.ori_x.length - s_pred.length).fill(null);
        values = none.concat(s_pred);

        ctxMain.data.datasets.find(dataset => dataset.label === 'Predicted').data =  dates.map((dateStr, index) => ({
            x: new Date(dateStr),
            y: values[index]}));


        // 업데이트 호출하여 그래프 변경사항 반영
        ctxMain.update();

        points = [];
    }
};

function hyperbolic_clicked_event(event) {
    const rect = ctxSub.canvas.getBoundingClientRect();
    const x = event.clientX - rect.left;
    const y = event.clientY - rect.top;
    var remove = parseFloat($('#remove').val());
    // 클릭된 좌표를 데이터로 변환
    const xScale = ctxSub.scales.x.getValueForPixel(x);
    const yScale = ctxSub.scales.y.getValueForPixel(y);

    points.push({ x: xScale, y: yScale });

    if (points.length == 2) {

        ctxSub.data.datasets.find(dataset => dataset.label === 'Regression Line').data = points;
        ctxSub.update();

        let slope = calculateSlope(points[0].x, points[0].y, points[1].x, points[1].y);
        let intercept = calculateIntercept(points[0].x, points[0].y, slope);
        let sf =1/slope - data.so;
        document.getElementById('alpha').value =  intercept;            
        document.getElementById('beta').value =  slope;         // t_pred의 각 값에 대해 예측값을 계산
        document.getElementById('sf').textContent =  Math.round(-sf*100)/100            // t_pred의 각 값에 대해 예측값을 계산
        document.getElementById('Compaction Density').textContent = Math.round((data.sl/-sf * 100)*100)/100;
        document.getElementById('residual').textContent = Math.round((-sf - data.sl)*100)/100;
        let s_pred = data.t_pred.map(t => data.so - t / (intercept + slope * t)); 
        let none = new Array(data.ori_x.length - s_pred.length).fill(null);
        values = none.concat(s_pred);

        const index = data.ori_y2.findIndex(num=> num<-sf+remove);
        const date = new Date(data.ori_x[index]);
        const formattedDate = date.toLocaleDateString('ko-KR', {
            year: 'numeric',
            month: '2-digit',
            day: '2-digit'
          });
        document.getElementById('removal data').textContent =formattedDate;
        ctxMain.data.datasets.find(dataset => dataset.label === 'Predicted').data =  dates.map((dateStr, index) => ({
            x: new Date(dateStr),
            y: values[index]}));
        

        // 업데이트 호출하여 그래프 변경사항 반영
        ctxMain.update();

        points = [];
    }
};