from __future__ import absolute_import
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db import transaction
from .models import UserProfile, Question, Answer, Comment, Tag, QVoter, Voter
import datetime


def get_user_profile(user_ob):
    try:
        obj = UserProfile.objects.get(user=user_ob)
    except UserProfile.DoesNotExist:
        obj = UserProfile(user=user_ob)
        obj.save()
    return obj


@require_POST
def search(request):
    word = request.POST['word']
    latest_question_list = Question.objects.filter(question_text__contains=word)
    paginator = Paginator(latest_question_list, 10)
    page = request.GET.get('page')
    try:
        questions = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        questions = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        questions = paginator.page(paginator.num_pages)

    latest_noans_list = Question.objects.order_by('-pub_date')\
                                        .filter(tags__slug__contains=word, answer__isnull=True)[:10]
    top_questions = Question.objects.order_by('-reward')\
                                    .filter(tags__slug__contains=word, answer__isnull=True, reward__gte=1)[:10]
    count = Question.objects.count
    count_a = Answer.objects.count

    return render(request, 'qa/index.html', {
        'questions': questions,
        'totalcount': count,
        'anscount': count_a,
        'noans': latest_noans_list,
        'reward': top_questions,
    })


def tag(request, slug):
    latest_question_list = Question.objects.filter(tags__slug=slug)
    paginator = Paginator(latest_question_list, 10)
    page = request.GET.get('page')
    try:
        questions = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        questions = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        questions = paginator.page(paginator.num_pages)

    latest_noans_list = Question.objects\
        .order_by('-pub_date')\
        .filter(tags__slug=slug,
                answer__isnull=True)[:10]
    top_questions = Question.objects\
        .order_by('-reward') \
        .filter(tags__slug=slug,
                answer__isnull=True,
                reward__gte=1)[:10]
    count = Question.objects.count
    count_a = Answer.objects.count

    return render(request, 'qa/index.html', {
        'questions': questions,
        'totalcount': count,
        'anscount': count_a,
        'noans': latest_noans_list,
        'reward': top_questions,
    })


def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')
    latest_noans_list = Question.objects.order_by('-pub_date').filter(answer__isnull=True)[:10]
    top_questions = Question.objects.order_by('-reward').filter(answer__isnull=True, reward__gte=1)[:10]

    count = Question.objects.count
    count_a = Answer.objects.count

    paginator = Paginator(latest_question_list, 10)
    page = request.GET.get('page')
    try:
        questions = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        questions = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        questions = paginator.page(paginator.num_pages)

    return render(request, 'qa/index.html', {
        'questions': questions,
        'totalcount': count,
        'anscount': count_a,
        'noans': latest_noans_list,
        'reward': top_questions,
    })


def profile(request, user_id):
    user_ob = get_object_or_404(get_user_model(), id=user_id)
    user = get_user_profile(user_ob)
    return render(request, 'qa/profile.html', {'user': user})


@login_required
@transaction.atomic
def add(request):
    if request.method == 'POST':
        question_text = request.POST['question']
        tags_text = request.POST['tags']
        user = get_user_profile(request.user)

        if question_text.strip() == '':
            return render(request, 'qa/add.html', {'message': 'Empty'})

        pub_date = datetime.datetime.now()
        q = Question()
        q.question_text = question_text
        q.pub_date = pub_date
        q.user_data = user
        q.save()

        tags = tags_text.split(',')
        for tag_slug in tags:
            try:
                t = Tag.objects.get(slug=tag_slug)
                q.tags.add(t)
            except Tag.DoesNotExist:
                t = Tag()
                t.slug = tag_slug
                t.save()
                q.tags.add(t)
        return redirect("qa:detail", question_id=q.id)
    return render(request, 'qa/add.html', {})


@login_required
@transaction.atomic
def comment(request, answer_id):
    if request.method == 'POST':
        comment_text = request.POST['comment']

        user = get_user_profile(request.user)
        user.points += 1
        user.save()

        if comment_text.strip() == '':
            return render(request, 'qa/comment.html', {'answer_id': answer_id, 'message': 'Empty'})

        pub_date = datetime.datetime.now()
        a = get_object_or_404(Answer, pk=answer_id)
        c = Comment()
        c.answer = a
        c.comment_text = comment_text
        c.pub_date = pub_date
        c.user_data = user
        c.save()

        question = a.question
        question.views += 1
        question.save()
        answer_list = question.answer_set.order_by('-votes')

        paginator = Paginator(answer_list, 10)
        page = request.GET.get('page')
        try:
            answers = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            answers = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            answers = paginator.page(paginator.num_pages)

        return render(request, 'qa/detail.html', {'answers': answers, 'question': question}, )

    return render(request, 'qa/comment.html', {'answer_id': answer_id})


def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)

    question.views += 1
    question.save()
    answer_list = question.answer_set.order_by('-votes')

    paginator = Paginator(answer_list, 10)
    page = request.GET.get('page')
    try:
        answers = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        answers = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        answers = paginator.page(paginator.num_pages)

    return render(request, 'qa/detail.html', {'answers': answers, 'question': question}, )


@login_required
def answer(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'qa/answer.html', {'question': question})


@login_required
@require_POST
@transaction.atomic
def add_answer(request):
    answer_text = request.POST['answer']
    question_id = request.POST['question']

    question = get_object_or_404(Question, pk=question_id)

    user = get_user_profile(request.user)
    user.points += 5
    user.save()

    if answer_text.strip() == '':
        return render(request, 'qa/answer.html', {'question': question, 'message': 'Empty'})

    a = Answer()
    pub_date = datetime.datetime.now()
    a.answer_text = answer_text
    a.question = question
    a.user_data = user
    a.pub_date = pub_date
    a.save()

    return redirect("qa:detail", question_id=question.id)

@login_required
@transaction.atomic
def vote(request, answer_id, question_id, op_code):
    user = get_user_profile(request.user)
    question = get_object_or_404(Question, pk=question_id)
    answer_ob = get_object_or_404(Answer, pk=answer_id)

    answer_list = question.answer_set.order_by('-votes')

    paginator = Paginator(answer_list, 10)
    page = request.GET.get('page')
    try:
        answers = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        answers = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        answers = paginator.page(paginator.num_pages)

    if Answer.objects.filter(id=answer_id, user_data=user).exists():
        return render(request, 'qa/detail.html',
                      {'question': question, 'answers': answers, 'message': "You cannot vote on your answer!"})

    if Voter.objects.filter(answer_id=answer_id, user=user).exists():
        return render(request, 'qa/detail.html',
                      {'question': question, 'answers': answers, 'message': "You've already cast vote on this answer!"})

    if op_code == '0':
        answer_ob.votes += 1
        u = answer_ob.user_data
        u.points += 10
        u.points += question.reward
        u.save()
    if op_code == '1':
        answer_ob.votes -= 1
        u = answer_ob.user_data
        u.points -= 10
        u.save()
    answer_ob.save()

    answer_list = question.answer_set.order_by('-votes')

    paginator = Paginator(answer_list, 10)
    page = request.GET.get('page')
    try:
        answers = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        answers = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        answers = paginator.page(paginator.num_pages)

    v = Voter()
    v.user = user
    v.answer = answer_ob
    v.save()

    return render(request, 'qa/detail.html', {'question': question, 'answers': answers})


@login_required
@transaction.atomic
def thumb(request, question_id, op_code):
    user = get_user_profile(request.user)
    question = Question.objects.get(pk=question_id)

    answer_list = question.answer_set.order_by('-votes')

    paginator = Paginator(answer_list, 10)
    page = request.GET.get('page')
    try:
        answers = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        answers = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        answers = paginator.page(paginator.num_pages)

    if QVoter.objects.filter(question_id=question_id, user=user).exists():
        return render(request, 'qa/detail.html', {'question': question, 'answers': answers,
                                                  'message': "You've already cast vote on this question!"})

    if op_code == '0':
        question.reward += 5
        u = question.user_data
        u.points += 5
        u.save()
    if op_code == '1':
        question.reward -= 5
        u = question.user_data
        u.points -= 5
        u.save()
    question.save()

    v = QVoter()
    v.user = user
    v.question = question
    v.save()

    return redirect("qa:detail", question_id=question.id)
