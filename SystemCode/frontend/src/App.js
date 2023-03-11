import { BrowserRouter, Routes, Route } from "react-router-dom";
import "./App.css";
import ChatScreen from "./components/ChatScreen";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<ChatScreen />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
