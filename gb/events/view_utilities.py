from django.contrib import messages
from django.shortcuts import get_object_or_404
import requests
from requests.exceptions import Timeout

import json

from events.models import Event, EventMembership
from gb.secrets import get_secret


def event_auth_checkpoint(event_id, request, organizer=False):
    event = get_object_or_404(Event, pk=event_id)
    membership = None
    try:
        membership = EventMembership.objects.get(user=request.user, event=event)
    except EventMembership.DoesNotExist:
        messages.info(request, f"You don't have access to this event.  Please have an event organizer add you.")
        return event, membership, False
    if organizer:
        if not membership.is_organizer:
            messages.info(request, f"You must be an organizer to have access to this view.")
            return event, membership, False
    return event, membership, True


def validate_and_categorize_youtube_link(url, request):
    # Validation
    stripped_string = url.strip()
    if 'youtube.com/watch?v=' not in url[0:32].lower():
        messages.info(request, 'Only links from Youtube videos are allowed.')
        return False, False, False
    youtube_id = stripped_string.split('youtube.com/watch?v=')[1][0:11]
    if len(youtube_id) != 11:
        messages.info(request, 'The URL you pasted seems corrupted, try pasting the full video URL again!')
        return False, False, False

    # API call checking if embeddable
    try:
        response = requests.get(f"https://www.googleapis.com/youtube/v3/videos?id={youtube_id}&key={get_secret('YOUTUBE_API_KEY')}&part=status", timeout=3)
    except Timeout:
        messages.info(request, 'Internal connection failure to Youtube... if you see this problem, please let site staff know.')
        return False, False, False

    to_dict = json.loads(response.text)
    if len(to_dict['items']) == 0:
        messages.info(request, 'Youtube: Video ID is not valid.')
        return False, False, False
    else:
        is_embeddable = to_dict['items'][0]['status']['embeddable']
        return True, is_embeddable, youtube_id


def return_qty_price_select_field(max_pieces, item_price, item_packing, whole_cases=False):
    '''Taking in the item price, item packing, and maximum allowable pieces, this will return a nicely formatted list
    for Django's ChoiceField, which displays the total piece sum next to the piece count.'''

    choices_list = []
    if whole_cases == False:
        for i in range(max_pieces):
            choices_list.append((i + 1, f'{i + 1}/{item_packing} - ${round((i + 1) * (item_price / item_packing), 2)}'))
    else:
        for i in range(max_pieces):
            choices_list.append((i , f'{i} - ${round(i * item_price, 2)}'))
    return choices_list