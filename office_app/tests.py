from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Topic, Room, Message

class ViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.client.login(username='testuser', password='password123')

        # Topic Tests 
        self.topic1 = Topic.objects.create(name='Test Topic 1')
        self.topic2 = Topic.objects.create(name='Test Topic 2')

        # Room Tests
        self.room1 = Room.objects.create(host=self.user, topic=self.topic1, name='Test Room 1', description='Description for Test Room 1')
        self.room2 = Room.objects.create(host=self.user, topic=self.topic2, name='Test Room 2', description='Description for Test Room 2')

        # Message Tests 
        self.message1 = Message.objects.create(user=self.user, room=self.room1, body='Test Message 1')
        self.message2 = Message.objects.create(user=self.user, room=self.room2, body='Test Message 2')

    def test_home_view(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'base/home.html')

    def test_login_view(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'base/register-login.html')

    def test_room_view(self):
        response = self.client.get(reverse('room', kwargs={'pk': self.room1.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'base/group.html')

    def test_user_profile_view(self):
        response = self.client.get(reverse('user-profile', kwargs={'pk': self.user.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'base/profile.html')

    def test_create_group_view(self):
        response = self.client.get(reverse('create-group'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'base/group-form.html')

    def test_update_room_view(self):
        response = self.client.get(reverse('update-room', kwargs={'pk': self.room1.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'base/group-form.html')

    def test_delete_room_view(self):
        response = self.client.get(reverse('delete-room', kwargs={'pk': self.room1.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'base/delete.html')

    def test_delete_message_view(self):
        response = self.client.get(reverse('delete-message', kwargs={'pk': self.message1.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'base/delete.html')

class TopicModelTestCase(TestCase):
    def setUp(self):
        self.topic = Topic.objects.create(name="Test Topic")

    def test_topic_creation(self):
        self.assertEqual(self.topic.name, "Test Topic")

    def test_topic_str_method(self):
        self.assertEqual(str(self.topic), "Test Topic")

class RoomModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="test_user", password="password123")
        self.topic = Topic.objects.create(name="Test Topic")
        self.room = Room.objects.create(
            host=self.user,
            topic=self.topic,
            name="Test Room",
            description="This is a test room"
        )

    def test_room_creation(self):
        self.assertEqual(self.room.host, self.user)
        self.assertEqual(self.room.topic, self.topic)
        self.assertEqual(self.room.name, "Test Room")
        self.assertEqual(self.room.description, "This is a test room")

    def test_room_str_method(self):
        self.assertEqual(str(self.room), "Test Room")

class MessageModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="test_user", password="password123")
        self.topic = Topic.objects.create(name="Test Topic")
        self.room = Room.objects.create(
            host=self.user,
            topic=self.topic,
            name="Test Room",
            description="This is a test room"
        )
        self.message = Message.objects.create(
            user=self.user,
            room=self.room,
            body="This is a test message"
        )

    def test_message_creation(self):
        self.assertEqual(self.message.user, self.user)
        self.assertEqual(self.message.room, self.room)
        self.assertEqual(self.message.body, "This is a test message")

    def test_message_str_method(self):
        self.assertEqual(str(self.message), "This is a test message")