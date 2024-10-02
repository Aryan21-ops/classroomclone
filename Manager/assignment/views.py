from django.shortcuts import render, redirect, HttpResponse
from django.urls import reverse, reverse_lazy
from .models import Assignment, Response
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from .forms import AssignmentForm, ResponseForm, AssignmentFilesForm
from group.models import Group
# from assignment.tasks import test
# Create your views here.


def delete(request, pk):
    try:
        assignment = Assignment.objects.get(pk=pk)
        group_slug = assignment.group.slug
        assignment.delete()
        return reverse_lazy('group:class_single', kwargs={'slug': group_slug})
    except ObjectDoesNotExist:
        messages.warning(request, "Assignment is not found")
        return redirect('group:base1')


def update_assignment(request, pk):
    context = {}
    assignment = Assignment.objects.get(pk=pk)
    group_slug = assignment.group.slug
    form = AssignmentForm(request.POST or None, instance=assignment)
    if form.is_valid():
        form.save()
        return reverse('group:class_single', kwargs={'slug': group_slug})
    context['assignment_form'] = form
    return render(request, "update-assignment.html", context)


def create_assignment(request, slug):
    context = {}
    group = Group.objects.filter(slug=slug)[0]
    if request.method == 'POST':
        form = AssignmentForm(request.POST)
        if form.is_valid():
            form.save(commit=False)
            form.instance.group = group
            form.save()
            aslug = form.instance.slug
            print(form.instance.group.name)
            # add_task_in_post.delay(request.user.username,
            #                        form.instance.id, form.instance.group.id)
            return redirect('assignment:assignment-detail', slug=aslug)
    context['assignment_form'] = AssignmentForm()

    return render(request, "create-assignment.html", context)


def assignment_detail(request, assignment_slug):

    assignment = Assignment.objects.filter(slug=assignment_slug)[0]
    responseform = ResponseForm()
    assignmentform = AssignmentFilesForm()

    if request.method == 'POST':
        if 'response-form' in request.POST:
            form = ResponseForm(request.POST, request.FILES)
            if form.is_valid():
                response = Response.objects.create(
                    student=request.user, assignment=assignment)
                form.save(commit=False)
                form.instance.response = response
                form.save()
                messages.success(
                    request, "Assignment has been Successfully Added")
                return redirect('assignment:assignment-detail', slug=assignment.slug)
        if 'attachments' in request.POST:
            form = AssignmentFilesForm(request.POST, request.FILES)
            if form.is_valid():
                form.save(commit=False)
                form.instance.assignment = assignment
                form.save()
                messages.success(
                    request, "Attachments has been Successfully Added")
                return redirect('assignment:assignment-detail', slug=assignment.slug)

    context = {
        'assignment': assignment,
        'responseform': responseform,
        'assignmentform': assignmentform,
    }

    return render(request, 'assignment-detail.html', context)


def celery_test(request):
    test.delay(10)
    return HttpResponse("Celery Works")
