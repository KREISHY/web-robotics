import React from "react";
import 'bootstrap/dist/css/bootstrap.min.css';
import './style.css';
import { BrowserRouter, Route, Routes, useLocation, NavLink } from 'react-router-dom';
import Home from './Pages/Home';
import LoginPage from './Pages/Profile';
import Footer from './Footer';
import NavbarMain from "./Pages/Components/NavbarMain";
import TableTests from "./Pages/TableTests";
import TableComands from "./Pages/Components/TableComands";
import JudjesPage from "./Pages/JudjesPage";
import TableForUsers from "./Pages/Components/TableForUsers";
function AppContent() {
    const location = useLocation();

    // Список маршрутов, где header не должен отображаться
    const hideHeaderRoutes = ["/judjes-page"];

    return (
        <div className="app-container">
            {/* Показываем Header только если текущий маршрут не находится в списке hideHeaderRoutes */}
            {!hideHeaderRoutes.includes(location.pathname) && <NavbarMain />}

            <div className="main-content">
                <Routes>
                    <Route path="/" element={<Home />} />
                    <Route path="/login" element={<LoginPage />} />
                    <Route path="/table-tests" element={<TableTests />} />
                    <Route path="/table-comp" element={<TableComands />} />
                    <Route path="/judjes-page" element={<JudjesPage />} />
                    {/* Изменили путь для передачи competitionId */}
                    <Route path="/user-table-page/:competitionId" element={<TableForUsers />} />
                </Routes>
            </div>

            <Footer />
        </div>
    );
}

function App() {
    return (
        <BrowserRouter>
            <AppContent />
        </BrowserRouter>
    );
}

export default App;
