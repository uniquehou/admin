from django.contrib import admin
from .models import Version, Announcement, Live

class VersionAdmin(admin.ModelAdmin):
	list_display = ('version', 'update_url',)
	list_filter = ['version',]

class AnnouncementAdmin(admin.ModelAdmin):
	list_display = ('text', 'create_time')
	list_filter = ['create_time',]

class LiveAdmin(admin.ModelAdmin):
	list_display = ('name', 'show_image', 'anchor_count', 'create_time',)
	list_filter = ['name',]
	search_fields = ('name', 'summary')
	

admin.site.register(Version, VersionAdmin)
admin.site.register(Announcement, AnnouncementAdmin)
admin.site.register(Live, LiveAdmin)
