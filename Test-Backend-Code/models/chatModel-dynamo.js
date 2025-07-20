const dynamoose = require("dynamoose");
const User = require("./userModel-dynamo");

const chatModel = new dynamoose.Schema(
    {
        "_id": String,
        "chatName":{
            "type":String,
        },
        "isGroupChat":{
            "type":Boolean,
            "default":false
        },
        "users":{
            "type":Array,
            "schema":[User.User],
        },
        "latestMessage":{
            "type":String,
        },
        "groupAdmin": User.User,
    },
    {
        "timestamps": true
    }
);

const Chat = dynamoose.model("Chat",chatModel,{create: true,waitForActive: true});

module.exports = {Chat};