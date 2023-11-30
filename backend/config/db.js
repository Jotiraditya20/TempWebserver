const mongoose = require("mongoose");
const colors = require("colors");

const connectDB = async () => {
  try {
    const conn = await mongoose.connect(process.env.MONGO_URI, {
      useNewUrlParser: true,
      useUnifiedTopology: true,
    });

    console.log(`MongoDB Connected: ${conn.connection.host}`.cyan.underline);
  } catch (error) {
    console.error(`Error: ${error.message}`.red.bold);
    process.exit(1); // Exit with a non-zero status code to indicate an error
  }
};

module.exports = connectDB;

//Connecting to DB /*
/*
const {DynamoDBClient, ListTablesCommand} =require("@aws-sdk/client-dynamodb")
require('dotenv').config();

const credentials = {
  region: process.env.REGION,
  credentials: {
    accessKeyId: process.env.ACCESSKEY,
    secretAccessKey: process.env.SECRETKEY
  }
};
const client=new DynamoDBClient(credentials);
(async()=>{
  const command=new ListTablesCommand({});
  try{
    const results = await client.send(command);
    console.log(results.TableNames.join("\n"));
  }catch(err){
    console.log(err);
  }
})();
module.exports = client;*/