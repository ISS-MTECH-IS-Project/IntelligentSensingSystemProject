import { ButtonGroup, Grid } from "@mui/material";
import Button from "@mui/material/Button";
import { useEffect, useState, useRef, useCallback } from "react";
import Tooltip from "@mui/material/Tooltip";
import SendIcon from "@mui/icons-material/Send";
import FormGroup from "@mui/material/FormGroup";
import FormControlLabel from "@mui/material/FormControlLabel";
import Switch from "@mui/material/Switch";
import Webcam from "react-webcam";
import { ReactSketchCanvas } from "react-sketch-canvas";
import Modal from "react-modal";

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
  const canvas = useRef(null);

  const [skipprocessing, setSkipprocessing] = useState(false);
  const [modalIsOpen, setIsOpen] = useState(false);

  function openModal() {
    setIsOpen(true);
  }
  function closeModal() {
    setIsOpen(false);
  }
  function undoModal() {
    canvas.current.undo();
  }
  function redoModal() {
    canvas.current.redo();
  }
  function clearModal() {
    canvas.current.clearCanvas();
  }

  const updateImage = async (data) => {
    const blob = await fetch(data).then((res) => res.blob());
    blob.name = "screenshot" + Date.now() + ".jpg";
    blob.lastModified = new Date();
    setImage(blob);
    setPreview(data);
  };

  const exportDraw = useCallback(async () => {
    setSkipprocessing(true);
    canvas.current
      .exportImage("jpeg")
      .then((data) => {
        updateImage(data);
        closeModal();
      })
      .catch((e) => {
        console.log(e);
      });
  });
  const capture = useCallback(async () => {
    setSkipprocessing(false);
    const pictureSrc = webcamRef.current.getScreenshot();
    updateImage(pictureSrc);
  });
  const onClickF = () => {
    console.log("button clicked");
    onSend(image, preview, skipprocessing);
    setImage(null);
    setUploadImage(null);
  };

  const handleChange = (e) => {
    console.log(e.target);
    setSkipprocessing(false);
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
          <Button onClick={openModal} variant="contained" component="label">
            Draw
          </Button>
        </div>
      </Grid>
      <Grid item xs={5}>
        <img width={400} src={preview}></img>
        <div>
          <Modal
            isOpen={modalIsOpen}
            onRequestClose={closeModal}
            contentLabel="Example Modal"
            ariaHideApp={false}
          >
            <Button onClick={closeModal} variant="contained" component="label">
              close
            </Button>
            <Button
              variant="contained"
              component="label"
              onClick={(e) => {
                e.preventDefault();
                exportDraw();
              }}
            >
              Get Image
            </Button>
            <Button onClick={undoModal} variant="contained" component="label">
              Undo
            </Button>
            <Button onClick={redoModal} variant="contained" component="label">
              Redo
            </Button>
            <Button onClick={clearModal} variant="contained" component="label">
              Clear
            </Button>
            <ReactSketchCanvas
              ref={canvas}
              strokeWidth={5}
              strokeColor="black"
              height="90%"
              width="50%"
            />
          </Modal>
        </div>
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
