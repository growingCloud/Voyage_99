// 기본적인 웹서버 코드 작성 과정 

const express = require("express");
const connect = require("./schemas");
const app = express();
const port = 3002;

connect();

const goodsRouter = require("./routes/goods.js");
const cartsRouter = require("./routes/carts.js");

const requestMiddleware = (req, res, next) => {
    console.log("Request URL : ", req.originalUrl, " - ", new Date());
    next();
};

// use : 미들웨어 사용 (다른것들보다 위에 있어야 다른 애들이 미들웨어의 영향 안에 들어올 수 있음)
// app.use((req, res, next) => {
//     console.log("미들웨어가 구현되었어요!");
//     console.log("주소는?", req.path); // 구현되어 있지 않아도 미들웨어는 항상 동작한다!
//     if (req.path === "/test") {
//         res.send("테스트 주소로 왔습니다")
//     } else {
//         next(); // 다음 미들웨어? 라우터?로 넘기기 위한 필수 항목 (없으면 무한로딩)
//     }
// });

app.use(express.json());
app.use(requestMiddleware);

app.use("/api", [goodsRouter, cartsRouter]);

// get : 
app.get('/', (req, res) => {
    res.send("Hello world");
});

// listen : 
app.listen(port, () => {
    console.log(port, "포트로 서버가 켜졌어요!");
});

// ----- 완료