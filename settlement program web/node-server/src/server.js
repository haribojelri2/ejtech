const express = require('express');
const multer = require('multer');
const path = require('path');
const axios = require('axios');
const FormData = require('form-data');
const fs = require('fs');

const app = express();

// 파일 저장 설정
const storage = multer.diskStorage({
    destination: function (req, file, cb) {
        cb(null, path.join(__dirname, '..', 'uploads'));
    },
    filename: function (req, file, cb) {
        cb(null, Date.now() + path.extname(file.originalname)); // 파일 이름 설정
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
    if (!file) {
        return res.status(400).json({ error: 'No file uploaded' });
    }

    // 파일 경로 수정
    const filePath = path.resolve(__dirname, '..', 'uploads', file.filename);
    const form = new FormData();
    form.append('file', fs.createReadStream(filePath));
    form.append('plotType', plotType);
    form.append('timeInterval', timeInterval);
    form.append('startDate', startDate);
    form.append('endDate', endDate);
    form.append('predict_date', predict_date);

    const pythonServerUrl = 'http://localhost:5000/process-file';

    // Python 서버로 파일 전송을 비동기로 처리
    try {
        const response = await axios.post(pythonServerUrl, form, {
            headers: {
                ...form.getHeaders()
            }
        });
        fs.unlinkSync(filePath);
        res.json(response.data);
    } catch (error) {
        console.error('Error sending file to Python server:', error);
        res.status(500).json({ error: 'Failed to send file to Python server' });
    }
});

app.use(express.static(path.join(__dirname, '..', 'public')));

app.set('port', process.env.PORT || 3000);

app.listen(app.get('port'), () => {
    console.log(`Server running on port ${app.get('port')}`);
});
