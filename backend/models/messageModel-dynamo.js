const dynamoose = require('dynamoose');
const User = require("./userModel-dynamo");
const Chat = require("./chatModel-dynamo");
const messageSchema= new dynamoose.Schema(
  {

      "_id": String,
      "sender": User.User,
      "content":{
          "type": String,
          "required":true
      },
      "chat": Chat.Chat,
      "readBy": User.User,
  },{
      "timestamps": true
  }
);
const Message = dynamoose.model("Message", messageSchema,{create:true,waitForActive:true});
module.exports = {Message};
