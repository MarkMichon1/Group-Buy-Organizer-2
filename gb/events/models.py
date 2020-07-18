from django.db import models

import uuid

from users.models import User


class Category(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ('name',)


class Event(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, null=False)
    description = models.CharField(max_length=200, default='No description added!')
    date_created = models.DateTimeField(auto_now_add=True)
    is_locked = models.BooleanField(default=False)
    is_closed = models.BooleanField(default=False)
    users_full_event_visibility = models.BooleanField(default=True)
    extra_charges = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    created_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name='created_events')
    members = models.ManyToManyField(User, through='EventMembership')

    def __str__(self):
        return f'{self.name} - {self.id}'

    def get_active_participants(self):
        return EventMembership.objects.filter(event=self.id).count()

    def get_active_case_splits(self):
        return self.case_splits.filter(is_complete=False).count()

    def get_total_cases(self):
        total_cases_from_case_buys = 0
        for case_buy in self.case_buys.all():
            total_cases_from_case_buys += case_buy.quantity
        return self.case_splits.filter(is_complete=True).count() + total_cases_from_case_buys

    def get_event_total(self):
        total_count = 0
        for case_order in self.case_buys.all():
            total_count += case_order.quantity
        for case_split in self.case_splits.all():
            if case_split.is_complete == True:
                total_count += 1
        return total_count

    def get_total_comments(self):
        return self.comments.count()

    def generate_event_items(self):
        pass

    def generate_order_summary(self):
        pass

    def generate_user_breakdown(self):
        pass


class EventMembership(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_organizer = models.BooleanField(default=False)
    is_creator = models.BooleanField(default=False)
    has_paid = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.event.name} -> {self.user.username}'

    def check_if_active_buys_or_commits(self):
        return self.case_buys.count() > 1 or self.split_commits.count() > 1

    def generate_total(self): # For use in added cost split, user breakdown final addup, and manage payments.
        return 0.00

    class Meta:
        ordering = ('user',)


class Item(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    added_by = models.ForeignKey(EventMembership, null=True, on_delete=models.SET_NULL, related_name='created_items')
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    packing = models.SmallIntegerField()
    event = models.ForeignKey(Event, null=True, on_delete=models.CASCADE, related_name='items')
    category = models.ForeignKey(Category, null=True, on_delete=models.SET_NULL, related_name='items')

    def __str__(self):
        return f'{self.category.name} -> {self.name} -> {self.id}'

    class Meta:
        ordering = ('category', 'name')


class CaseBuy(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='case_buys')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='case_buys')
    membership = models.ForeignKey(EventMembership, on_delete=models.CASCADE, related_name='case_buys')
    quantity = models.SmallIntegerField(null=False)

    def __str__(self):
        return f'{self.event.name} -> {self.user.username} -> {self.item.name}'


class CaseSplit(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='case_splits')
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='case_splits')
    started_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    date_created= models.DateTimeField(auto_now_add=True)
    is_complete = models.BooleanField(default=False)

    def __str__(self):
        return f'(Split) {self.event.name} -> {self.item.name} -> {self.id}'


class CasePieceCommit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    quantity = models.SmallIntegerField(null=False)
    membership = models.ForeignKey(EventMembership, on_delete=models.CASCADE, related_name='split_commits')
    case_split = models.ForeignKey(CaseSplit, on_delete=models.CASCADE, related_name='split_commits')

    def __str__(self):
        return f'(Commit) {self.event.name} -> {self.case_split.item.name} -> {self.user.username} -> ' \
               f'{self.quantity}/{self.case_split.item.packing}'


class EventComment(models.Model):
    author = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL, related_name='+')
    membership = models.ForeignKey(EventMembership, blank=True, null=True, on_delete=models.SET_NULL, related_name='+')
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='comments')
    date_added = models.DateTimeField(auto_now_add=True)
    comment = models.TextField()

    def __str__(self):
        username = None
        if self.author:
            username = self.author.username
        return f'{self.event.name} -> {username} -> {self.date_added}'

    class Meta:
        ordering = ('-date_added',)


class ItemComment(models.Model):
    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name='+')
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='item_comments')
    comment = models.TextField()#todo ordering


class ItemYoutubeVideo(models.Model):
    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name='+')
    date_added = models.DateTimeField(auto_now_add=True)
    url = models.CharField(max_length=150) #todo ordering