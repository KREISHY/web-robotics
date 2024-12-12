import React, { useState } from 'react';
import { Container, Card, Nav, Form, Button } from "react-bootstrap";
import axiosConfig from "./Components/AxiosConfig"; // Ваш axiosConfig для отправки данных
import { useNavigate } from 'react-router-dom'; // Для перенаправления пользователя

function LoginPage() {
    const [role, setRole] = useState("user");
    const [user, setUser] = useState({
        email: "",
        username: "",
        password: "",
        last_name: "",
        first_name: "",
        patronymic: ""
    });
    const [error, setError] = useState(""); // Стейт для хранения ошибок
    const navigate = useNavigate(); // Для редиректа после успешной аутентификации

    const handleChange = (e) => {
        const { name, value } = e.target;
        setUser({
            ...user,
            [name]: value
        });
    };

    const handleSelectRole = (rol) => {
        setRole(rol);
    };

    const handleSubmit = async () => {
        let payload = {};
        if (role === "user") {
            payload = {
                email: user.email,
                password: user.password
            };
        } else if (role === "referi") {
            payload = {
                username: user.username,
                password: user.password
            };
        } else if (role === "registerUser") {
            payload = {
                email: user.email,
                username: user.username,
                password: user.password,
                first_name: user.first_name,
                last_name: user.last_name,
                patronymic: user.patronymic
            };
        }

        try {
            let response;
            if (role === "registerUser") {
                response = await axiosConfig.post('/users/register/', payload);
                console.log('User registered:', response);
                navigate("/login"); // Перенаправление на страницу входа после регистрации
            } else {
                const endpoint = role === "user" ? '/users/login-email/' : '/users/login-username/';
                response = await axiosConfig.post(endpoint, payload);
                console.log('User logged in:', response);

                // Сохраняем токен и информацию о текущем пользователе в localStorage
                localStorage.setItem('currentUser', JSON.stringify({ loggedIn: true, user: response.data }));

                // Перенаправляем на страницу после успешного входа
                navigate("/table-teams"); // Редирект на страницу с контентом
            }
        } catch (error) {
            console.error('Error:', error);
            setError('Ошибка аутентификации. Пожалуйста, проверьте свои данные.');
        }
    };

    return (
        <div>
            <Container className="d-flex justify-content-center">
                <Card style={{ maxWidth: "900px", width: "100%" }}>
                    <Card.Header>
                        <Nav variant="pills" defaultActiveKey="#first" className="justify-content-center">
                            <Nav.Item>
                                <Nav.Link onClick={() => handleSelectRole("user")}>Новичок</Nav.Link>
                            </Nav.Item>
                            <Nav.Item>
                                <Nav.Link onClick={() => handleSelectRole("referi")}>Смешарик</Nav.Link>
                            </Nav.Item>
                        </Nav>
                    </Card.Header>
                    <Card.Body>
                        <Card.Title>{role === "registerUser" ? "Регистрация" : "Вход"}</Card.Title>

                        {error && <div className="text-danger">{error}</div>} {/* Выводим ошибку, если она есть */}

                        {/* Форма для роли "user" */}
                        {role === "user" ? (
                            <Card.Text>
                                <Nav.Link className="text-primary" onClick={() => handleSelectRole("registerUser")}>Регистрация</Nav.Link>
                                <Form.Group className="mb-3">
                                    <Form.Label>Email адрес</Form.Label>
                                    <Form.Control
                                        type="email"
                                        name="email"
                                        value={user.email}
                                        onChange={handleChange}
                                        placeholder="kotik@example.com"
                                    />
                                    <Form.Label htmlFor="inputPassword5">Пароль</Form.Label>
                                    <Form.Control
                                        type="password"
                                        name="password"
                                        value={user.password}
                                        onChange={handleChange}
                                        id="inputPassword5"
                                    />
                                </Form.Group>
                            </Card.Text>
                        ) : role === "referi" ? (
                            <Card.Text>
                                <Form.Group className="mb-3">
                                    <Form.Label>Имя пользователя</Form.Label>
                                    <Form.Control
                                        type="text"
                                        name="username"
                                        value={user.username}
                                        onChange={handleChange}
                                        placeholder="Пример"
                                    />
                                    <Form.Label htmlFor="inputPassword4">Пароль</Form.Label>
                                    <Form.Control
                                        type="password"
                                        name="password"
                                        value={user.password}
                                        onChange={handleChange}
                                        id="inputPassword4"
                                    />
                                </Form.Group>
                            </Card.Text>
                        ) : role === "registerUser" ? (
                            <Card.Text>
                                <Form.Group className="mb-3">
                                    <Form.Label>Имя пользователя</Form.Label>
                                    <Form.Control
                                        type="text"
                                        name="username"
                                        value={user.username}
                                        onChange={handleChange}
                                        placeholder="Пример"
                                    />
                                    <Form.Label>Имя</Form.Label>
                                    <Form.Control
                                        type="text"
                                        name="first_name"
                                        value={user.first_name}
                                        onChange={handleChange}
                                        placeholder="Имя"
                                    />
                                    <Form.Label>Фамилия</Form.Label>
                                    <Form.Control
                                        type="text"
                                        name="last_name"
                                        value={user.last_name}
                                        onChange={handleChange}
                                        placeholder="Фамилия"
                                    />
                                    <Form.Label>Отчество</Form.Label>
                                    <Form.Control
                                        type="text"
                                        name="patronymic"
                                        value={user.patronymic}
                                        onChange={handleChange}
                                        placeholder="Отчество"
                                    />
                                    <Form.Label>Почта</Form.Label>
                                    <Form.Control
                                        type="email"
                                        name="email"
                                        value={user.email}
                                        onChange={handleChange}
                                        placeholder="kotik@example.com"
                                    />
                                    <Form.Label htmlFor="registerPassword">Пароль</Form.Label>
                                    <Form.Control
                                        type="password"
                                        name="password"
                                        value={user.password}
                                        onChange={handleChange}
                                        id="registerPassword"
                                    />
                                    <Form.Text id="passwordHelpBlock" muted>
                                        Your password must be 8-20 characters long, contain letters and numbers,
                                        and must not contain spaces, special characters, or emoji.
                                    </Form.Text>
                                </Form.Group>
                            </Card.Text>
                        ) : null}

                        <Button variant="primary" onClick={handleSubmit}>
                            {role === 'registerUser' ? 'Зарегистрироваться' : 'Войти'}
                        </Button>
                    </Card.Body>
                </Card>
            </Container>
        </div>
    );
}

export default LoginPage;
