from django.shortcuts import render, redirect
from www.forms import *
from www.models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import datetime
from dateutil.relativedelta import relativedelta
import calendar


def register(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(user.password)
            user.save()
            account = Account(user=user)
            account.save()
            return redirect('index')
        elif User.objects.filter(username=request.POST["username"]).exists():
            context = {'errors':
                       "El username elegido no esta disponible"}
        return render(request, 'register.html', context)
    return render(request, 'register.html', {'errors': None})


def userLogin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            return render(request, 'login.html',
                          {'errors': "User o password incorrectos"})
    return render(request, 'login.html', {'errors': None})


def userLogout(request):
    logout(request)
    return redirect('userLogin')


@login_required(login_url='/login')
def index(request):
    today = datetime.datetime.now()
    return redirect('indexCalendar', year=today.year, month=today.month)


@login_required(login_url='/login')
def indexCalendar(request, year, month):
    acc = Account.objects.get(user=request.user)
    today = datetime.datetime.now()
    now = datetime.date(int(year), int(month), today.day)
    days, months = days_of_month(now)
    result = []
    for i in xrange(len(days)):
        if days[i] < 10:
            aux = "0" + str(days[i]) + "/"
        else:
            aux = str(days[i]) + "/"
        if months[i] < 10:
            aux += "0"
        aux += str(months[i]) + "/"
        aux += str(now.year)
        result.append(aux)
    result = zip(days, months, result)
    list_events = Event.objects.filter(user=request.user,
                                       date__gte=now).order_by("date")[:5]
    list_jobs = Job.objects.filter(user=request.user).order_by("-importance",
                                                               "-progress")[:5]
    list_meetings = Meeting.objects.filter(user=request.user,
                                           date__gte=now).order_by("date")[:5]
    all_events = Event.objects.filter(user=request.user)
    all_ev_dates = []
    for event in all_events:
        all_ev_dates.append(event.date)
    all_meetings = Meeting.objects.filter(user=request.user)
    all_meet_dates = []
    for meet in all_meetings:
        all_meet_dates.append(meet.date)
    aux = now - relativedelta(months=1)
    previousMonth = aux.month
    aux = now + relativedelta(months=1)
    nextMonth = aux.month
    context = {'account': acc,
               'list_events': list_events,
               'list_jobs': list_jobs,
               'list_meetings': list_meetings,
               'all_events': all_ev_dates,
               'all_meetings': all_meet_dates,
               'now': now,
               'previousMonth': previousMonth,
               'nextMonth': nextMonth,
               'today': today,
               'result': result}
    return render(request, 'index.html', context)


@login_required(login_url='/login')
def profile(request):
    acc = Account.objects.get(user=request.user)
    now = datetime.datetime.now()
    list_events = Event.objects.filter(user=request.user,
                                       date__gte=now).order_by("date")[:5]
    list_jobs = Job.objects.filter(user=request.user).order_by("-importance",
                                                               "-progress")[:5]
    list_meetings = Meeting.objects.filter(user=request.user,
                                           date__gte=now).order_by("date")[:5]
    if request.method == 'POST':
        user = request.user
        user.username = request.POST["username"]
        user.first_name = request.POST["first_name"]
        user.last_name = request.POST["last_name"]
        user.email = request.POST["email"]
        if request.POST["password"] != "":
            user.set_password(request.POST["password"])
        user.save()
        if "avatar" in request.FILES:
            acc.avatar = request.FILES["avatar"]
            acc.save()
    context = {'account': acc,
               'list_events': list_events,
               'list_jobs': list_jobs,
               'list_meetings': list_meetings}
    return render(request, 'profile.html', context)


@login_required(login_url='/login')
def create_event(request):
    acc = Account.objects.get(user=request.user)
    now = datetime.datetime.now()
    list_events = Event.objects.filter(user=request.user,
                                       date__gte=now).order_by("date")[:5]
    list_jobs = Job.objects.filter(user=request.user).order_by("-importance",
                                                               "-progress")[:5]
    list_meetings = Meeting.objects.filter(user=request.user,
                                           date__gte=now).order_by("date")[:5]
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.user = request.user
            event.save()
            return redirect('events')
    context = {'account': acc,
               'list_events': list_events,
               'list_jobs': list_jobs,
               'list_meetings': list_meetings}
    return render(request, 'create_event.html', context)


@login_required(login_url='/login')
def edit_event(request, id_event):
    acc = Account.objects.get(user=request.user)
    now = datetime.datetime.now()
    event = Event.objects.get(pk=id_event, user=request.user)
    list_events = Event.objects.filter(user=request.user,
                                       date__gte=now).order_by("date")[:5]
    list_jobs = Job.objects.filter(user=request.user).order_by("-importance",
                                                               "-progress")[:5]
    list_meetings = Meeting.objects.filter(user=request.user,
                                           date__gte=now).order_by("date")[:5]
    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            event = form.save()
            return redirect('events')
    context = {'account': acc,
               'list_events': list_events,
               'list_jobs': list_jobs,
               'list_meetings': list_meetings,
               'event': event}
    return render(request, 'edit_event.html', context)


@login_required(login_url='/login')
def delete_event(request, id_event):
    event = Event.objects.get(pk=id_event, user=request.user)
    event.delete()
    return redirect('events')


@login_required(login_url='/login')
def create_job(request):
    acc = Account.objects.get(user=request.user)
    now = datetime.datetime.now()
    list_events = Event.objects.filter(user=request.user,
                                       date__gte=now).order_by("date")[:5]
    list_jobs = Job.objects.filter(user=request.user).order_by("-importance",
                                                               "-progress")[:5]
    list_meetings = Meeting.objects.filter(user=request.user,
                                           date__gte=now).order_by("date")[:5]
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.user = request.user
            job.save()
            return redirect('jobs')
    context = {'account': acc,
               'list_events': list_events,
               'list_jobs': list_jobs,
               'list_meetings': list_meetings}
    return render(request, 'create_job.html', context)


@login_required(login_url='/login')
def edit_job(request, id_job):
    acc = Account.objects.get(user=request.user)
    now = datetime.datetime.now()
    job = Job.objects.get(pk=id_job, user=request.user)
    list_events = Event.objects.filter(user=request.user,
                                       date__gte=now).order_by("date")[:5]
    list_jobs = Job.objects.filter(user=request.user).order_by("-importance",
                                                               "-progress")[:5]
    list_meetings = Meeting.objects.filter(user=request.user,
                                           date__gte=now).order_by("date")[:5]
    if request.method == 'POST':
        form = JobForm(request.POST, instance=job)
        if form.is_valid():
            job = form.save()
            return redirect('jobs')
    context = {'account': acc,
               'list_events': list_events,
               'list_jobs': list_jobs,
               'list_meetings': list_meetings,
               'job': job}
    return render(request, 'edit_job.html', context)


@login_required(login_url='/login')
def delete_job(request, id_job):
    job = Job.objects.get(pk=id_job, user=request.user)
    job.delete()
    return redirect('jobs')


@login_required(login_url='/login')
def create_meeting(request):
    acc = Account.objects.get(user=request.user)
    now = datetime.datetime.now()
    list_events = Event.objects.filter(user=request.user,
                                       date__gte=now).order_by("date")[:5]
    list_jobs = Job.objects.filter(user=request.user).order_by("-importance",
                                                               "-progress")[:5]
    list_meetings = Meeting.objects.filter(user=request.user,
                                           date__gte=now).order_by("date")[:5]
    if request.method == 'POST':
        form = MeetingForm(request.POST)
        if form.is_valid():
            meeting = form.save(commit=False)
            meeting.user = request.user
            meeting.save()
            return redirect('index')
    context = {'account': acc,
               'list_events': list_events,
               'list_jobs': list_jobs,
               'list_meetings': list_meetings}
    return render(request, 'create_meeting.html', context)


@login_required(login_url='/login')
def edit_meeting(request, id_meeting):
    acc = Account.objects.get(user=request.user)
    now = datetime.datetime.now()
    meeting = Meeting.objects.get(pk=id_meeting, user=request.user)
    list_events = Event.objects.filter(user=request.user,
                                       date__gte=now).order_by("date")[:5]
    list_jobs = Job.objects.filter(user=request.user).order_by("-importance",
                                                               "-progress")[:5]
    list_meetings = Meeting.objects.filter(user=request.user,
                                           date__gte=now).order_by("date")[:5]
    if request.method == 'POST':
        form = MeetingForm(request.POST, instance=meeting)
        if form.is_valid():
            meeting = form.save()
            return redirect('index')
    context = {'account': acc,
               'list_events': list_events,
               'list_jobs': list_jobs,
               'list_meetings': list_meetings,
               'meeting': meeting}
    return render(request, 'edit_meeting.html', context)


@login_required(login_url='/login')
def delete_meeting(request, id_meeting):
    meeting = Meeting.objects.get(pk=id_meeting, user=request.user)
    meeting.delete()
    return redirect('index')


@login_required(login_url='/login')
def events(request):
    acc = Account.objects.get(user=request.user)
    now = datetime.datetime.now()
    list_events = Event.objects.filter(user=request.user,
                                       date__gte=now).order_by("date")[:5]
    list_jobs = Job.objects.filter(user=request.user).order_by("-importance",
                                                               "-progress")[:5]
    list_meetings = Meeting.objects.filter(user=request.user,
                                           date__gte=now).order_by("date")[:5]
    all_events = Event.objects.filter(user=request.user,
                                      date__gte=now).order_by("date")
    context = {'account': acc,
               'list_events': list_events,
               'list_jobs': list_jobs,
               'list_meetings': list_meetings,
               'all_events': all_events}
    return render(request, 'events.html', context)


@login_required(login_url='/login')
def jobs(request):
    acc = Account.objects.get(user=request.user)
    now = datetime.datetime.now()
    list_events = Event.objects.filter(user=request.user,
                                       date__gte=now).order_by("date")[:5]
    list_jobs = Job.objects.filter(user=request.user).order_by("-importance",
                                                               "-progress")[:5]
    list_meetings = Meeting.objects.filter(user=request.user,
                                           date__gte=now).order_by("date")[:5]
    all_jobs = Job.objects.filter(user=request.user).order_by("-importance",
                                                              "-progress")
    context = {'account': acc,
               'list_events': list_events,
               'list_jobs': list_jobs,
               'list_meetings': list_meetings,
               'all_jobs': all_jobs}
    return render(request, 'jobs.html', context)


@login_required(login_url='/login')
def meetings(request):
    acc = Account.objects.get(user=request.user)
    now = datetime.datetime.now()
    list_events = Event.objects.filter(user=request.user,
                                       date__gte=now).order_by("date")[:5]
    list_jobs = Job.objects.filter(user=request.user).order_by("-importance",
                                                               "-progress")[:5]
    list_meetings = Meeting.objects.filter(user=request.user,
                                           date__gte=now).order_by("date")[:5]
    all_meetings = Meeting.objects.filter(user=request.user,
                                          date__gte=now).order_by("date")
    context = {'account': acc,
               'list_events': list_events,
               'list_jobs': list_jobs,
               'list_meetings': list_meetings,
               'all_meetings': all_meetings}
    return render(request, 'meetings.html', context)


@login_required(login_url='/login')
def day(request, day, month, year):
    acc = Account.objects.get(user=request.user)
    now = datetime.datetime.now()
    day = datetime.date(int(year), int(month), int(day))
    list_events = Event.objects.filter(user=request.user,
                                       date__gte=now).order_by("date")[:5]
    list_jobs = Job.objects.filter(user=request.user).order_by("-importance",
                                                               "-progress")[:5]
    list_meetings = Meeting.objects.filter(user=request.user,
                                           date__gte=now).order_by("date")[:5]
    events_by_day = Event.objects.filter(user=request.user, date=day)
    meetings_by_day = Meeting.objects.filter(user=request.user, date=day)
    context = {'account': acc,
               'list_events': list_events,
               'list_jobs': list_jobs,
               'list_meetings': list_meetings,
               'day': day,
               'events_by_day': events_by_day,
               'meetings_by_day': meetings_by_day}
    return render(request, 'day.html', context)


@login_required(login_url='/login')
def search(request):
    if request.method == 'POST':
        date = request.POST.get("date")
        try:
            date = datetime.datetime.strptime(date, '%d/%m/%Y')
            return redirect('day', day=date.day,
                            month=date.month, year=date.year)
        except:
            return redirect('index')


def days_of_month(date):
    aux = date - datetime.timedelta(date.weekday())
    if aux.month == date.month:
        aux = aux - datetime.timedelta(7 * ((aux.day / 7) + 1))
    days = []
    months = []
    if aux.day != 1:
        if date.month > 1:
            before_month = calendar.monthrange(date.year, date.month-1)[1]
        else:
            before_month = calendar.monthrange(date.year-1, 12)[1]
        days = range(aux.day, before_month+1)
        for elem in days:
            months.append(aux.month)
    this_month = calendar.monthrange(date.year, date.month)[1]
    this_days = range(1, this_month+1)
    days.extend(this_days)
    for elem in this_days:
        months.append(date.month)
    aux = datetime.date(date.year, date.month, this_month)
    if aux.weekday() != 6:
        aux = aux + datetime.timedelta(6-aux.weekday())
        this_days = range(1, aux.day+1)
        days.extend(this_days)
        for elem in this_days:
            months.append(aux.month)
    return days, months
