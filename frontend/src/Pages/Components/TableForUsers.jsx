import React, { useEffect, useState } from "react";
import { Container, Table } from "react-bootstrap";
import axiosConfig from "./AxiosConfig";
import { NavLink, useParams } from "react-router-dom";

// Функция для преобразования даты в читаемый формат
const formatDate = (dateString) => {
    if (!dateString) return "—"; // Если дата отсутствует
    const date = new Date(dateString);
    return date.toLocaleString("ru-RU", {
        year: "numeric",
        month: "long",
        day: "numeric",
        hour: "2-digit",
        minute: "2-digit",
    });
};

const TableForUsers = () => {
    const { competitionId } = useParams(); // Получаем competitionId из пути
    const [teams, setTeams] = useState([]);
    const [criterias, setCriterias] = useState([]);
    const [scores, setScores] = useState([]);

    useEffect(() => {
        // Получение данных о командах
        const fetchTeams = async () => {
            try {
                const response = await axiosConfig.get("/v0/teams/");
                setTeams(response.data);
            } catch (error) {
                console.error("Ошибка при получении данных команд:", error);
            }
        };

        // Получение данных о критериях
        const fetchCriteria = async () => {
            try {
                const response = await axiosConfig.get(`/v0/criteria/?competition_id=${competitionId}`);
                setCriterias(response.data.results); // предполагаем, что ответы приходят в results
            } catch (error) {
                console.error("Ошибка при получении данных критериев:", error);
            }
        };

        // Получение баллов по каждой команде
        const fetchScores = async () => {
            try {
                const response = await axiosConfig.get(`/v0/score/?competition_id=${competitionId}`);
                setScores(response.data);
            } catch (error) {
                console.error("Ошибка при получении данных баллов:", error);
            }
        };

        fetchTeams();
        fetchCriteria();
        fetchScores();
    }, [competitionId]); // Обновление данных при изменении competitionId

    // Сортировка команд по суммарным баллам
    const calculateTotalScores = (teamId) => {
        const teamScores = scores.filter(score => score.team_id === teamId);
        return teamScores.reduce((total, score) => total + score.score, 0); // Используем score, а не value
    };

    // Фильтрация команд по selectedCompetition
    const filteredTeams = teams.filter((team) => String(team.competition_id) === String(competitionId));

    const sortedTeams = [...filteredTeams].sort((a, b) => calculateTotalScores(b.id) - calculateTotalScores(a.id));

    return (
        <Container className="main-content">
            <h2 className="text-center mb-4" style={{ fontWeight: "bold" }}>
                Оценки команд
            </h2>
            <Table responsive="sm" bordered hover>
                <thead>
                <tr>
                    <th>#</th>
                    <th>Команда</th>
                    {criterias.map((criteria) => (
                        <th key={criteria.id}>{criteria.name}</th>
                    ))}
                    <th>Сумма баллов</th>
                </tr>
                </thead>
                <tbody>
                {sortedTeams.length > 0 ? (
                    sortedTeams.map((team, index) => {
                        // Массив баллов для каждой команды и каждого критерия
                        const teamScores = criterias.map(criteria => {
                            // Ищем балл для этой команды и критерия
                            const score = scores.find(score =>
                                String(score.team_id) === String(team.id) && String(score.criteria_id) === String(criteria.id)
                            );
                            // Логируем баллы для каждого критерия
                            console.log(`Команда: ${team.name}, Критерий: ${criteria.name}, Балл: ${score ? score.score : 0}`);
                            return score ? score.score : 0; // Если балл найден, используем его, иначе 0
                        });

                        const totalScore = teamScores.reduce((total, score) => total + score, 0); // Суммируем баллы для команды

                        return (
                            <tr key={team.id} style={{ cursor: "pointer" }}>
                                <td>{index + 1}</td>
                                <td>{team.name || "—"}</td>
                                {teamScores.map((score, idx) => (
                                    <td key={idx}>{score}</td> // Отображаем баллы по каждому критерию
                                ))}
                                <td>{totalScore}</td>
                            </tr>
                        );
                    })
                ) : (
                    <tr>
                        <td colSpan="5" className="text-center">
                            Нет доступных данных
                        </td>
                    </tr>
                )}
                </tbody>
            </Table>
            <NavLink to={'/'}>На главную</NavLink>
        </Container>
    );
};

export default TableForUsers;
