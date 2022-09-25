import { BrowserRouter, Route, Routes } from 'react-router-dom';

import 'bootstrap/dist/css/bootstrap.min.css';

import ToolBar from './ToolBar/ToolBar';
import Login from './Login/Login';
import Home from './Home/Home';
import Results from './Results/Results';
import Report from './Report/Report';
import About from './About/About';
import UploadAPK from './Upload/UploadAPK';
import SelectAlgorithms from './Upload/SelectAlgorithms';
import AdditionalUploads from './Upload/AdditionalUploads';
import UploadSummary from './Upload/UploadSummary';
import { GoogleOAuthProvider } from '@react-oauth/google';
const clientID = '503245552032-9c1vsa0d7uu5r1ujcmp8fdqmsj73v1oh.apps.googleusercontent.com';

function App() {

    return (
        <GoogleOAuthProvider clientId={clientID}> 
        <BrowserRouter>
            <ToolBar />

            <Routes>
                <Route path="" element={<Home />}></Route>
                <Route path="/login" element={<Login />}></Route>
                <Route path="/about" element={<About />}></Route>
                <Route path="/results" element={<Results />}></Route>
                <Route path="/report" element={<Report />}></Route>
                <Route path="/upload" element={<UploadAPK />}></Route>
                <Route path="/upload/selectalgorithm" element={<SelectAlgorithms />}></Route>
                <Route path="/upload/additionaluploads" element={<AdditionalUploads />}></Route>
                <Route path="/upload/summary" element={<UploadSummary />}></Route>
            </Routes>
        </BrowserRouter>
        </GoogleOAuthProvider>
    );
}


export default App;
