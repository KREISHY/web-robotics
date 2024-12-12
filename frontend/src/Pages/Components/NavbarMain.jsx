import React from 'react';
import Button from 'react-bootstrap/Button';
import Container from 'react-bootstrap/Container';
import Nav from 'react-bootstrap/Nav';
import Navbar from 'react-bootstrap/Navbar';
import Offcanvas from 'react-bootstrap/Offcanvas';
import Image from 'react-bootstrap/Image';
import { useNavigate, NavLink} from 'react-router-dom';
import './style.css';

function NavbarMain() {
    const navigate = useNavigate();

    // Обработчик для перехода на страницу логина
    const handleLogin = () => {
        navigate('/login');
    };

    return (
        <>
            {[false].map((expand) => (
                <Navbar key={expand} expand={expand} className="bg-primary navbar-dark mb-3" >
                    <Container fluid>
                        <Navbar.Brand href="#">
                            <Image src="/logo.png" style={{ width: '300px', height: '90px' }} />
                        </Navbar.Brand>

                        {/* Контейнер для выравнивания кнопки входа и меню */}
                        <div className="d-flex align-items-center">
                            {/* Кнопка Вход */}
                            <Button
                                variant="outline-light"
                                className="me-2"
                                onClick={handleLogin} // Вызовем функцию при нажатии на кнопку
                            >
                                Вход
                            </Button>

                            {/* Кнопка для выдвигающегося меню */}
                            <Navbar.Toggle aria-controls={`offcanvasNavbar-expand-${expand}`} />
                        </div>

                        <Navbar.Offcanvas
                            id={`offcanvasNavbar-expand-${expand}`}
                            aria-labelledby={`offcanvasNavbarLabel-expand-${expand}`}
                            placement="end"
                        >
                            <Offcanvas.Header closeButton>
                                <Offcanvas.Title id={`offcanvasNavbarLabel-expand-${expand}`}>
                                    Меню
                                </Offcanvas.Title>
                            </Offcanvas.Header>
                            <Offcanvas.Body>
                                <Nav className="justify-content-end flex-grow-1 pe-3">
                                    <NavLink to='/' style={{ fontSize: '36px' }}>Домой</NavLink>
                                    <NavLink to='/login' style={{ fontSize: '36px' }}>Вход</NavLink>
                                    <NavLink to='/table-comp' style={{ fontSize: '36px' }}>Соревнования</NavLink>
                                    <NavLink to='/contacts' style={{ fontSize: '36px' }}>Контакты</NavLink>
                                </Nav>
                            </Offcanvas.Body>
                        </Navbar.Offcanvas>
                    </Container>
                </Navbar>
            ))}
        </>
    );
}

export default NavbarMain;
