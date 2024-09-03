function calculateSlope(x1, y1, x2, y2) {
    return (y2 - y1) / (x2 - x1);
}

// 절편 구하기 함수
function calculateIntercept(x1, y1, slope) {
    return y1 - slope * x1;
}