const mongoose = require("mongoose");
const bcrypt = require("bcryptjs");

const userSchema = mongoose.Schema(
  {
    name: { type: "String", required: true },
    email: { type: "String", unique: true, required: true },
    password: { type: "String", required: true },
    pic: {
      type: "String",
      required: true,
      default:
        "https://icon-library.com/images/anonymous-avatar-icon/anonymous-avatar-icon-25.jpg",
    },
    isAdmin: {
      type: Boolean,
      required: true,
      default: false,
    },
  },
  { timestaps: true }
);

userSchema.methods.matchPassword = async function (enteredPassword) {
  return await bcrypt.compare(enteredPassword, this.password);
};

userSchema.pre("save", async function (next) {
  if (!this.isModified) {
    next();
  }

  const salt = await bcrypt.genSalt(10);
  this.password = await bcrypt.hash(this.password, salt);
});

const User = mongoose.model("User", userSchema);

module.exports = User;

/*
const { DynamoDBClient, PutItemCommand ,CreateTableCommand} = require("@aws-sdk/client-dynamodb");
require('dotenv').config();
const credentials = {
    region: process.env.REGION,
    credentials: {
      accessKeyId: process.env.ACCESSKEY,
      secretAccessKey: process.env.SECRETKEY
    }
  };
const dynamoDBClient = new DynamoDBClient(credentials);
const createUserTable =( async () => {
    const params = {
      TableName: "users",
      AttributeDefinitions: [
        { AttributeName: "_id", AttributeType: "S" },
        { AttributeName: "pic", AttributeType: "S" },
        { AttributeName: "isAdmin", AttributeType: "BOOL" },
        { AttributeName: "name", AttributeType: "S" },
        { AttributeName: "email", AttributeType: "S" },
        { AttributeName: "password", AttributeType: "S" }
      ],
      KeySchema: [
        { AttributeName: "_id", KeyType: "HASH" },// HASH = partition key
        { AttributeName: "email", KeyType: "RANGE" },
         
      ],
      ProvisionedThroughput: {
        ReadCapacityUnits: 5,
        WriteCapacityUnits: 5,
      },
    };
  
    try {
      await dynamoDBClient.send(new CreateTableCommand(params));
      console.log("Table created successfully!");
    } catch (err) {
      console.error("Error creating table:", err);
    }
});
module.exports=createUserTable;
*/