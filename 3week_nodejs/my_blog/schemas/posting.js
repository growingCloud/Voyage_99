const mongoose = require('mongoose');

const postSchema = new mongoose.Schema({
    postId: {
        type: Number,
        required: true,
        unique: true
    },
    username: {
        type: String,
        required: true
    },
    title: {
        type: String,
        required: true
    },
    content: {
        type: String,
        required: true
    },
    now_date: {
        type: Number,
        required: true
    }
});

module.exports = mongoose.model('Post', postSchema);