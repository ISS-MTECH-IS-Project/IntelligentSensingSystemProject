import { ButtonGroup, Grid } from "@mui/material";
import Button from "@mui/material/Button";
import { useEffect, useState, useRef, useCallback } from "react";
import Tooltip from "@mui/material/Tooltip";
import SendIcon from "@mui/icons-material/Send";
import FormGroup from "@mui/material/FormGroup";
import FormControlLabel from "@mui/material/FormControlLabel";
import Switch from "@mui/material/Switch";
import Webcam from "react-webcam";
const videoConstraints = {
  width: 400,
  height: 400,
  facingMode: "user",
};
const Footer = ({ onSend, onToggle }) => {
  const [image, setImage] = useState();
  const [preview, setPreview] = useState();
  const [uploadImage, setUploadImage] = useState();
  const webcamRef = useRef(null);

  const capture = useCallback(async () => {
    const pictureSrc = webcamRef.current.getScreenshot();
    const blob = await fetch(pictureSrc).then((res) => res.blob());
    blob.name = "screenshot" + Date.now() + ".jpg";
    blob.lastModified = new Date();
    setImage(blob);
    setPreview(pictureSrc);
  });
  const onClickF = () => {
    console.log("button clicked");
    onSend(image, preview);
    setImage(null);
    setUploadImage(null);
  };

  const handleChange = (e) => {
    console.log(e.target);
    setImage(e.target.files[0]);
    setUploadImage(e.target.files[0]);
  };

  useEffect(() => {
    if (uploadImage) {
      const reader = new FileReader();
      reader.onloadend = () => {
        setPreview(reader.result);
      };
      reader.readAsDataURL(uploadImage);
    } else {
      setPreview(null);
    }
  }, [uploadImage]);

  return (
    <Grid mt={3} container direction="row" alignItems="center">
      <Grid item xs={5}>
        <div>
          <Webcam
            audio={false}
            ref={webcamRef}
            screenshotFormat="image/jpeg"
            videoConstraints={videoConstraints}
          />
        </div>
        <div>
          <button
            onClick={(e) => {
              e.preventDefault();
              capture();
            }}
            className="btn btn-danger"
          >
            Capture from Camera
          </button>
          <Button variant="contained" component="label">
            Upload
            <input
              hidden
              accept="image/*"
              multiple={false}
              type="file"
              onChange={handleChange}
            />
          </Button>
        </div>
      </Grid>
      <Grid item xs={5}>
        <img width={400} src={preview}></img>
      </Grid>
      <Grid item xs={2} alignItems="flex-end">
        <Grid container direction="column" alignContent="flex-end">
          <ButtonGroup orientation="vertical">
            <Tooltip title="Send my response">
              <Button
                variant="contained"
                onClick={onClickF}
                endIcon={<SendIcon />}
              >
                Send
              </Button>
            </Tooltip>
            {/* <FormGroup>
              <FormControlLabel
                control={<Switch defaultChecked={false} onClick={onToggle} />}
                label="More details"
              />
            </FormGroup> */}
          </ButtonGroup>
        </Grid>
      </Grid>
    </Grid>
  );
};

export default Footer;
