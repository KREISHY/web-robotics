import React from "react";
import 'bootstrap/dist/css/bootstrap.min.css';
import './style.css';
import { BrowserRouter, Route, Routes } from 'react-router-dom';
import Home from './Pages/Home';
import LoginPage from './Pages/Profile';
import Footer from './Footer';
import NavbarMain from "./Pages/Components/NavbarMain";


function App() {
    return (
        <div className="app-container">

            <div className="main-content">
                <BrowserRouter>
                    <NavbarMain />
                    <Routes>
                        <Route path="/" element={<Home />} />
                        {/* Добавлен маршрут для страницы логина */}
                        <Route path="/login" element={<LoginPage />} />
                    </Routes>
                </BrowserRouter>
            </div>
            <Footer />
        </div>
    );
}

export default App;
