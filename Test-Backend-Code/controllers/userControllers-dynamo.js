const asyncHandler = require("express-async-handler");
const User = require("../models/userModel");
const generateToken = require("../config/generateToken");
const dynamo_User = require("../models/userModel-dynamo");
const {v4:uuidv4}=require('uuid');
//@description     Get or Search all users
//@route           GET /api/user?search=
//@access          Public
const allUsers = asyncHandler(async (req, res) => {
    // console.log('Search Keyword:', req.query.search);
    // console.log('MongoDB Query:', keyword);

  const dynamo_users=await dynamo_User.User.scan().filter("name").contains(req.query.search).or().filter("email").contains(req.query.search).exec();

  let users = dynamo_users.toJSON();
  users = users.filter(Element=>Element._id!== req.user._id);
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

  const userExists = (await dynamo_User.User.scan().filter('email').eq(email).attributes(["email"]).exec()).toJSON();
  console.log(`RegisterUser UserExsists:${JSON.stringify(userExists)}`);
  if (userExists.length !== 0) { 
    res.status(400);
    throw new Error("User already exists");
  }
  const password1 = await dynamo_User.save_dynamo(password);
  console.log(password1);
  //Dynamo
  const idd=uuidv4().toString();
  try{
    const user = await dynamo_User.User.create({
      _id : idd,
      name : name,
      email : email,
      password : password1,
      pic : pic
    });
    console.log("created");
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
  }catch(e){
    console.log(e);
  }
});

//@description     Auth the user
//@route           POST /api/users/login
//@access          Public
const authUser = asyncHandler(async (req, res) => {
  const { email, password } = req.body;

  const dynamo_user=await dynamo_User.User.scan().filter("email").eq(email).exec();
  const user=dynamo_user.toJSON()[0];
  console.log(user);
  console.log(password);
  console.log(email);
  if (user && (await dynamo_User.matchpassword_dynamo(password,user))) {
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
