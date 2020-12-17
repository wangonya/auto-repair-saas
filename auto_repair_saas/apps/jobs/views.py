from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render

from auto_repair_saas.apps.jobs.forms import NewJobForm


@login_required
def jobs(request):
    return render(request, 'jobs/index.html')


@login_required
def new_job(request):
    if request.method == 'POST':
        form = NewJobForm(request.POST)
        if form.is_valid():
            return HttpResponseRedirect('/jobs/')
        else:
            error = 'Invalid email / password.'
            return render(
                request, 'jobs/new.html', {
                    'form': form, 'error': error
                }
            )
    else:
        form = NewJobForm()
    return render(request, 'jobs/new.html', {'form': form})
