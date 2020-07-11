from django.contrib import admin

from events.models import CaseBuy, CasePieceCommit, CaseSplit, Category, Event, EventMembership, Item

admin.site.register(CaseBuy)
admin.site.register(CasePieceCommit)
admin.site.register(CaseSplit)
admin.site.register(Category)
admin.site.register(Event)
admin.site.register(EventMembership)
admin.site.register(Item)