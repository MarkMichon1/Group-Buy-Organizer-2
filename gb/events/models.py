from django.db import models

from decimal import Decimal
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
        target_case_splits = []

        if page_type == 'event':
            items = self.items.all()

        elif page_type == 'breakdown' or page_type == 'summary':
            for item in self.items.all():
                if item.case_splits.filter(is_complete=True).count() > 0 or item.case_buys.count() > 0:
                    items.append(item)

        elif page_type == 'my_order':
            case_buys = CaseBuy.objects.filter(membership=membership)
            for case_buy in case_buys:
                items.append(case_buy.item)
            split_commits = CasePieceCommit.objects.filter(membership=membership)
            for commit in split_commits:
                if commit.case_split.is_complete:
                    target_case_splits.append(commit.case_split)
                    if commit.case_split.item not in items:
                        items.append(commit.case_split.item)


        page_data = {}

        # Core Category/Item View
        item_groups = []
        grand_total = 0
        total_cases = 0
        if items:
            category_list = [items[0].category.name, []]
            category_name = items[0].category.name
            for item in items:
                if item.category.name == category_name:
                    if page_type == 'event':
                        item_view = item.render_event_view(membership=membership)
                    elif page_type == 'summary':
                        item_view = item.render_summary_view()
                        total_cases += item_view['total_cases']
                        grand_total += item_view['total']
                    elif page_type == 'breakdown':
                        item_view = item.render_breakdown_view()
                        item_view['casebuys'] = item.case_buys.all()
                        item_view['casesplits'] = item.case_splits.filter(is_complete=True).all()
                    elif page_type == 'my_order':
                        item_view = item.render_my_order_view(membership=membership)
                        grand_total += item_view['your_total_price']

                else:
                    item_groups.append(category_list)
                    category_name = item.category.name
                    category_list = [item.category.name, []]
                    if page_type == 'event':
                        item_view = item.render_event_view(membership=membership)
                    elif page_type == 'summary':
                        item_view = item.render_summary_view()
                        total_cases += item_view['total_cases']
                        grand_total += item_view['total']
                    elif page_type == 'breakdown':
                        item_view = item.render_breakdown_view()
                        item_view['casebuys'] = item.case_buys.all()
                        item_view['casesplits'] = item.case_splits.filter(is_complete=True).all()
                    elif page_type == 'my_order':
                        item_view = item.render_my_order_view(membership=membership)
                        grand_total += item_view['your_total_price']
                category_list[1].append(item_view)

            # Cleanup
            item_groups.append(category_list)


        page_data['item_groups'] = item_groups
        page_data['grand_total'] = grand_total
        page_data['total_cases'] = total_cases
        page_data['target_case_splits'] = target_case_splits

        # Extras at end of page
        if page_type == 'breakdown':
            page_data['member_totals'] = self.generate_user_totals_all()
        elif page_type == 'my_order':
            my_order_summary = self.generate_user_totals_all(target_membership=membership)
            page_data['my_order_summary'] = my_order_summary

        return page_data

    def generate_user_totals_all(self, target_membership=None):
        master_dict = {}
        membership_list = []
        grand_total = 0
        my_order_summary = {}
        if target_membership:
            for membership in EventMembership.objects.filter(event=self):
                pre_total = membership.generate_my_total()
                grand_total += pre_total
            pre_total = target_membership.generate_my_total()
            my_order_summary['pre_order'] = pre_total
            percentage_of_event = pre_total / grand_total
            my_order_summary['displayed_percentage'] = round(percentage_of_event * 100, 2)
            my_order_summary['share_of_fee'] = round((self.extra_charges * percentage_of_event), 2)
            my_order_summary['post_total'] = round((pre_total + my_order_summary['share_of_fee']), 2)
            return my_order_summary

        else:
            for membership in EventMembership.objects.filter(event=self):
                member_dict = {}
                member_dict['username'] = membership.user.username
                member_dict['user_id'] = membership.user.id
                member_dict['id'] = membership.id
                member_dict['has_paid'] = membership.has_paid
                pre_total = membership.generate_my_total()
                grand_total += pre_total
                member_dict['pre_total'] = pre_total
                membership_list.append(member_dict)
            for member_dict in membership_list:
                percentage_of_event = member_dict['pre_total'] / grand_total if grand_total else 0
                member_dict['percentage_of_event'] = round(percentage_of_event, 2)
                member_dict['displayed_percentage'] = round(percentage_of_event * 100, 2)
                member_dict['share_of_fee'] = round((self.extra_charges * percentage_of_event), 2)
                member_dict['post_total'] = round((member_dict['pre_total'] + member_dict['share_of_fee']), 2)

            master_dict['membership_list'] = membership_list
            master_dict['grand_total'] = grand_total
            return master_dict


class EventMembership(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='members')
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
        for case_buy in self.case_buys.all():
            total += case_buy.item.price * case_buy.quantity
        for commit in self.split_commits.all():
            if commit.case_split.is_complete:
                total += round((Decimal(commit.quantity/commit.case_split.item.packing) * commit.case_split.item.price), 2)

        return total

    class Meta:
        ordering = ('user',)


class Item(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    added_by = models.ForeignKey(EventMembership, null=True, on_delete=models.SET_NULL, related_name='created_items')
    date_created = models.DateTimeField(auto_now_add=True)
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
        returned_dict = {}
        returned_dict = {**returned_dict, **self._core_data_fragment()}
        returned_dict = {**returned_dict, **self._total_cases_fragment()}
        return returned_dict

    def render_my_order_view(self, membership):
        returned_dict = {}
        returned_dict = {**returned_dict, **self._core_data_fragment()}
        returned_dict = {**returned_dict, **self._your_involvement_fragment(membership, is_my_order=True)}
        return returned_dict

    def render_summary_view(self):
        returned_dict = {}
        returned_dict = {**returned_dict, **self._core_data_fragment()}
        returned_dict = {**returned_dict, **self._total_cases_fragment()}
        return returned_dict

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
        case_buys = CaseBuy.objects.filter(membership=membership).filter(item=self)
        for case_buy in case_buys:
            cases_you_bought += case_buy.quantity
        new_dict['cases_you_bought'] = cases_you_bought

        splits_involved_in = 0
        pieces_reserved_from_splits = 0
        for case_split in self.case_splits.all():
            if case_split.is_user_involved(membership.user) and case_split.is_complete:
                commit = CasePieceCommit.objects.filter(case_split=case_split).get(user=membership.user)
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
        total_cases = 0
        total_casebuy_cases = 0
        for case_buy in self.case_buys.all():
            total_casebuy_cases += case_buy.quantity
            total_cases += case_buy.quantity
        total_casesplit_cases = 0
        for case_split in self.case_splits.all():
            if case_split.is_complete:
                total_casesplit_cases += 1
                total_cases += 1

        new_dict['total_casebuy_cases'] = total_casebuy_cases
        new_dict['total_casesplit_cases'] =  total_casesplit_cases
        new_dict['total_cases'] =  total_cases
        new_dict['total'] = total_cases * self.price

        return new_dict

    def return_active_case_splits(self):
        return self.case_splits.filter(is_complete=False)

    def return_closed_case_splits(self):
        return self.case_splits.filter(is_complete=True)


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

    def return_casebuy_total(self):
        return round(self.quantity * self.item.price, 2)


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

    def return_available_pieces(self):
        total_pieces = self.item.packing
        for commit in self.split_commits.all():
            total_pieces -= commit.quantity
        return total_pieces

    def return_reserved_pieces(self):
        reserved_pieces = 0
        for commit in self.split_commits.all():
            reserved_pieces += commit.quantity
        return reserved_pieces

    def is_user_involved(self, user):
        for commit in self.split_commits.all():
            if user == commit.user:
                return True
        return False

    def get_filled_percentage(self):
        return (self.return_reserved_pieces()/self.item.packing) * 100

    def evaluate_complete_status(self):
        piece_sum = 0
        for commit in self.split_commits.all():
            piece_sum += commit.quantity
        if self.is_complete:
            if piece_sum < self.item.packing:
                self.is_complete = False
        else:
            if piece_sum == self.item.packing:
                self.is_complete = True
        self.save()

    class Meta:
        ordering = ('-date_created',)


class CasePieceCommit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    quantity = models.SmallIntegerField(null=False)
    date_created = models.DateTimeField(auto_now_add=True)
    membership = models.ForeignKey(EventMembership, on_delete=models.CASCADE, related_name='split_commits')
    case_split = models.ForeignKey(CaseSplit, on_delete=models.CASCADE, related_name='split_commits')

    def __str__(self):
        return f'(Commit) {self.event.name} -> {self.case_split.item.name} -> {self.user.username} -> ' \
               f'{self.quantity}/{self.case_split.item.packing}'

    def return_quantity_pledged_prettied(self):
        packing = self.case_split.item.packing
        price = self.case_split.item.price

        return f'{self.quantity}/{packing} -- ${round((self.quantity * (price/packing)), 2)}'

    class Meta:
        ordering = ('-date_created',)


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
    url = models.CharField(max_length=50)
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='item_youtube_videos')

    def __str__(self):
        return f'{self.item.name} -> {self.is_embeddable} -> {self.url}'

    class Meta:
        ordering = ('-date_added',)
