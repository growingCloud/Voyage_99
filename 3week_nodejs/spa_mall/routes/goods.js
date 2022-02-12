const express = require("express");
const router = express.Router();

// "/" = "/api/"
router.get("/", (req, res) => {
    res.send("this is root page");
});

const goods = [{
        goodsId: 4,
        name: "상품 4",
        thumbnailUrl: "https://cdn.pixabay.com/photo/2016/09/07/02/11/frogs-1650657_1280.jpg",
        category: "drink",
        price: 0.1,
    },
    {
        goodsId: 3,
        name: "상품 3",
        thumbnailUrl: "https://cdn.pixabay.com/photo/2016/09/07/02/12/frogs-1650658_1280.jpg",
        category: "drink",
        price: 2.2,
    },
    {
        goodsId: 2,
        name: "상품 2",
        thumbnailUrl: "https://cdn.pixabay.com/photo/2014/08/26/19/19/wine-428316_1280.jpg",
        category: "drink",
        price: 0.11,
    },
    {
        goodsId: 1,
        name: "상품 1",
        thumbnailUrl: "https://cdn.pixabay.com/photo/2016/09/07/19/54/wines-1652455_1280.jpg",
        category: "drink",
        price: 6.2,
    },
];

router.get("/goods", (req, res) => {
    res.json({
        goods: goods
    });
});

// "/goods/:12345 (12345가 goodsId가 됨)"
router.get("/goods/:goodsId", (req, res) => {
    const goodsId = req.params.goodsId;

    // console.log(goodsId);
    // res.send("goods Id 확인용"), 라우터를 작성하고 응답이 없으면 무한로딩에 걸리기 때문

    res.json({
        datail: goods.filter((item) => item.goodsId === Number(goodsId))[0]
    });
});

module.exports = router;