const asyncHandler = require("express-async-handler");
const dynamo_User = require("../models/userModel-dynamo");
const dynamo_Chat = require("../models/chatModel-dynamo");
const dynamo_Messages = require("../models/messageModel-dynamo");
const {v4:uuidv4}=require('uuid');
//@description     Get all Messages
//@route           GET /api/Message/:chatId
//@access          Protected
const allMessages = asyncHandler(async (req, res) => {
  try {
    const messages = (await dynamo_Messages.Message.scan().filter("chat").eq(req.params.chatId.toString()).exec()).toJSON();
    res.json(messages);
  } catch (error) {
    res.status(400);
    throw new Error(error.message);
  }
});

//@description     Create New Message
//@route           POST /api/Message/
//@access          Protected
const sendMessage = asyncHandler(async (req, res) => {
  const { content, chatId } = req.body;

  if (!content || !chatId) {
    console.log("Invalid data passed into request");
    return res.sendStatus(400);
  }


  //console.log(`First:${JSON.stringify(newMessage)}`);
  const newMessage = {
    sender: req.user._id.toString(),
    content: content,
    chat: chatId._id.toString(),
  };
  try {

    const idd=uuidv4();
    newMessage._id = idd.toString();
    console.log("connected");
    console.log(newMessage);
    const message=await dynamo_Messages.Message.create(newMessage);
    console.log(`MyNewMessage:${JSON.stringify(message)}`);
    //const latestMessage =  (await dynamo_Chat.Chat.update({"_id":chatId._id.toString()},{"latestMessage":idd}));
    const lastmessage=await message.populate();
    console.log(`Lastmessage: ${lastmessage}`);
    res.json(lastmessage);
    //await Chat.findByIdAndUpdate(req.body.chatId, { latestMessage: message });
    //
    //console.log(latestMessage);
    // Dynamodb
    
  } catch (error) {
    res.status(400);
    throw new Error(error.message);
  }
});

module.exports = { allMessages, sendMessage };
