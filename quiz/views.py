from django.contrib.auth.mixins import (LoginRequiredMixin,
                                        PermissionRequiredMixin,
                                        UserPassesTestMixin)
from django.shortcuts import get_object_or_404
from django.db.models import Count, Q
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth import get_user_model
from django.http import JsonResponse

from CultureAnalyzer.constants import ITEMS_ON_PAGE

from quiz.forms import QuizCreateForm
from quiz.models import Quizzes, Results
from quiz.service import get_final_buisness_result
from tutors.models import Questions
from groups.models import Group
from indicators.models import CountryIndicator, INDICATORS_ORDER
from feedbacks.models import Recommendation, Feedback

__all__ = ['QuizzesList', 'CreateQuizView', 'UpdateQuizView',
           'DeleteQuizView', 'QuizDetailView', 'ResultView', 'ResultsListView']


class QuizzesList(LoginRequiredMixin, PermissionRequiredMixin,
                  generic.ListView):
    model = Quizzes
    context_object_name = 'quizzes'
    template_name = 'quiz/quizzes_list.html'
    paginate_by = 2
    permission_required = 'quiz.view_quizzes'

    def get_queryset(self):
        quizzes = Quizzes.objects.all().order_by('title')
        quiz_search = self.request.GET.get("quiz_search")
        if quiz_search:
            return quizzes.filter(
                Q(title__icontains=quiz_search))
        return quizzes

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(QuizzesList, self).get_context_data(
            object_list=None, **kwargs)
        context['search'] = self.request.GET.get("quiz_search")
        return context


class CreateQuizView(LoginRequiredMixin, PermissionRequiredMixin,
                     generic.CreateView):
    model = Quizzes
    template_name = 'quiz/quiz_create.html'
    form_class = QuizCreateForm
    success_url = reverse_lazy('quiz:quizzes-list')
    permission_required = 'quiz.add_quizzes'


class QuizDetailView(LoginRequiredMixin, PermissionRequiredMixin,
                     generic.ListView):
    model = Questions
    context_object_name = 'questions'
    template_name = 'quiz/quiz_detail.html'
    paginate_by = ITEMS_ON_PAGE
    permission_required = 'quiz.view_quizzes'

    def get_queryset(self):
        """
        The search for questions is based on fields 'question_text'.
        Returns the queryset of questions that you want to display.
        """
        questions = Questions.objects.filter(quiz=self.kwargs['pk']).annotate(
            num_answer=Count('answers')).order_by('question_number')
        question_search = self.request.GET.get("question_search")
        if question_search:
            return questions.filter(
                Q(question_text__icontains=question_search))
        return questions

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=None, **kwargs)
        context['search'] = self.request.GET.get("question_search")
        context['quiz'] = get_object_or_404(Quizzes, pk=self.kwargs['pk'])
        return context


class DeleteQuizView(LoginRequiredMixin, PermissionRequiredMixin,
                     generic.DeleteView):
    model = Quizzes
    context_object_name = 'quiz'
    template_name = 'quiz/quiz_delete.html'
    success_url = reverse_lazy('quiz:quizzes-list')
    permission_required = 'quiz.delete_quizzes'


class UpdateQuizView(LoginRequiredMixin, PermissionRequiredMixin,
                     generic.UpdateView):
    model = Quizzes
    form_class = QuizCreateForm
    template_name = 'quiz/quiz_update.html'
    success_url = reverse_lazy('quiz:quizzes-list')
    permission_required = 'quiz.change_quizzes'


class ResultsListView(PermissionRequiredMixin, generic.ListView):
    model = Results
    template_name = 'quiz/result_list.html'
    context_object_name = 'results'
    permission_required = 'quiz.view_results'

    def get_queryset(self):
        results = Results.objects.filter(user=self.kwargs['pk'])
        return results


class ResultView(PermissionRequiredMixin, UserPassesTestMixin,
                 generic.TemplateView):
    template_name = 'quiz/column_chart_from_result.html'
    permission_required = 'quiz.view_results'

    def post(self, request, *args, **kwargs):
        context = self.get_context_data()
        countries_values = {}
        countries_feedback = {}
        countries_names = []
        if request.POST.getlist('select_indicator'):
            self._preparing_results_data(context, countries_values,
                                         countries_names,
                                         countries_feedback)
        context['countries_values'] = countries_values
        context['countries_names'] = countries_names
        context['countries_feedback'] = countries_feedback
        return super().render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.kwargs.get('group', False):
            result = get_final_buisness_result(
                get_object_or_404(Group, id=self.kwargs['pk']))
            context['name'] = self.kwargs['group']
        else:
            result = get_final_buisness_result(get_object_or_404(
                get_user_model(), username=self.kwargs['current_user']),
                                               self.kwargs['pk'])
            context['name'] = self.kwargs['current_user']
        context['result_table'] = [(ind.upper(), result[ind]) for ind in
                                   INDICATORS_ORDER]
        context['result_list'] = [result[ind] for ind in INDICATORS_ORDER]
        context['categories_chart'] = [ind.upper() for ind in INDICATORS_ORDER]
        context['country_indicators'] = CountryIndicator.objects.all()
        return context

    def test_func(self):
        """If user in not mentor of group and if group exists
        or if user typed another id -- rises 403 exception"""
        if self.kwargs.get('group'):
            return Group.objects.filter(
                pk=self.kwargs['pk'], mentor__id=self.request.user.pk).exists()
        return self.kwargs['current_user'] == self.request.user.username

    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            try:
                feedback_id = request.GET['feedback_id']
                offset = int(request.GET['offset'])
                paginate_by = int(request.GET['paginate_by'])
            except (KeyError, ValueError):
                return JsonResponse({'status': 'false',
                                     'message': 'Incorrect request parameters'
                                     },
                                    status=400)

            return ResultView._next_recommendations_response(feedback_id,
                                                             offset,
                                                             paginate_by)
        return super().get(request, *args, **kwargs)

    def _preparing_results_data(self, context, countries_values,
                                countries_names, countries_feedback):
        iso_codes = self.request.POST.getlist('select_indicator')
        for iso_code in iso_codes:
            indicator_obj = context['country_indicators'].get(
                iso_code=iso_code)
            countries_values.update(indicator_obj.get_indicators)
            countries_names.append(indicator_obj.name)
            countries_feedback[indicator_obj.name] = ResultView._get_feedback(
                countries_values[iso_code], context['result_list'],
                INDICATORS_ORDER)

    @staticmethod
    def _get_feedback(indicators_values, result, indicators_name):
        """
        Retrieve for each indicator feedback based on country and result
        difference

        Assuming three parameters with same length
        :param indicators_values: values for selected country
        :param result: users results by each indicators
        :param indicators_name in correct order
        :return: dict with feedback for each indicator
        """
        indicators_feedback = {}
        for i in range(len(indicators_values)):
            indicators_difference = abs(indicators_values[i] - result[i])
            indicator_feedback = Feedback.objects.filter(
                Q(min_value__lte=indicators_difference) &
                Q(max_value__gte=indicators_difference),
                indicator__iexact=indicators_name[i])
            indicators_feedback[indicators_name[i]] = indicator_feedback
        return indicators_feedback

    @staticmethod
    def _next_recommendations_response(feedback_id, offset, paginate_by):
        """
        Calculate next recommendation portion to retrieve
        :param feedback_id:
        :param offset: current recommendations retrieved
        :param paginate_by:
        :return: jsonresponse with list of recommendations and end variable if
        no more recommendations available
        """
        query = Recommendation.objects.filter(feedback__id=feedback_id) \
            [offset:offset + paginate_by]
        recommendations = list(query.values_list('recommendation', flat=True))
        end = 'end' if Recommendation.objects.filter(feedback__id=feedback_id)\
                                     .count() <= offset + paginate_by else ''
        return JsonResponse({'end': end,
                             'recommendations': recommendations
                             })
