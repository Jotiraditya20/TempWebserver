const mongoose = require("mongoose");

const chatModel = mongoose.Schema(
  {
    chatName: { type: String, trim: true },
    isGroupChat: { type: Boolean, default: false },
    users: [{ type: mongoose.Schema.Types.ObjectId, ref: "User" }],
    latestMessage: {
      type: mongoose.Schema.Types.ObjectId,
      ref: "Message",
    },
    groupAdmin: { type: mongoose.Schema.Types.ObjectId, ref: "User" },
  },
  { timestamps: true }
);

const Chat = mongoose.model("Chat", chatModel);

module.exports = Chat;
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
const createChatTable =( async () => {
    const params = {
      TableName: "Chat",
      AttributeDefinitions: [
        { AttributeName: "_id", AttributeType: "S" },
        {AttributeName:"isGroupChat",AttributeType:"BOOL"},
        {AttributeName:"users",AttributeType:"S"},
        {AttributeName:"chatName",AttributeType:"S"},
        {AttributeName:"latestMessage",AttributeType:"S"},
      ],
      KeySchema: [
        { AttributeName: "_id", KeyType: "HASH" },// HASH = partition key
        {AttributeName:"isGroupChat",KeyType:"RANGE"} // Range
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
  
  model.exports=createChatTable;*/