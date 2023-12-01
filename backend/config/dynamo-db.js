const dynamoose = require("dynamoose");
require("dotenv").config();
// Create new DynamoDB instance
const connectDB=async()=>{
    try{
        
const ddb = new dynamoose.aws.ddb.DynamoDB({
    "region": 'us-east-1'
});

// Set DynamoDB instance to the Dynamoose DDB instance
dynamoose.aws.ddb.set(ddb);

}catch(e){
    console.log(e);
}};

module.exports = connectDB;