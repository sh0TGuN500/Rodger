from django.db.utils import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.utils import timezone
from django.views import generic
from django.views.generic.base import View

from .forms import CommentForm, AddQuestionForm
from .models import Question, Choice


class IndexView(generic.ListView):
    paginate_by = 10
    template_name = 'polls/polls_list.html'
    # context_object_name = 'latest_question_list'

    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')


class DetailMixinView(generic.edit.FormMixin, generic.detail.DetailView):
    model = Question
    template_name = 'polls/polls_detail.html'
    form_class = CommentForm

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultView(generic.DetailView):
    model = Question
    template_name = 'polls/votes_results.html'


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/polls_detail.html', {
            'question': question,
            'form': CommentForm(),
            'error_message': 'You didn\'t select a choice'
        })
    else:
        if question.vote_set.filter(user=request.user.id):
            return render(request, 'polls/polls_detail.html', {
                'question': question,
                'form': CommentForm(),
                'error_message': 'You have already voted'
            })
        add_vote = question.vote_set.create(question_id=question_id,
                                            choice_id=request.POST['choice'],
                                            user=request.user.id)
        add_vote.save()
        selected_choice.votes += 1
        selected_choice.save()

        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))


def text_validator(text):
    splitted_text = text.split()
    if len(splitted_text) >= 0 and not text.isspace():
        return ' '.join(splitted_text)
    else:
        return None


def search(request):
    valid_text = text_validator(request.POST['search'])
    if valid_text:
        latest_question_list = Question.objects.filter(question_title__icontains=valid_text)
        context = {'latest_question_list': latest_question_list}
    else:
        search_message = 'You input invalid text'
        context = {'search_message': search_message}
    return render(request, 'polls/polls_list.html', context=context)


def my_questions(request):
    if request.user.is_authenticated:
        latest_question_list = Question.objects.filter(author_name=request.user)
        context = {'latest_question_list': latest_question_list}
    else:
        error_message = 'To view your questions, you must be '
        context = {'error_message': error_message}
    return render(request, 'polls/polls_list.html', context=context)


'''def leave_comment(request, question_id):
    question = get_object_or_404(Question, id=question_id)

    if text_validator(request.POST['text']):
        question.comment_set.create(author_name=request.user, comment_text=request.POST['text'])
        return HttpResponseRedirect(reverse('polls:detail', args=(question.id,)))

    return render(request, 'polls/polls_detail.html', {
        'question': question,
        'error_comment': 'You input invalid text'
    })'''


def home(request):
    return render(request, 'polls/home_page.html')


def personal_page(request):
    return render(request, 'polls/personal_page.html')


def add_question(request):
    if request.user.is_staff:
        return render(request, 'polls/add_question.html', {
            'form': AddQuestionForm
        })
    else:
        return HttpResponseRedirect(reverse('polls:home'))


def leave_question(request):
    form = AddQuestionForm
    data = request.POST
    if not request.user.is_staff or not data:
        return HttpResponseRedirect(reverse('polls:home'))
    title = text_validator(data['question_title'])
    text = text_validator(data['question_text'])
    if title and text and data:
        if data.get('choice'):
            choice_list = dict(data.lists())['choice']
            count = 0
            for choice in choice_list:
                if text_validator(choice):
                    choice_list[count] = text_validator(choice)
                    count += 1
                else:
                    return render(request, 'polls/add_question.html', {
                        'error_message': 'You input invalid text'
                    })
            create_question = Question(question_title=title,
                                       question_text=text,
                                       author_name=request.user,
                                       pub_date=timezone.now())
            try:
                create_question.save()
            except IntegrityError:
                return render(request, 'polls/add_question.html', {
                    'error_message': f'Title "{title}" already exist',
                    'form': form,
                })

            for choice in choice_list:
                create_choice = Choice(question_id=create_question.id,
                                       choice_text=choice)
                create_choice.save()
        else:
            create_question = Question(question_title=title,
                                       question_text=text,
                                       author_name=request.user,
                                       pub_date=timezone.now())
            try:
                create_question.save()
            except IntegrityError:
                return render(request, 'polls/add_question.html', {
                    'error_message': f'Title "{title}" already exist',
                    'form': form,
                })
        return HttpResponseRedirect(reverse('polls:detail', args=(create_question.id,)))

    else:
        return render(request, 'polls/add_question.html', {
            'error_message': 'You input invalid text',
            'form': form,
        })


'''class AddQuestion(View):
    def post(self, request):
        print(request.POST)
        print(id)
        form = QuestionForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.question_id = pk
        return redirect('/')'''


class AddComment(View):
    def get(self, request, question):
        return HttpResponseRedirect(reverse('polls:home'))

    def post(self, request, question):
        question = get_object_or_404(Question, id=question)
        form = CommentForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.question = question
            form.author_name = request.user
            form.save()
            return HttpResponseRedirect(reverse('polls:detail', args=(question.id,)))
        else:
            return render(request, 'polls/polls_detail.html', {
                'question': question,
                'form': form
            })
