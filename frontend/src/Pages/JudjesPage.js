import { Container } from "react-bootstrap";
import Navbar from "react-bootstrap/Navbar";
import Image from "react-bootstrap/Image";
import Offcanvas from "react-bootstrap/Offcanvas";
import Nav from "react-bootstrap/Nav";
import React, { useState } from "react";
import TableTests from "./TableTests";
import TableJudjes from "./Components/TableJudjes";

const JudjesPage = () => {
    const expand = false; // Укажите нужный размер, если хотите, чтобы Offcanvas работал для всех размеров
    const [activeTable, setActiveTable] = useState("comp"); // Состояние для выбора таблицы
    const [selectedCompetition, setSelectedCompetition] = useState(null); // Состояние для выбранного соревнования

    const renderTable = () => {
        // Возвращаем нужный компонент на основе состояния
        switch (activeTable) {
            case "comp":
                return <TableJudjes setSelectedCompetition={setSelectedCompetition} />;
            case "tests":
                return <TableTests competition={selectedCompetition} />;
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
                                            onClick={() => setActiveTable("tests")}
                                        >
                                            Список испытаний
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
                {renderTable()}
                {selectedCompetition? (
                    <div>
                        <h3>Выбрано</h3>
                        <h2>{selectedCompetition.name}</h2>
                        <p>{selectedCompetition.description}</p>
                        <p>Дата начала регистрации: {selectedCompetition.start_registration}</p>
                        <p>Дата конца регистрации: {selectedCompetition.end_registration}</p>
                    </div>

                ) : (null)
                }
            </Container>
        </>
    );
};

export default JudjesPage;