const express = require("express");
const Goods = require("../schemas/goods");
const router = express.Router();

// "/" = "/api/"
router.get("/", (req, res) => {
    res.send("this is root page");
});


router.get("/goods", async(req, res) => {
    const { category } = req.query;
    console.log("category : ", category);

    const goods = await Goods.find({ category })

    res.json({ goods: goods });
});

// "/goods/:12345 (12345가 goodsId가 됨)"
router.get("/goods/:goodsId", async(req, res) => {
    const { goodsId } = req.params;

    const [detail] = await Goods.find({ goodsId: Number(goodsId) });

    // console.log(goodsId);
    // res.send("goods Id 확인용"), 라우터를 작성하고 응답이 없으면 무한로딩에 걸리기 때문

    // const [datail] = goods.filter((item) => item.goodsId === Number(goodsId));

    res.json({ detail });
});


router.post("/goods", async(req, res) => {
    const { goodsId, name, thumbnailUrl, category, price } = req.body;

    const goods = await Goods.find({ goodsId });
    if (goods.length) {
        return res.status(400).json({ success: false, errorMessage: "이미 있는 데이터 입니다." });
    }

    const createdGoods = await Goods.create({ goodsId, name, thumbnailUrl, category, price });

    res.json({ goods: createdGoods });
});

module.exports = router;