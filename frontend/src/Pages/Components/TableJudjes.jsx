import React, { useEffect, useState } from "react";
import { Container, Table } from "react-bootstrap";
import axiosConfig from "./AxiosConfig";

const formatDate = (dateString) => {
    if (!dateString) return "—";
    const date = new Date(dateString);
    return date.toLocaleString("ru-RU", {
        year: "numeric",
        month: "long",
        day: "numeric",
        hour: "2-digit",
        minute: "2-digit",
    });
};

const TableJudjes = ({ setSelectedCompetition }) => {
    const [competition, setCompetition] = useState([]);

    useEffect(() => {
        const fetchCompetitions = async () => {
            try {
                const response = await axiosConfig.get("/v0/competition/");
                setCompetition(response.data);
            } catch (error) {
                console.error("Ошибка при получении данных соревнований:", error);
            }
        };

        fetchCompetitions();
    }, []);

    return (
        <Container className="main-content">
            <h2 className="text-center mb-4" style={{ fontWeight: "bold" }}>
                Список соревнований
            </h2>
            <Table responsive="sm" bordered hover>
                <thead>
                <tr>
                    <th>#</th>
                    <th>Название</th>
                    <th>Описание</th>
                    <th>Начало регистрации</th>
                    <th>Конец регистрации</th>
                </tr>
                </thead>
                <tbody>
                {competition.length > 0 ? (
                    competition.map((comp, index) => (
                        <tr
                            key={comp.id || index}
                            style={{ cursor: "pointer" }}
                            onClick={() => setSelectedCompetition(comp)}
                        >
                            <td>{index + 1}</td>
                            <td>{comp.name || "—"}</td>
                            <td>{comp.description || "—"}</td>
                            <td>{formatDate(comp.start_registration)}</td>
                            <td>{formatDate(comp.end_registration)}</td>
                        </tr>
                    ))
                ) : (
                    <tr>
                        <td colSpan="5" className="text-center">
                            Нет доступных данных
                        </td>
                    </tr>
                )}
                </tbody>
            </Table>
        </Container>
    );
};

export default TableJudjes;
