import { useState, useRef } from "react";
import Header from "./Header";
import Footer from "./Footer";
import Messages from "./Messages";
import { Box, Grid } from "@mui/material";
import Paper from "@mui/material/Paper";
import Divider from "@mui/material/Divider";

const ChatScreen = () => {
  const [messages, setMessages] = useState([]);
  const [showDetails, setShowDetails] = useState(false);

  const uploadImg = async (file, preview, skipprocessing) => {
    const reqBody = new FormData();
    reqBody.append("skipprocessing", skipprocessing);
    reqBody.append("image", file, file.name);
    const res = await fetch(`http://localhost:5000/api/match`, {
      method: "POST",
      body: reqBody,
    });
    const data = await res.json();
    setMessages([
      ...messages,
      { file: file, preview: preview, response: data },
    ]);
    scrollToBottom();
  };

  const onToggle = () => {
    setShowDetails(!showDetails);
  };

  const messagesEndRef = useRef(null);
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  // https://www.chatbot.com/chatbot-templates/
  return (
    <Grid container p={1} justifyContent="left">
      <Box display="none" sx={{ width: 0.18 }}>
        <Paper elevation={3}>
          <Grid item></Grid>
        </Paper>
      </Box>
      <Box display="inline-grid" sx={{ width: 0.6 }}>
        <Paper elevation={3}>
          <Grid item p={2}>
            <Header />
            <Divider sx={{ mt: 2 }} />
            <Messages messages={messages} showDetails={showDetails} />
            <Divider sx={{ mt: 2 }} />
            <Footer onSend={uploadImg} onToggle={onToggle} />
            <div ref={messagesEndRef} />
          </Grid>
        </Paper>
      </Box>
    </Grid>
  );
};

export default ChatScreen;
