# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from sphinxsite import models as sphinx_models

class InviteCodeAdmin(admin.ModelAdmin):

	list_display = ['first_name', 'last_name', 'email', 'code', 'in_use']
	readonly_fields = ['code']

class SiteUserAdmin(admin.ModelAdmin):

	list_display = ['first_name', 'last_name', 'email', 'team']
	readonly_fields = ['first_name', 'last_name', 'email', 'team', 'invite']
	exclude = ['user', 'invite_code_input', 'invite_code']

	def has_delete_permission(self, request, obj=None):
		return False



admin.site.register(sphinx_models.InviteCode, InviteCodeAdmin)
admin.site.register(sphinx_models.SiteUser, SiteUserAdmin)


