import os
import django
import random
from datetime import timedelta
from django.utils.timezone import now

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'your_project.settings')
django.setup()

from users.models import User
from competitions.models import Competition, CompetitionJudges, Criteria, Experiment, Score, Teams


# Создание пользователей (судей)
def create_judges():
    judges = []
    for i in range(5):
        username = f'judge_{i + 1}'
        email = f'judge_{i + 1}@example.com'  # Уникальный email
        judge, created = User.objects.get_or_create(
            username=username,
            defaults={'email': email, 'password': 'password'}
        )
        judges.append(judge)
    return judges


# Создание соревнований
def create_competitions():
    competitions = []
    for i in range(1, 4):
        competition, created = Competition.objects.get_or_create(
            name=f"Competition {i}",
            defaults={
                'description': f"Description for Competition {i}",
                'start_registration': now() - timedelta(days=5),
                'end_registration': now() + timedelta(days=5),
            },
        )
        competitions.append(competition)
    return competitions


# Создание команд
def create_teams(competitions):
    teams = []
    for i in range(1, 11):
        competition = random.choice(competitions)
        team, created = Teams.objects.get_or_create(
            name=f"Team {i}",
            defaults={
                'robot_name': f"Robot {i}",
                'city': f"City {i}",
                'institution': f"Institution {i}",
                'members': "Member1, Member2",
                'leader': f"Leader {i}",
                'captain': User.objects.first(),
                'contact_phone': f"+70000000{i}",
                'status': 'approved',
                'competition': competition,
            },
        )
        teams.append(team)
    return teams


# Создание критериев
def create_criteria(competitions):
    criteria_list = []
    for competition in competitions:
        for i in range(1, 6):
            criteria, created = Criteria.objects.get_or_create(
                name=f"Criteria {i} for {competition.name}",
                defaults={
                    'weight': random.uniform(1, 5),
                    'competitions': competition,
                },
            )
            criteria_list.append(criteria)
    return criteria_list


# Создание испытаний
def create_experiments(competitions):
    experiments = []
    for competition in competitions:
        for i in range(1, 4):
            experiment, created = Experiment.objects.get_or_create(
                name=f"Experiment {i} for {competition.name}",
                defaults={'competition': competition},
            )
            experiments.append(experiment)
    return experiments


# Создание баллов
def create_scores(competitions, teams, judges, criteria_list, experiments):
    for competition in competitions:
        competition_teams = [team for team in teams if team.competition == competition]
        competition_criteria = [criteria for criteria in criteria_list if criteria.competitions == competition]
        competition_experiments = [experiment for experiment in experiments if experiment.competition == competition]

        for team in competition_teams:
            for judge in judges:
                for criteria in competition_criteria:
                    for experiment in competition_experiments:
                        Score.objects.create(
                            competition=competition,
                            judge_user=judge,
                            criteria=criteria,
                            score=random.uniform(50, 100),
                            experiment=experiment,
                            team=team,
                        )


# Основная функция
def main():
    judges = create_judges()
    competitions = create_competitions()
    teams = create_teams(competitions)
    criteria_list = create_criteria(competitions)
    experiments = create_experiments(competitions)
    create_scores(competitions, teams, judges, criteria_list, experiments)
    print("Test data successfully created!")


if __name__ == "__main__":
    main()
