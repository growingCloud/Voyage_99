const mongoose = require('mongoose');

const commentSchema = new mongoose.Schema({
    commentId: {
        type: Number,
        required: true,
        unique: true
    },
    postId: {
        type: Number,
        required: true,
    },
    username: {
        type: String,
        required: true
    },
    comment_content: {
        type: String,
        required: true
    },
    now_date: {
        type: Number,
        required: true,
    }
});

module.exports = mongoose.model('Comment', commentSchema);