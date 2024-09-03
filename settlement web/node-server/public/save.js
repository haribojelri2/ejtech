document.getElementById('save').addEventListener('click', function() {

    const data = dates.map((date, i) => ({ date, values: values[i] }));
    console.log(data)
    const worksheet = XLSX.utils.json_to_sheet(data);
    const workbook = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(workbook, worksheet, 'data');

    // 현재 시간을 문자열로 변환하여 파일 이름에 포함
    const now = new Date();
    const formattedDate = now.toISOString().replace(/T/, '').replace(/:/g, '').split('.')[0]; // 예: 2024-09-02_14-30-45
    const filename = `${formattedDate}.xlsx`;            // 파일 저장
    XLSX.writeFile(workbook, filename);
    console.log('Succes Saved File')
});