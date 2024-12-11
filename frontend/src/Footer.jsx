import React from "react";
import './style.css'
import {Col, Row} from 'react-bootstrap'
const Footer = () => {
    return (
        <div className="bg-footer">
            <Row>
                <Col>
                    © 2024 КТК - Клуб Технической Компетенции. Все права защищены.
                </Col>
                <Col>


                    Контакты:
                    Адрес: г. Москва, ул. Технологий, д. 10
                    Телефон: +7 (495) 123-45-67
                    Эл. почта: info@ktk-robotics.ru

                </Col>

                <Col>
                    Партнеры:

                    Университет Инноваций
                    Научный центр "Технополис"
                    РобоЛига России

                    "КТК вдохновляет, обучает и объединяет будущее робототехники!"
                </Col>
            </Row>
        </div>
    )
};

export default Footer;