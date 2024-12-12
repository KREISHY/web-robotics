import React, { useEffect, useState } from "react";
import { useNavigate } from 'react-router-dom';
import { Container, Table } from "react-bootstrap";
import axiosConfig from "./AxiosConfig";

const TableTeams = ({ selectedCompetition }) => {
    const [teams, setTeams] = useState([]);
    const navigate = useNavigate();

    useEffect(() => {
        const fetchTeams = async () => {
            try {
                const response = await axiosConfig.get("/v0/teams/");
                setTeams(response.data);
            } catch (error) {
                console.error("Ошибка при получении данных команд:", error);
            }
        };

        fetchTeams();
    }, []);

    const filteredTeams = teams.filter(
        (team) => String(team.competition_id) === String(selectedCompetition)
    );

    const handleTeam = (teamName) => {
        localStorage.setItem('teamName', teamName);
        navigate('/table-tests');
    }

    return (
        <Container className="main-content">
            <h2 className="text-center mb-4" style={{ fontWeight: "bold" }}>
                Список команд
            </h2>
            <Table responsive="sm" bordered hover>
                <thead>
                <tr>
                    <th>#</th>
                    <th>Название</th>
                    <th>Институт</th>
                    <th>Город</th>
                    <th>Название Робота</th>
                </tr>
                </thead>
                <tbody>
                {filteredTeams.length > 0 ? (
                    filteredTeams.map((team, index) => (
                        <tr
                            key={team.id || index}
                            style={{ cursor: "pointer" }}
                            onClick={() => handleTeam(team.name)} // Обрабатываем клик
                        >
                            <td>{index + 1}</td>
                            <td>{team.name || "—"}</td>
                            <td>{team.institution || "—"}</td>
                            <td>{team.city || "—"}</td>
                            <td>{team.robot_name || "—"}</td>
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

export default TableTeams;
