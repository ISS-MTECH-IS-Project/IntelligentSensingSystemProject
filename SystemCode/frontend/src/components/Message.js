import { Box, Grid } from "@mui/material";
import Paper from "@mui/material/Paper";
import { styled } from "@mui/material/styles";
import Table from "@mui/material/Table";
import TableBody from "@mui/material/TableBody";
import TableCell from "@mui/material/TableCell";
import TableContainer from "@mui/material/TableContainer";
import TableHead from "@mui/material/TableHead";
import TableRow from "@mui/material/TableRow";

const StyledTableRow = styled(TableRow)(({ theme }) => ({
  "&:nth-of-type(odd)": {
    backgroundColor: theme.palette.action.hover,
  },
  // hide last border
  "&:last-child td, &:last-child th": {
    backgroundColor: theme.palette.success.light,
  },
}));
const Message = ({ message, showDetails }) => {
  return (
    <Grid container direction="row" p={1}>
      <Grid item display="inline-flex">
        <Grid container direction="column" alignContent="flex-start" p={1}>
          <Grid item alignItems="flex">
            <img
              alt="Spot My Fish"
              src="/static/images/sample/favicon-32x32.png"
            />
            <span>{message.file.name}</span>
          </Grid>
          <Grid item display="inline-flex">
            <Paper>
              <Box>
                <img alt="User Input" width={400} src={message.preview} />
                <img
                  alt="Matched Output"
                  width={400}
                  src={"/static/images/" + message.response.result}
                />
              </Box>
            </Paper>
          </Grid>
        </Grid>
      </Grid>
      {/* <Grid item display="inline-flex" p={1}>
        {showDetails && (
          <TableContainer component={Paper}>
            <Table size="small" aria-label="simple table">
              <TableHead>
                <TableRow>
                  <TableCell>
                    <b>Model Name</b>
                  </TableCell>
                  <TableCell align="left">
                    <b>Classify Output</b>
                  </TableCell>
                  <TableCell align="right">
                    <b>Probability</b>
                  </TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {message.response.result.map((row, i) => (
                  <StyledTableRow
                    key={i}
                    sx={{
                      "&:last-child td, &:last-child th": { border: 0 },
                    }}
                  >
                    <TableCell component="th" scope="row">
                      {row.model_name}
                    </TableCell>
                    <TableCell align="left">{row.type}</TableCell>
                    <TableCell align="right">
                      {row.probability.toFixed(2)}%
                    </TableCell>
                  </StyledTableRow>
                ))}
              </TableBody>
            </Table>
          </TableContainer>
        )}
      </Grid> */}
    </Grid>
  );
};

export default Message;
