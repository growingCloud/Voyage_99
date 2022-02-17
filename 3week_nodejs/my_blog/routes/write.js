const express = require("express");
const Posting = require("../schemas/posting");
const Comments = require("../schemas/comments");
const router = express.Router();

router.get('/', async(req, res) => {
    const { postId, title, username, now_date, order } = req.query;
    let posts;

    if (postId) {
        posts = await Posting.find({ postId: Number(postId) });
    } else {
        posts = await Posting.find();
    }

    if (title) {
        posts = posts.filter((post) => post.title === title);
    }
    if (username) {
        posts = posts.filter((post) => post.username === username);
    }
    if (now_date) {
        posts = posts.filter((post) => post.now_date === Number(now_date));
    }
    if (order === '1') {
        posts.sort((prev, present) => present.now_date - prev.now_date);
    }

    if (posts.length) {
        return res.json(posts);
    }

    res.status(400).json({ success: false, errorMessage: '해당 조건의 게시글이 없습니다.' });
});


router.post('/write', async(req, res) => {
    const maxPostId = await Posting.findOne().sort('-postId').exec();
    let postId = 1

    if (maxPostId) {
        postId = maxPostId.postId + 1
    }

    const { username, title, content } = req.body;

    const day = new Date();
    const month = day.getMonth() > 9 ? `${day.getMonth() + 1}` : `0${day.getMonth() + 1}`;
    const date = day.getDate() > 9 ? `${day.getDate()}` : `0${day.getDate()}`;
    const now_date = Number(`${day.getFullYear()}${month}${date}`);

    await Posting.create({
        postId,
        username,
        title,
        content,
        now_date
    });

    res.json({ success: true });
});

router.put('/write/:postId', async(req, res) => {
    const { postId } = req.params;
    const { title, username, content } = req.body;

    await Posting.updateOne({ postId: Number(postId) }, {
        $set: {
            title,
            username,
            content
        }
    });
    res.json({ success: true })
});

router.delete('/delete/:postId', async(req, res) => {
    const { postId } = req.params;

    const post = await Posting.find({ postId: Number(postId) });
    if (!post.length) {
        return res.status(400).json({ success: false, errorMessage: '해당 게시글은 존재하지 않습니다.' });
    }
    await Posting.deleteOne({ postId: Number(postId) });
    await Comments.deleteMany({ postId: Number(postId) });
    res.json({ success: true });
});

router.get('/:postId', async(req, res) => {
    const { postId } = req.params;

    const [post] = await Posting.find({ postId: Number(postId) });

    if (post) {
        return res.json(post);
    }
    res.status(400).json({
        success: false,
        errorMessage: '해당 게시글은 존재하지 않습니다.'
    });
});

module.exports = router;