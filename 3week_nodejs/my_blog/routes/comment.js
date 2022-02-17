const express = require("express");
const Posting = require("../schemas/posting");
const Comments = require("../schemas/comments");
const router = express.Router();

router.get('/:postId', async(req, res) => {
    const { postId } = req.params;
    const order = req.query;
    const comments = await Comments.find({ postId: Number(postId) });

    if (order === '1') {
        comments.sort((prev, present) => {
            return prev.now_date - present.now_date;
        })
    }

    if (!comments.length) {
        return res.status(400).json({ success: false, errorMessage: "작성된 댓글이 없습니다." });
    }
    res.json(comments);
});

router.post('/write/:postId', async(req, res) => {
    const { postId } = req.params;
    const { username, comment_content } = req.body;

    if (!comment_content) {
        return res.status(400).json({ success: false, errorMessage: '댓글을 입력해주세요.' })
    }

    const post = await Posting.find({ postId: Number(postId) });
    if (!post.length) {
        return res.status(400).json({ success: false, errorMessage: '해당 게시글이 없습니다.' })
    }

    const maxCommentId = await Comments.findOne().sort('-commentId').exec();
    let commentId;
    if (maxCommentId) {
        commentId = maxCommentId.commentId + 1;
        //console.log('commentId in if sen. :', commentId);
    } else { commentId = 1 }
    //console.log('maxCommentId :', maxCommentId);
    //console.log('commentId :', commentId);

    const day = new Date();
    const month = day.getMonth() > 9 ? `${day.getMonth() + 1}` : `0${day.getMonth() + 1}`;
    const date = day.getDate() > 9 ? `${day.getDate()}` : `0${day.getDate()}`;
    const now_date = Number(`${day.getFullYear()}${month}${date}`);

    await Comments.create({
        commentId: Number(commentId),
        postId,
        username,
        comment_content,
        now_date,
    });

    res.json({ success: true });
});


router.put('/write/:commentId', async(req, res) => {
    const { commentId } = req.params;
    const { comment_content } = req.body;

    const comment = await Comments.find({ commentId: Number(commentId) });
    if (!comment.length) {
        return res.status(400).json({ success: false, errorMessage: '해당 댓글이 존재하지 않습니다' });
    }

    if (!comment_content) {
        return res.status(400).json({ success: false, errorMessage: '댓글 내용을 입력해주세요' });
    }

    await Comments.updateOne({ commentId: Number(commentId) }, {
        $set: {
            comment_content
        }
    });
    res.json({ success: true });
});

router.delete('/delete/:commentId', async(req, res) => {
    const { commentId } = req.params;
    const comment = await Comments.find({ commentId: Number(commentId) });

    if (!comment.length) {
        return res.status(400).json({ success: false, errorMessage: '해당 댓글이 존재하지 않습니다' });
    }

    await Comments.deleteOne({ commentId: Number(commentId) });
    res.json({ success: true });
})

module.exports = router;