import Message from "./Message";
import Grid from "@mui/material/Grid";

const Messages = ({ messages, showDetails }) => {
  return (
    <Grid>
      {messages.map((m, i) => (
        <Message key={"ID" + i} message={m} showDetails={showDetails} />
      ))}
    </Grid>
  );
};

export default Messages;
