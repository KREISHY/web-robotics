from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from django.http import HttpResponse
import csv
from openpyxl import Workbook
from competitions.models import Score, Experiment, Competition, Criteria, User


class ExportCSVScoresViewSet(ViewSet):
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['get'], url_path='by-experiment')
    def export_by_experiment(self, request, pk=None):
        """Экспорт оценок по испытанию с каждым судьей в отдельном столбце, исключая строки с N/A, если все оценки судей N/A."""
        try:
            experiment = Experiment.objects.get(pk=pk)
        except Experiment.DoesNotExist:
            return Response({'error': 'Experiment not found'}, status=404)

        # Получаем все оценки для данного эксперимента
        scores = Score.objects.filter(experiment=experiment).select_related('judge_user', 'criteria')

        # Собираем список уникальных судей
        judges = scores.values_list('judge_user__username', flat=True).distinct()

        # Подготовка ответа CSV
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="scores_experiment_{experiment.id}.csv"'
        writer = csv.writer(response, delimiter=';')

        # Заголовки CSV: Эксперимент, Критерий, Команда и все судьи + сумма
        header = ['Experiment', 'Criteria', 'Team'] + [f'{judge}' for judge in judges] + ['Total']
        writer.writerow(header)

        # Получаем все команды для данного эксперимента
        teams = experiment.competition.teams.all()

        # Для каждой команды и критерия пишем строку
        for team in teams:
            for criterion in Criteria.objects.all():
                row = [experiment.name, criterion.name, team.name]

                row_with_scores = row.copy()  # Копируем начало строки, чтобы не модифицировать оригинал
                total_score = 0  # Переменная для подсчета суммы
                all_na = True  # Флаг для проверки, есть ли хотя бы один балл, отличный от "N/A"

                # Заполняем баллами для каждого судьи
                for judge in judges:
                    score = scores.filter(experiment=experiment, criteria=criterion, judge_user__username=judge,
                                          team=team).first()
                    if score:
                        row_with_scores.append(round(score.score, 1))  # Если есть оценка, добавляем ее
                        total_score += score.score  # Добавляем к общей сумме
                        all_na = False  # Если есть оценка, флаг меняем на False
                    else:
                        row_with_scores.append("N/A")  # Если оценки нет, пишем "N/A"

                # Если в строке есть хотя бы один действительный балл, записываем строку, иначе пропускаем
                if not all_na:
                    row_with_scores.append(round(total_score, 1))  # Добавляем сумму
                    writer.writerow(row_with_scores)

        return response

    @action(detail=True, methods=['get'], url_path='by-team')
    def export_by_team(self, request, pk=None):
        """Экспорт оценок по команде в CSV с каждым судьей в отдельном столбце, исключая строки с N/A, если все оценки судей N/A."""
        try:
            competition = Competition.objects.get(pk=pk)
        except Competition.DoesNotExist:
            return Response({'error': 'Competition not found'}, status=404)

        # Получаем все оценки для данной конкуренции
        scores = Score.objects.filter(competition=competition).select_related('judge_user', 'experiment', 'criteria')

        # Собираем список уникальных судей
        judges = scores.values_list('judge_user__username', flat=True).distinct()

        # Подготовка ответа CSV
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="scores_team_{competition.id}.csv"'
        writer = csv.writer(response, delimiter=';')

        # Заголовки CSV: Эксперимент, Критерий, Команда, все судьи и сумма
        header = ['Experiment', 'Criteria', 'Team'] + [f'{judge}' for judge in judges] + ['Total']
        writer.writerow(header)

        # Группируем оценки по эксперименту и критерию
        experiments = Experiment.objects.filter(competition=competition)

        for experiment in experiments:
            for criterion in Criteria.objects.all():
                row = [experiment.name, criterion.name, experiment.competition.teams.filter(
                    pk=competition.id).first().name if experiment.competition.teams.exists() else "Unknown"]

                # Заполняем баллами для каждого судьи
                row_with_scores = row.copy()  # Копируем начало строки, чтобы не модифицировать оригинал
                total_score = 0  # Переменная для подсчета суммы
                all_na = True  # Флаг для проверки, есть ли хотя бы один балл, отличный от "N/A"

                # Заполняем баллами для каждого судьи
                for judge in judges:
                    score = scores.filter(experiment=experiment, criteria=criterion, judge_user__username=judge).first()
                    if score:
                        row_with_scores.append(round(score.score, 1))  # Если есть оценка, добавляем ее
                        total_score += score.score  # Добавляем к общей сумме
                        all_na = False  # Если есть оценка, флаг меняем на False
                    else:
                        row_with_scores.append("N/A")  # Если оценки нет, пишем "N/A"

                # Если в строке есть хотя бы один действительный балл, записываем строку, иначе пропускаем
                if not all_na:
                    row_with_scores.append(round(total_score, 1))  # Добавляем сумму
                    writer.writerow(row_with_scores)

        return response

    @action(detail=True, methods=['get'], url_path='by-competition')
    def export_by_competition(self, request, pk=None):
        """Экспорт оценок по конкуренции в CSV с каждым судьей в отдельном столбце и суммой по каждому критерию для каждой команды."""
        try:
            competition = Competition.objects.get(pk=pk)
        except Competition.DoesNotExist:
            return Response({'error': 'Competition not found'}, status=404)

        # Получаем все оценки для данной конкуренции
        scores = Score.objects.filter(competition=competition).select_related('judge_user', 'experiment', 'criteria',
                                                                              'team')

        # Собираем список уникальных судей
        judges = scores.values_list('judge_user__username', flat=True).distinct()

        # Подготовка ответа CSV
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="scores_competition_{competition.id}.csv"'
        writer = csv.writer(response, delimiter=';')

        # Заголовки CSV: Эксперимент, Критерий, Команда, все судьи и сумма
        header = ['Team', 'Experiment', 'Criteria'] + [f'{judge}' for judge in judges] + ['Total']
        writer.writerow(header)

        # Группируем оценки по команде, эксперименту и критерию
        teams = competition.teams.all()

        for team in teams:
            # Для каждой команды выводим оценки по каждому эксперименту и критерию
            for experiment in Experiment.objects.filter(competition=competition):
                for criterion in Criteria.objects.all():
                    row = [team.name, experiment.name, criterion.name]

                    # Заполняем баллами для каждого судьи
                    row_with_scores = row.copy()  # Копируем начало строки, чтобы не модифицировать оригинал
                    total_score = 0  # Переменная для подсчета суммы
                    all_na = True  # Флаг для проверки, есть ли хотя бы один балл, отличный от "N/A"

                    # Заполняем баллами для каждого судьи
                    for judge in judges:
                        score = scores.filter(experiment=experiment, criteria=criterion, judge_user__username=judge,
                                              team=team).first()
                        if score:
                            row_with_scores.append(round(score.score, 1))  # Если есть оценка, добавляем ее
                            total_score += score.score  # Добавляем к общей сумме
                            all_na = False  # Если есть оценка, флаг меняем на False
                        else:
                            row_with_scores.append("N/A")  # Если оценки нет, пишем "N/A"

                    # Если в строке есть хотя бы один действительный балл, записываем строку, иначе пропускаем
                    if not all_na:
                        row_with_scores.append(round(total_score, 1))  # Добавляем сумму
                        writer.writerow(row_with_scores)

        return response

