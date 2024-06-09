import { BrowserRouter, Routes, Route } from "react-router-dom";
import { ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import Footer from "./components/Footer";
import Navbar from "./components/Navbar";
import Home from "./pages/Home";
import Login from "./pages/Login";
import { AuthProvider } from "./context/AuthContext";
import Problems from "./pages/Problems";
import SingleProblem from "./pages/SingleProblem";
import CreateAccount from "./pages/CreateAccount";
import AddProblem from "./pages/AddProblem";
import Leaderboard from "./pages/Leaderboard";
import Profile from "./pages/Profile";


function App() {

  return (
    <AuthProvider>

      <BrowserRouter>
        <Navbar />
        <ToastContainer />
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/log-in" element={<Login />} />
          <Route path="/register" element={<CreateAccount />} />
          <Route path="/problems/all" element={<Problems/>}/>
          <Route path="/problems/add" element={<AddProblem/>}/>
          <Route path="/problems/:id" element={<SingleProblem />} />
          <Route path="/leaderboard" element={<Leaderboard/>} />
          <Route path="/profile" element={<Profile />} />
        </Routes>
        <Footer />
      </BrowserRouter>

    </AuthProvider>
  )
}

export default App
