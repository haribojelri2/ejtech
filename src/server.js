const express = require('express');
const multer = require('multer');
const path = require('path');
const axios = require('axios');
const FormData = require('form-data');
const fs = require('fs');
const bodyParser = require('body-parser');
const app = express();
const compression = require('compression');

// 압축 미들웨어 사용
app.use(compression());

// 파일 저장 설정
const storage = multer.diskStorage({
    destination: function (req, file, cb) {
        // Azure에서 플랫폼 독립적인 경로 설정
        const uploadPath = path.resolve(__dirname, 'uploads');
        if (!fs.existsSync(uploadPath)) {
            fs.mkdirSync(uploadPath, { recursive: true });
        }
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
    const { plotType, timeInterval, startDate, endDate, predict_date } = req.body;

    if (!file || !plotType || !startDate || !endDate || !predict_date) {
        return res.status(400).json({ error: 'Not required field' });
    }

    if (plotType === 'asaoka' && (!timeInterval || !startDate || !endDate || !predict_date)) {
        return res.status(400).json({ error: 'Not required field' });
    }

    if ((plotType === 'hosino' || plotType === 'hyperbolic') && (!startDate || !endDate || !predict_date)) {
        return res.status(400).json({ error: 'Not required field' });
    }

    // 파일 경로 설정
    const filePath = path.resolve(__dirname, 'uploads', file.filename);
    const form = new FormData();
    form.append('file', fs.createReadStream(filePath));
    form.append('plotType', plotType);
    form.append('timeInterval', timeInterval);
    form.append('startDate', startDate);
    form.append('endDate', endDate);
    form.append('predict_date', predict_date);

    const pythonServerUrl = 'http://<flask-server-url>/process-file';

    try {
        // Python 서버로 파일 전송
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

// JSON 본문 파싱 미들웨어
app.use(bodyParser.json());

// 업데이트 라우트
app.post('/update', (req, res) => {
    const { alpha, beta } = req.body;
    res.json({ alpha, beta });
});

// 정적 파일 제공
app.use(express.static(path.join(__dirname, 'public'), { maxAge: '1d' }));

// 안전 페이지 라우트
app.get('/safe', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'safe.html'));
});

// 서버 시작
const port = process.env.PORT || 3000;
const hostname = '0.0.0.0';  // 모든 네트워크 인터페이스에서 접근 허용

app.listen(port, hostname, () => {
    console.log(`Server running on http://${hostname}:${port}`);
});
