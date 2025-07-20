const dynamoose=require("dynamoose");
const bcrypt=require("bcryptjs");
const connectDB = require("../config/dynamo-db");

const userSchema= new dynamoose.Schema(
    {

        "_id": String,
        "name": String,
        "email": {
            "type": String,
            "required": true,
            
        },
        "password":{
            "type": String,
            "required":true
        },
        "pic":{
            "type": String,
            "required": true,
            "default":"https://icon-library.com/images/anonymous-avatar-icon/anonymous-avatar-icon-25.jpg",
        },
        "isAdmin": {
            "type":Boolean,
            "required": true,
            "default":false,
        },
    },{
        "timestamps": true
    }
);

const matchpassword_dynamo=async(enteredPassword,user)=>{
    return await bcrypt.compare(enteredPassword, user.password);
};
console.log(userSchema.hashKey);

const save_dynamo=async(password)=>{
    const salt= await bcrypt.genSalt(10);
    password=await bcrypt.hash(password, salt);
    return password;
}

const User= dynamoose.model("User",userSchema,{create:true,waitForActive:true});

module.exports={User, matchpassword_dynamo,save_dynamo};