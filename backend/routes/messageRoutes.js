const express = require("express");
const {
  allMessages,
  sendMessage,
} = require("../controllers/messageControllers-dynamo");
const { protect } = require("../middleware/authMiddleware");

const router = express.Router();

router.route("/:chatId").get(protect, allMessages);
router.route("/").post(protect, sendMessage);

module.exports = router;
