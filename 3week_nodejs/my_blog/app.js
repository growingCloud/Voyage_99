const express = require("express");
const connect = require("./schemas");
const app = express();
const port = 3005;

connect();

const writeRouter = require("./routes/write.js");
const commentRouter = require("./routes/comment.js");

const requestMiddleware = (req, res, next) => {
    console.log("Request URL : ", req.originalUrl, " - ", new Date());
    next();
};


app.use(express.json());
app.use(requestMiddleware);

app.use("/post", [writeRouter]);
app.use("/comment", [commentRouter]);

app.get('/', (req, res) => {
    res.send("Hello world");
});

app.listen(port, () => {
    console.log('listening on 3005')
});