from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model


class ProfileFollowingCreateViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(username='testuser', password='testpassword')
        self.another_user = get_user_model().objects.create_user(username='anotheruser', password='anotherpassword')

    def test_follow_unfollow(self):
        """Tests the basic functionality of following and unfollowing a user."""
        self.client.force_login(self.user)

        # Initially, the user is not following another_user
        response = self.client.post(reverse('follow', args=[self.another_user.id]))
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data['is_follower'])
        self.assertEqual(data['count_followers'], 1)

        # Now, the user is following another_user
        response = self.client.post(reverse('follow', args=[self.another_user.id]))
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertFalse(data['is_follower'])
        self.assertEqual(data['count_followers'], 0)

    def test_nonexistent_user_returns_404(self):
        """Tests that trying to follow/unfollow a non-existent user returns a 404 response."""
        self.client.force_login(self.user)
        response = self.client.post(reverse('follow', args=[999]))  # Assuming 999 is a non-existent user ID
        self.assertEqual(response.status_code, 404)
