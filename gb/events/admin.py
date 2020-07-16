from django.contrib import admin

from events.models import CaseBuy, CasePieceCommit, CaseSplit, Category, Event, EventComment, EventMembership, Item, \
    ItemComment, ItemYoutubeVideo

admin.site.register(CaseBuy)
admin.site.register(CasePieceCommit)
admin.site.register(CaseSplit)
admin.site.register(Category)
admin.site.register(Event)
admin.site.register(EventComment)
admin.site.register(EventMembership)
admin.site.register(Item)
admin.site.register(ItemComment)
admin.site.register(ItemYoutubeVideo)