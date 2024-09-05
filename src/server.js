const express = require('express');
const multer = require('multer');
const path = require('path');
const axios = require('axios');
const FormData = require('form-data');
const fs = require('fs');
const bodyParser = require('body-parser');
const app = express();
const compression = require('compression');

app.use(compression());
// 파일 저장 설정
const storage = multer.diskStorage({
    destination: function (req, file, cb) {
        const uploadPath = process.env.TEMP || 'D:\\home\\LogFiles';
        cb(null, uploadPath);
    },
    filename: function (req, file, cb) {
        cb(null, Date.now() + path.extname(file.originalname));
    }
});

// 업로드 객체 생성
const upload = multer({ storage: storage });

// 파일 업로드 라우트
app.post('/upload', upload.single('file'), async (req, res) => {
    const file = req.file;
    const plotType = req.body.plotType;
    const timeInterval = req.body.timeInterval;
    const startDate = req.body.startDate;
    const endDate = req.body.endDate;
    const predict_date = req.body.predict_date;
    if (!file || !plotType  || !startDate || !endDate || !predict_date) {
        return res.status(400).send({ error: 'Not required field' });
    }

    else if (plotType === 'asaoka' && ( !timeInterval || !startDate || !endDate || !predict_date)) {
        return res.status(400).send({ error: 'Not required field' });
    }
    // plotType이 'hosino'일 때 추가 필드를 요구하는 경우
    else if ((plotType === 'hosino' || plotType ==='hyperbolic')  && (!startDate || !endDate || !predict_date)) {
        return res.status(400).send({ error: 'Not required field' });
    }
    // 공통 체크


    // 파일 경로 수정
    const filePath = path.resolve(__dirname, '..', 'uploads', file.filename);
    const form = new FormData();
    form.append('file', fs.createReadStream(filePath));
    form.append('plotType', plotType);
    form.append('timeInterval', timeInterval);
    form.append('startDate', startDate);
    form.append('endDate', endDate);
    form.append('predict_date', predict_date);
    const pythonServerUrl = 'http://settlementpython-dqdbezh9eqfvekdd.koreacentral-01.azurewebsites.net:5000/process-file';

    // Python 서버로 파일 전송을 비동기로 처리
    try {
        const response = await axios.post(pythonServerUrl, form, {
            headers: {
                ...form.getHeaders()
            }
        });
        res.json(response.data);
    } catch (error) {
        console.error('Error sending file to Python server:', error);
        res.status(500).json({ error: 'Failed to send file to Python server' });
    }
});

app.use(bodyParser.json());

app.post('/update', (req, res) => {
    const { alpha, beta } = req.body;
    res.json({alpha, beta  });
});

app.use(express.static(path.join(__dirname, '..', 'public'), { maxAge: '1d' }));
app.get('/safe', (req, res) => {
    res.sendFile(path.join(__dirname, '..', 'public','safe.html'));
})
const port = process.env.PORT || 3000;
const hostname = '0.0.0.0';  // 모든 네트워크 인터페이스에서 접근 허용

app.listen(port, hostname, () => {
    console.log(`Server running on http://${hostname}:${port}`);
});

