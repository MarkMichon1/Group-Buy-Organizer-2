from django.db import models

import math
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

    def generate_event_pages_contents(self, page_type, membership=None):
        items = []

        if page_type == 'event':
            items = self.items.all()

        elif page_type == 'breakdown' or page_type == 'summary':
            for item in self.items.all():
                if len(item.case_splits.count() > 0 or item.case_buys.count() > 0):
                    items.append(item)

        elif page_type == 'my_order':
            case_buys = CaseBuy.objects.filter(membership=membership)
            for case_buy in case_buys:
                items.append(case_buy.item)
            split_commits = CasePieceCommit.objects.filter(membership=membership)
            for commit in split_commits:
                if commit.case_split.is_complete:
                    items.append(commit.case_split.item)


        page_data = {}

        # Core Category/Item View
        item_groups = []
        if items:
            category_list = [items[0].category.name, []]
            category_name = items[0].category.name
            for item in items:
                if item.category.name == category_name:
                    if page_type == 'event':
                        category_list[1].append(item.render_event_view(membership=membership))
                else:
                    item_groups.append(category_list)
                    category_name = item.category.name
                    category_list = [item.category.name, []]
                    if page_type == 'event':
                        category_list[1].append(item.render_event_view(membership=membership))

            # Cleanup
            item_groups.append(category_list)


        page_data['item_groups'] = item_groups

        # Extras at end of page
        if page_type == 'breakdown':
            pass

        elif page_type == 'my_order':
            pass

        elif page_type == 'summary':
            pass

        return page_data


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

    def generate_my_total(self): # For use in added cost split, user breakdown final addup, and manage payments.
        total = 0
        for case_buy in self.case_buys: #todo... all?
            total += case_buy.item.price * case_buy.quantity
        for commit in self.split_commits:
            total += round(((commit.quantity/commit.case_split.item.packing) * commit.case_split.item.price), 2)

        return total

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
        return f'{self.event.name} -> {self.category.name} -> {self.name} -> {self.id}'

    def render_event_view(self, membership):
        returned_dict = {}
        returned_dict = {**returned_dict, **self._core_data_fragment()}
        returned_dict['active_case_splits'] = self.case_splits.filter(is_complete=False).count()
        returned_dict = {**returned_dict, **self._your_involvement_fragment(membership=membership)}
        comment_stats = {
            'item_comments': self.item_comments.count(),
            'item_youtube_videos': self.item_youtube_videos.count()
        }
        returned_dict = {**returned_dict, **comment_stats}
        return returned_dict

    def render_breakdown_view(self):
        pass

    def render_my_order_view(self):
        pass

    def render_summary_view(self):
        pass

    def _core_data_fragment(self):
        new_dict = {}
        new_dict['name'] = self.name
        new_dict['packing'] = self.packing
        new_dict['case_price'] = round(self.price, 2)
        new_dict['piece_price'] = round((self.price/self.packing), 2)
        new_dict['id'] = self.id
        return new_dict

    def _your_involvement_fragment(self, membership, is_my_order=False):
        new_dict = {}
        cases_you_bought = 0
        case_buys = CaseBuy.objects.filter(membership=membership)
        for case_buy in case_buys:
            cases_you_bought += case_buy.quantity
        new_dict['cases_you_bought'] = cases_you_bought

        splits_involved_in = 0
        pieces_reserved_from_splits = 0
        for commit in CasePieceCommit.objects.filter(membership=membership):
            if commit.case_split.is_complete:
                pieces_reserved_from_splits += commit.quantity
                splits_involved_in += 1
        new_dict['pieces_reserved_from_splits'] = pieces_reserved_from_splits

        new_dict['your_total_price'] = (cases_you_bought * self.price) + round(((self.price/self.packing) *
                                                                                pieces_reserved_from_splits), 2)

        new_dict['are_involved'] = new_dict['your_total_price'] > 0

        if is_my_order:
            new_dict['splits_involved_in'] = splits_involved_in

        return new_dict

    def _total_cases_fragment(self):
        new_dict = {}

        return new_dict



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

    def render_case_splits(self):
        pass


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
    membership = models.ForeignKey(EventMembership, blank=True, null=True, on_delete=models.SET_NULL, related_name='+')
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='item_comments')
    comment = models.TextField()

    class Meta:
        ordering = ('-date_added',)


class ItemYoutubeVideo(models.Model):
    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name='+')
    membership = models.ForeignKey(EventMembership, blank=True, null=True, on_delete=models.SET_NULL, related_name='+')
    date_added = models.DateTimeField(auto_now_add=True)
    is_embeddable = models.BooleanField()
    url = models.CharField(max_length=150)
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='item_youtube_videos')

    class Meta:
        ordering = ('-date_added',)
