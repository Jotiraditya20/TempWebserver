const asyncHandler = require("express-async-handler");
const Message = require("../models/messageModel");
const User = require("../models/userModel");
const Chat = require("../models/chatModel");
const dynamo_User = require("../models/userModel-dynamo")
const dynamo_Chat = require("../models/chatModel-dynamo");
const dynamo_Messages = require("../models/messageModel-dynamo");
//@description     Get all Messages
//@route           GET /api/Message/:chatId
//@access          Protected
const allMessages = asyncHandler(async (req, res) => {
  try {
    const messages = await Message.find({ chat: req.params.chatId })
      .populate("sender", "name pic email")
      .populate("chat");
      console.log(`ALLMESSAGES:${req.params.chatId}`);
    res.json(messages);

    //Dynamo
    const dynamo_messages = (await dynamo_Messages.Message.scan().filter("chat").eq(req.params.chatId.toString()).exec()).toJSON();
    console.log(dynamo_messages);
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

  var newMessage = {
    sender: req.user._id,
    content: content,
    chat: chatId,
  };
  //console.log(`First:${JSON.stringify(newMessage)}`);
  const newMessage1 = {
    sender: req.user._id.toString(),
    content: content,
    chat: chatId._id.toString(),
  };
  try {
    var message = await Message.create(newMessage);

    message = await message.populate("sender", "name pic").execPopulate();
    message = await message.populate("chat").execPopulate();
    message = await User.populate(message, {
      path: "chat.users",
      select: "name pic email",
    });

    await Chat.findByIdAndUpdate(req.body.chatId, { latestMessage: message });
    // Dynamodb
    newMessage1._id = message._id.toString();
    console.log("connected");
    console.log(newMessage1);
    const dynamo_message=await dynamo_Messages.Message.create(newMessage1);
    console.log(`MyNewMessage:${dynamo_message}`);
    res.json(message);
  } catch (error) {
    res.status(400);
    throw new Error(error.message);
  }
});

module.exports = { allMessages, sendMessage };
