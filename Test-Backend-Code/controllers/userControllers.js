const asyncHandler = require("express-async-handler");
const User = require("../models/userModel");
const generateToken = require("../config/generateToken");
const dynamo_User = require("../models/userModel-dynamo");
const {v4:uuidv4}=require('uuid');
//@description     Get or Search all users
//@route           GET /api/user?search=
//@access          Public
const allUsers = asyncHandler(async (req, res) => {
  //Dynamo
  const dynamo_users=await dynamo_User.User.scan().filter("name").contains(req.query.search).or().filter("email").contains(req.query.search).exec();
  const users = dynamo_users.toJSON();
  console.log(users);
  res.send(users);

});

//@description     Register new user
//@route           POST /api/user/
//@access          Public
const registerUser = asyncHandler(async (req, res) => {
  const { name, email, password, pic } = req.body;

  if (!name || !email || !password) {
    res.status(400);
    throw new Error("Please Enter all the Feilds");
  }
  const userExists = await User.findOne({ email });
  if (userExists) {
    res.status(400);
    throw new Error("User already exists");
  }

  const user = await User.create({
    name,
    email,
    password,
    pic,
  });

  if (user) {
    res.status(201).json({
      _id: user._id,
      name: user.name,
      email: user.email,
      isAdmin: user.isAdmin,
      pic: user.pic,
      token: generateToken(user._id),
    });
  } else {
    res.status(400);
    throw new Error("User not found");
  }

  //Dynamo
  const idd=uuidv4().toString();
  try{
  const dynamo_user = await dynamo_User.User.create({
    _id : user._id.toString(),
    name : name,
    email : email,
    password : password,
    pic : pic
  });
  console.log("created");
  }catch(e){
    console.log(e);
  }

  if (user) {
    res.status(201).json({
      _id: user._id,
      name: user.name,
      email: user.email,
      isAdmin: user.isAdmin,
      pic: user.pic,
      token: generateToken(user._id),
    });
  } else {
    res.status(400);
    throw new Error("User not found");
  }
  
});

//@description     Auth the user
//@route           POST /api/users/login
//@access          Public
const authUser = asyncHandler(async (req, res) => {
  const { email, password } = req.body;

  const user = await User.findOne({ email });
  console.log(user);
  let dynamo_user=await dynamo_User.User.scan().filter("email").eq(email).exec();
  dynamo_user=dynamo_user.toJSON();
  console.log(dynamo_user[0]);
  if (user && (await user.matchPassword(password))) {
    res.json({
      _id: user._id,
      name: user.name,
      email: user.email,
      isAdmin: user.isAdmin,
      pic: user.pic,
      token: generateToken(user._id),
    });
  } else {
    res.status(401);
    throw new Error("Invalid Email or Password");
  }
  
});

module.exports = { allUsers, registerUser, authUser };
