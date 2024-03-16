from django.test import TestCase, Client
from django.urls import reverse
from .models import RoomMember
import json

class ViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_lobby_view(self):
        response = self.client.get(reverse('lobby'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'base/lobby.html')

    def test_room_view(self):
        response = self.client.get(reverse('room'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'base/room.html')

    def test_getToken_view(self):
        response = self.client.get(reverse('getToken'), {'channel': 'test_channel'})
        self.assertEqual(response.status_code, 200)
        self.assertTrue('token' in response.json())
        self.assertTrue('uid' in response.json())

    def test_createMember_view(self):
        data = {
            'name': 'Test Name',
            'UID': '12345',
            'room_name': 'Test Room'
        }
        response = self.client.post(reverse('createMember'), json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(RoomMember.objects.count(), 1)
        self.assertEqual(RoomMember.objects.get().name, 'Test Name')

    def test_getMember_view(self):
        member = RoomMember.objects.create(name='Test Name', uid='12345', room_name='Test Room')
        response = self.client.get(reverse('getMember'), {'UID': '12345', 'room_name': 'Test Room'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['name'], 'Test Name')

    def test_deleteMember_view(self):
        member = RoomMember.objects.create(name='Test Name', uid='12345', room_name='Test Room')
        data = {
            'name': 'Test Name',
            'UID': '12345',
            'room_name': 'Test Room'
        }
        response = self.client.post(reverse('deleteMember'), json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(RoomMember.objects.count(), 0)