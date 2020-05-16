from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse
from django.views import generic
from .models import Group, GroupMember
from . import models
from django.shortcuts import get_object_or_404
from django.db import IntegrityError
from django.contrib import messages

class CreateGroup(LoginRequiredMixin, generic.CreateView):
    fields = ("name","description")
    model = Group

class SingleGroup(generic.DetailView):
    model = Group

class ListGroups(generic.ListView):
    model = Group

class JoinGroup(LoginRequiredMixin, generic.RedirectView):

    def get_redirect_url(self,*args,**kwargs):
        return reverse('groups:single', kwargs={'slug':self.kwargs.get('slug')})

    def get(self,request,*args,**kwargs):
        group = get_object_or_404(Group, slug=self.kwargs.get('slug'))

        try:
            GroupMember.objects.create(user=self.request.user, group=group)

        except IntegrityError:
            messages.warning(self.request, ('Already a member of the {}.'.format(group.name)))

        else:
            messages.success(self.request, ('You are now a member of {}.'.format(group.name)))

        return super().get(request,*args,**kwargs)

class LeaveGroup(LoginRequiredMixin, generic.RedirectView):

    def get_redirect_url(self,*args,**kwargs):
        return reverse('groups:single', kwargs={'slug':self.kwargs.get('slug')})

    def get(self,request,*args,**kwargs):
        try:
            membership = models.GroupMember.objects.filter(
                user = self.request.user,
                group__slug = self.kwargs.get('slug')
            ).get()

        except models.GroupMember.DoesNotExist:
            messages.warning(self.request, 'You are not a member of this group.')

        else:
            membership.delete()
            messages.success(self.request, 'You have successfully left the group.')

        return super().get(request,*args,**kwargs)
