import './style.css';
import { Container, Carousel, Row, Col } from 'react-bootstrap';
import {Heading, Text} from "@chakra-ui/react";
import Image from "react-bootstrap/Image";

function Home() {
    return (
        <>
            <Container className="main-container">
                <Row className="align-items-center">
                    <Col md={4} className="text-center">
                        <Image src="лого7.png" className="main-logo animated-logo" />
                    </Col>
                    <Col md={8}>
                        <Heading className="head">
                            ID-CUBE.СОРЕВНОВАНИЯ
                        </Heading>
                        <Text className="mainText">
                            Мы — команда, объединяющая студентов, преподавателей и энтузиастов в
                            области робототехники. Нашей целью является развитие инноваций, практических
                            навыков и инженерного мышления через изучение передовых технологий и создание уникальных проектов.
                        </Text>
                    </Col>
                </Row>
                <Carousel data-bs-theme="dark" className="carousel-wrapper">
                    <Carousel.Item>
                        <div className="carousel-item-wrapper">
                            <img
                                className="carousel-image"
                                src="/1.jpg"
                                alt="First slide"
                            />
                        </div>
                    </Carousel.Item>
                    <Carousel.Item>
                        <div className="carousel-item-wrapper">
                            <img
                                className="carousel-image"
                                src="/2.jpg"
                                alt="Second slide"
                            />
                        </div>
                    </Carousel.Item>
                    <Carousel.Item>
                        <div className="carousel-item-wrapper">
                            <img
                                className="carousel-image"
                                src="/3.jpg"
                                alt="Third slide"
                            />
                        </div>
                    </Carousel.Item>
                </Carousel>
            </Container>
        </>
    );
}

export default Home;
