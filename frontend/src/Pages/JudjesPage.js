import {Button, Container} from "react-bootstrap";
import Navbar from "react-bootstrap/Navbar";
import Image from "react-bootstrap/Image";
import Offcanvas from "react-bootstrap/Offcanvas";
import Nav from "react-bootstrap/Nav";
import React, { useState } from "react";
import TableTeams from "./Components/TableTeams";
import TableJudjes from "./Components/TableJudjes";
import {NavLink} from "react-router-dom";
import axiosConfig from "./Components/AxiosConfig";

const JudjesPage = () => {
    const expand = false; // Укажите нужный размер, если хотите, чтобы Offcanvas работал для всех размеров
    const [activeTable, setActiveTable] = useState("comp"); // Состояние для выбора таблицы
    const [selectedCompetition, setSelectedCompetition] = useState(null); // Состояние для выбранного соревнования
    const handleExport = async (comp) => {
        try{
            let response = await axiosConfig.get(`/v0/export-csv/${comp}/by-experiment/`);
        }catch(err){
            console.log(err);
        }
    }
    const renderTable = () => {
        console.log(selectedCompetition?.id);
        // Возвращаем нужный компонент на основе состояния
        switch (activeTable) {
            case "comp":
                return <TableJudjes setSelectedCompetition={setSelectedCompetition} />;
            case "teams":
                return <TableTeams selectedCompetition={selectedCompetition.id} />;
            default:
                return null;
        }
    };

    return (
        <>
            <Navbar key={expand} expand={expand} className="bg-primary navbar-dark mb-3">
                <Container fluid>
                    {/* Контейнер для кнопки открытия меню */}
                    <div className="d-flex align-items-center">
                        {/* Кнопка для выдвигающегося меню */}
                        <Navbar.Toggle aria-controls={`offcanvasNavbar-expand-${expand}`} />
                    </div>

                    {/* Логотип */}
                    <Navbar.Brand className="ms-auto" href="#">
                        <Image src="/logo.png" style={{ width: '300px', height: '90px' }} />
                    </Navbar.Brand>

                    {/* Offcanvas меню */}
                    <Navbar.Offcanvas
                        id={`offcanvasNavbar-expand-${expand}`}
                        aria-labelledby={`offcanvasNavbarLabel-expand-${expand}`}
                        placement="start" // Меняем расположение на "слева"
                    >
                        <Offcanvas.Header closeButton>
                            <Offcanvas.Title id={`offcanvasNavbarLabel-expand-${expand}`}>
                                {selectedCompetition ? selectedCompetition.name : "Меню"}
                            </Offcanvas.Title>
                        </Offcanvas.Header>
                        <Offcanvas.Body>
                            <Nav className="flex-column">
                                {selectedCompetition ? (
                                    <>
                                        <Nav.Link
                                            style={{ fontSize: '24px', padding: '10px 0', cursor: 'pointer' }}
                                            onClick={() => setActiveTable("teams")}
                                        >
                                            Список команд
                                        </Nav.Link>
                                        <Nav.Link
                                            style={{ fontSize: '24px', padding: '10px 0', cursor: 'pointer' }}
                                            onClick={() => setSelectedCompetition(null)}
                                        >
                                            Вернуться к выбору соревнования
                                        </Nav.Link>
                                    </>
                                ) : (
                                    <Nav.Link
                                        style={{ fontSize: '24px', padding: '10px 0', cursor: 'pointer' }}
                                        onClick={() => setActiveTable("comp")}
                                    >
                                        Список соревнований
                                    </Nav.Link>
                                )}
                            </Nav>
                        </Offcanvas.Body>
                    </Navbar.Offcanvas>
                </Container>

            </Navbar>

            {/* Отображение выбранной таблицы */}
            <Container>
                {selectedCompetition? (
                    <div>
                        <h3>Выбрано</h3>
                        <h2>{selectedCompetition.name}</h2>
                        <p>{selectedCompetition.description}</p>
                        <p>Дата начала регистрации: {selectedCompetition.start_registration}</p>
                        <p>Дата конца регистрации: {selectedCompetition.end_registration}</p>
                        <a href={`http://localhost:8000/api/v0/export-csv/${selectedCompetition.id}/by-experiment/`}>Экспортировать .scv</a>
                    </div>

                ) : (null)
                }
                {renderTable()}
                <NavLink to={'/'} >На главную</NavLink>

            </Container>
        </>
    );
};

export default JudjesPage;
