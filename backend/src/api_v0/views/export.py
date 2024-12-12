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
        """Экспорт оценок по испытанию."""
        try:
            experiment = Experiment.objects.get(pk=pk)
        except Experiment.DoesNotExist:
            return Response({'error': 'Experiment not found'}, status=404)

        scores = Score.objects.filter(experiment=experiment).order_by('-score')
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="scores_experiment_{experiment.id}.csv"'
        writer = csv.writer(response, delimiter=';')

        writer.writerow(['Team', 'Judge', 'Criteria', 'Score', 'Experiment'])
        for score in scores:
            team = score.team  # Прямое обращение к объекту команды
            writer.writerow([
                team.name if team else "Unknown",  # Проверка, существует ли команда
                score.judge_user.username,
                score.criteria.name,
                round(score.score, 1),  # Округление до одной десятичной
                score.experiment.name,
            ])
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

        # Заголовки CSV: Эксперимент, Критерий, Команда и все судьи
        header = ['Experiment', 'Criteria', 'Team'] + [f'{judge}' for judge in judges]
        writer.writerow(header)

        # Группируем оценки по эксперименту и критерию
        experiments = Experiment.objects.filter(competition=competition)

        for experiment in experiments:
            for criterion in Criteria.objects.all():
                row = [experiment.name, criterion.name, experiment.competition.teams.filter(
                    pk=competition.id).first().name if experiment.competition.teams.exists() else "Unknown"]

                # Заполняем баллами для каждого судьи
                row_with_scores = row.copy()  # Копируем начало строки, чтобы не модифицировать оригинал
                all_na = True  # Флаг для проверки, есть ли хотя бы один балл, отличный от "N/A"

                for judge in judges:
                    score = scores.filter(experiment=experiment, criteria=criterion, judge_user__username=judge).first()
                    if score:
                        row_with_scores.append(round(score.score, 1))  # Если есть оценка, добавляем ее
                        all_na = False  # Если есть оценка, флаг меняем на False
                    else:
                        row_with_scores.append("N/A")  # Если оценки нет, пишем "N/A"

                # Если в строке есть хотя бы один действительный балл, записываем строку, иначе пропускаем
                if not all_na:
                    writer.writerow(row_with_scores)

        return response



