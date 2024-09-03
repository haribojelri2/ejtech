function alpha_beta_update(alpha, beta) {
    var alpha = parseFloat(alpha); // alpha_pred의 각 값에 대해 예�
    var beta =parseFloat(beta);
    var s_pred;
    var none;
    var indicesToKeep;
    var remove = parseFloat($('#remove').val());

    document.getElementById('alpha').value = alpha;            // t_pred의 각 값에 대해 예측값을 계산
    document.getElementById('beta').value = beta; 

    if (data.plottype === 'hyperbolic') {
        ctxSub.data.datasets.find(dataset => dataset.label === 'Regression Line').data = data.reg_x.map((x, index) => ({
            x: x,
            y: alpha + beta * x
        }));
        let sf = 1/beta - data.so; 
        document.getElementById('sf').textContent =Math.round(-sf*100)/100;    
        document.getElementById('Compaction Density').textContent = Math.round((data.sl/-sf * 100)*100)/100;
        document.getElementById('residual').textContent = Math.round((-sf - data.sl)*100)/100;   
        const index = data.ori_y2.findIndex(num=> num<-sf+remove);
        const date = new Date(data.ori_x[index]);
        const formattedDate = date.toLocaleDateString('ko-KR', {
            year: 'numeric',
            month: '2-digit',
            day: '2-digit'
          });
        document.getElementById('removal data').textContent =formattedDate;
        s_pred = data.t_pred.map(t => data.so - t / (alpha + beta * t)); 
        none = new Array(data.ori_x.length - s_pred.length).fill(null);
        values = none.concat(s_pred);

    } else if(data.plottype === 'hosino') {

        ctxSub.data.datasets.find(dataset => dataset.label === 'Regression Line').data = data.reg_x.map((x, index) => ({
            x: x,
            y: alpha + beta * x
        }));
        let sf = Math.sqrt(1/beta) - data.so;
        document.getElementById('sf').textContent = Math.round(-sf*100)/100;
        document.getElementById('Compaction Density').textContent = Math.round((data.sl/-sf * 100)*100)/100;
        document.getElementById('residual').textContent =Math.round((-sf - data.sl)*100)/100;  
        const index = data.ori_y2.findIndex(num=> num<-sf+remove);
        const date = new Date(data.ori_x[index]);
        const formattedDate = date.toLocaleDateString('ko-KR', {
            year: 'numeric',
            month: '2-digit',
            day: '2-digit'
          });
        document.getElementById('removal data').textContent =formattedDate;
        s_pred = data.t_pred.map(t => data.so - Math.sqrt(t / (alpha + beta * t))); 
        none = new Array(data.ori_x.length - s_pred.length).fill(null);
        values = none.concat(s_pred);
        
    } else if(data.plottype === 'asaoka') {
        
        let x_cross = alpha / (1-beta);
        let y_cross = x_cross
        let x_min = Math.min(...data.s1.map(val => val * -1));
        let x_max = Math.max(Math.max(...data.s1.map(val => val * -1)), x_cross)*1.05;
        const x_range = linspace(x_min, x_max, 10);
        const sf = alpha/(1-beta)*-1;
        ctxSub.data.datasets.find(dataset => dataset.label === 'Regression Line').data = x_range.map((x, index) => ({
            x: x,
            y: alpha + beta * x
        }));
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
        ctxSub.options.scales.x.min =x_min;
        ctxSub.options.scales.x.max =x_max;
        ctxSub.options.scales.y.min =x_min;
        ctxSub.options.scales.y.max =x_max;
        ctxSub.data.datasets[2].data = [{x:x_cross,y:y_cross}];
        ctxSub.data.datasets[3].data=[{x: x_min, y: y_cross}, {x: x_cross, y: y_cross}];
        ctxSub.data.datasets[4].data=[{x: x_cross, y:x_min}, {x: x_cross, y: y_cross}];

        s_pred = data.t_pred.slice(1).map(t=>sf - (sf - data.s1[0])* Math.exp(t*Math.log(beta)/data.timeInterval))
        console.log(s_pred);
        indicesToKeep = new Set(Array.from({ length: s_pred.length }, (_, i) => i).filter(i => i % data.timeInterval === 0));
        s_pred = s_pred.map((value, i) => indicesToKeep.has(i) ? value : null);
        none = new Array(data.ori_x.length - s_pred.length).fill(null);
        values = none.concat(s_pred);  
        ctxSub.data.datasets.find(dataset => dataset.label === 'y=x').data =  [{x:x_min,y : x_min},{x:x_max,y:x_max}];
    }


    ctxMain.data.datasets.find(dataset => dataset.label === 'Predicted').data =  dates.map((dateStr, index) => ({
        x: new Date(dateStr),
        y: values[index]}));


    // 업데이트 호출하여 그래프 변경사항 반영
    ctxSub.update();
    ctxMain.update();
}

function linspace(start, end, num) {
    if (num <= 1) {
      return [start];
    }
  
    const step = (end - start) / (num - 1);
    const result = [];
  
    for (let i = 0; i < num; i++) {
      result.push(start + (step * i));
    }
  
    return result;
  }
  