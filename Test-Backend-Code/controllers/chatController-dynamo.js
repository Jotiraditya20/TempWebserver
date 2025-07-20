const asyncHandler = require("express-async-handler");
const {v4:uuidv4}=require('uuid');
const Chat = require("../models/chatModel");
const User = require("../models/userModel");
const dynamo_Chat = require("../models/chatModel-dynamo");
const dynamo_User = require("../models/userModel-dynamo");
//@description     Create or fetch One to One Chat
//@route           POST /api/chat/
//@access          Protected
//Find
const accessChat = asyncHandler(async (req, res) => {
  const { userId } = req.body;

  if (!userId) {
    console.log("UserId param not sent with request");
    return res.sendStatus(400);
  }

  //dynamo
  try{
    //console.log("Chat Sacn");
    const dynamo_chats= (await dynamo_Chat.Chat.scan().filter("isGroupChat").eq(false).exec()).toJSON() || [];
    //console.log(dynamo_chats);
    const filtered_dynamo_chat = dynamo_chats.filter(Element =>
      Element.users.includes(userId.toString()) && Element.users.includes(req.user._id.toString())
    );
    //console.log(filtered_dynamo_chat);
    let isChat;
    if(filtered_dynamo_chat.length !== 0){
    isChat=(await (await dynamo_Chat.Chat.scan().filter("_id").eq(filtered_dynamo_chat[0]._id).exec()).populate()).toJSON()[0];
    }
    // isChat = await User.populate(isChat, {
      // path: "latestMessage.sender",
      // select: "name pic email",
    // });
    console.log(`isChat:${isChat}`);
    if (isChat) {
      res.send(isChat);
    } else {
      var chatData = {
        chatName: "sender",
        isGroupChat: false,
        users: [req.user._id, userId],
      };


      try {
        //Dynamo
        const id=uuidv4();
        chatData._id = id.toString();
        chatData.users[0]=chatData.users[0].toString();
        console.log(chatData);
        const createdChat_dynamo = await dynamo_Chat.Chat.create(chatData);
        const FullChat = (await createdChat_dynamo.populate()).toJSON();
        console.log(FullChat);
        console.log("Create Chat Itwm")
        res.status(200).json(FullChat);
      } catch (error) {
        res.status(400);
        console.log(error);
        throw new Error(error.message);
      }

    }
  }catch(e){
    console(e);
  }
//Comeback

});

//@description     Fetch all chats for a user
//@route           GET /api/chat/
//@access          Protected
const fetchChats = asyncHandler(async (req, res) => {
  try {

      //console.log(results);
      const dynamo_chats= (await dynamo_Chat.Chat.scan().exec()).toJSON();
      const filtered_dynamo_chat = dynamo_chats.filter(Element =>
        Element.users.includes(req.user._id.toString())
      );
      const pop_chat = [];
      for(const Chats of filtered_dynamo_chat) {
        pop_chat.push((await (await dynamo_Chat.Chat.scan().filter("_id").eq(Chats._id).exec()).populate()).toJSON()[0]);
      }
      //console.log(`Our CONSOLW`);
      //console.log(pop_chat);
     // console.log(JSON.stringify(pop_chat));
     
      res.status(200).send(pop_chat);

  } catch (error) {
    res.status(400);
    throw new Error(error.message);
  }
});

//@description     Create New Group Chat
//@route           POST /api/chat/group
//@access          Protected
const createGroupChat = asyncHandler(async (req, res) => {
  if (!req.body.users || !req.body.name) {
    return res.status(400).send({ message: "Please Fill all the feilds" });
  }
  const users = JSON.parse(req.body.users);

  if (users.length < 2) {
    return res
      .status(400)
      .send("More than 2 users are required to form a group chat");
  }
  const idd=uuidv4();
  users.push(req.user._id.toString());
  console.log(users);
  try {
    /*console.log(`MongoGroupChat: ${groupChat}`);
    console.log(req.body.name);
    console.log(users1);
    console.log(req.user);
    console.log(groupChat._id);*/
    //Dynamo Create Group
    const dyn_groupChat = await dynamo_Chat.Chat.create({
      chatName: req.body.name,
      users: users,
      isGroupChat: true,
      groupAdmin: req.user._id.toString(),
      _id: idd.toString()
    });
    
    // console.log(`GroupChat: ${dyn_groupChat}`);
    

      // console.log(`MongoGroupChatPop: ${fullGroupChat}`);
    const fullGroupChat = (await ( await dynamo_Chat.Chat.scan().filter('_id').eq(dyn_groupChat._id).exec()).populate()).toJSON()[0];
    //console.log(`GroupChatpop: ${JSON.stringify(dyn_fullGroupChat)}`);
    res.status(200).json(fullGroupChat);
  } catch (error) {
    res.status(400);
    throw new Error(error.message);
  }
});

// @desc    Rename Group
// @route   PUT /api/chat/rename
// @access  Protected
const renameGroup = asyncHandler(async (req, res) => {
  const { chatId, chatName } = req.body;
    // console.log(`Updated:${updatedChat}`);
    const dyn_fullGroupChat =  (await dynamo_Chat.Chat.update({"_id":chatId.toString()},{"chatName":chatName})) || [];
    let updatedChat=[];
    if(dyn_fullGroupChat != []){
    updatedChat=(await(await dynamo_Chat.Chat.scan().filter('_id').eq(chatId.toString()).exec()).populate()).toJSON()[0];
  }
    // console.log(`UpdatedDynamo:${dyn_fullGroupChat}`);
    // console.log(`FullPOP:${JSON.stringify(dyn_fullGroupChatpop)}`);
  if (updatedChat.length ===0) {
    res.status(404);
    throw new Error("Chat Not Found");
  } else {
    res.json(updatedChat);
  }
});

// @desc    Remove user from Group
// @route   PUT /api/chat/groupremove
// @access  Protected
const removeFromGroup = asyncHandler(async (req, res) => {
  const { chatId, userId } = req.body;
  const removed=0;
  // check if the requester is admin
/*
  const removed = await Chat.findByIdAndUpdate(
    chatId,
    {
      $pull: { users: userId },
    },
    {
      new: true,
    }
  )
    .populate("users", "-password")
    .populate("groupAdmin", "-password");
*/
  if (!removed) {
    res.status(404);
    throw new Error("Chat Not Found");
  } else {
    res.json(removed);
  }
});

// @desc    Add user to Group / Leave
// @route   PUT /api/chat/groupadd
// @access  Protected
const addToGroup = asyncHandler(async (req, res) => {
  const added=0;
  /*
  const { chatId, userId } = req.body;

  // check if the requester is admin

  const added = await Chat.findByIdAndUpdate(
    chatId,
    {
      $push: { users: userId },
    },
    {
      new: true,
    }
  )
    .populate("users", "-password")
    .populate("groupAdmin", "-password");
*/
  if (!added) {
    res.status(404);
    throw new Error("Chat Not Found");
  } else {
    res.json(added);
  }
});

module.exports = {
  accessChat,
  fetchChats,
  createGroupChat,
  renameGroup,
  addToGroup,
  removeFromGroup,
};
