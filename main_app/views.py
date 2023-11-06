from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect
from .models import Question, Comment
from .forms import QuestionForm, CommentForm

# Create your views here.
def home(request):
    return render(request, 'home.html')

def create_question(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user
            question.save()
            return redirect(question)
    else:
        form = QuestionForm()
    return render(request, 'create_question.html', {'form': form})

def create_comment(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.question = question
            comment.save()
            return redirect(question)
    else:
        form = CommentForm()
    return render(request, 'create_comment.html', {'form': form})

def edit_question(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.user == question.author:
        if request.method == 'POST':
            form = QuestionForm(request.POST, instance=question)
            if form.is_valid():
                form.save()
                return redirect('question_detail', question_id=question.id)
        else:
            form = QuestionForm(instance=question)
        return render(request, 'edit_question.html', {'form': form})

def edit_comment(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user == comment.author:
        if request.method == 'POST':
            form = CommentForm(request.POST, instance=comment)
            if form.is_valid():
                form.save()
                return redirect('question_detail', question_id=comment.question.id)
        else:
            form = CommentForm(instance=comment)
        return render(request, 'edit_comment.html', {'form': form})
    

def delete_question(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.user == question.author:
        question.delete()
        return redirect('question_list')

def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user == comment.author:
        question_id = comment.question.id
        comment.delete()
        return redirect('question_detail', question_id=question_id)