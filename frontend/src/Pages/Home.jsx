import './style.css';
import { Container, Carousel, Row, Col } from 'react-bootstrap';
import { Heading, Text } from '@chakra-ui/react';
import Image from 'react-bootstrap/Image';
import { useEffect } from 'react';

function Home() {
    // Функция для отслеживания появления элементов на экране
    const handleVisibilityChange = (entries, observer) => {
        entries.forEach((entry) => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
                observer.unobserve(entry.target);  // Останавливаем наблюдение после первого появления
            }
        });
    };

    useEffect(() => {
        const observer = new IntersectionObserver(handleVisibilityChange, {
            threshold: 0.5,  // элемент будет отслеживаться, когда 50% его видимой части будет в области просмотра
            rootMargin: '0px 0px -100px 0px', // делаем так, чтобы элемент начинал появляться немного раньше
        });

        // Наблюдаем за каждым элементом, которому необходимо добавить анимацию
        const elementsToAnimate = document.querySelectorAll('.hidden');
        elementsToAnimate.forEach((element) => observer.observe(element));

        return () => observer.disconnect(); // Очищаем observer при удалении компонента
    }, []);

    return (
        <>
            <Container className="main-container">
                <Row className="align-items-center">
                    <Col md={4} className="text-center">
                        <Image src="лого7.png" className="main-logo animated-logo hidden" />
                    </Col>
                    <Col md={8}>
                        <Heading className="head hidden">ID-CUBE.СОРЕВНОВАНИЯ</Heading>
                        <Text className="mainText hidden">
                            Мы — команда, объединяющая студентов, преподавателей и энтузиастов в области робототехники. Нашей целью является развитие инноваций, практических навыков и инженерного мышления через изучение передовых технологий и создание уникальных проектов.
                        </Text>
                    </Col>
                </Row>
                <Carousel data-bs-theme="dark" className="carousel-wrapper">
                    <Carousel.Item>
                        <div className="carousel-item-wrapper">
                            <img className="carousel-image hidden" src="/1.jpg" alt="First slide" />
                        </div>
                    </Carousel.Item>
                    <Carousel.Item>
                        <div className="carousel-item-wrapper">
                            <img className="carousel-image hidden" src="/2.jpg" alt="Second slide" />
                        </div>
                    </Carousel.Item>
                    <Carousel.Item>
                        <div className="carousel-item-wrapper">
                            <img className="carousel-image hidden" src="/3.jpg" alt="Third slide" />
                        </div>
                    </Carousel.Item>
                </Carousel>
            </Container>
        </>
    );
}

export default Home;
