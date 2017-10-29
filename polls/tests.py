from django.test import TestCase
from django.utils import timezone
from django.utils.html import escape

from .models import Question


def add_question(question_text="What's up?"):
    now = timezone.now()
    q = Question(question_text=question_text, pub_date=now)
    q.save()
    return q


class PollsModel(TestCase):

    def test_questions_string(self):
        q = add_question()
        self.assertEqual(q.question_text, str(q))

    def test_questions_have_recent_property(self):
        q = add_question()
        self.assertTrue(q.was_published_recently())

    def test_questions_can_be_retrieved_by_primary_key(self):
        q = add_question()
        self.assertEqual(Question.objects.get(pk=q.id), q)

    def test_can_attach_choices(self):
        q = add_question()
        q.choice_set.create(choice_text='Not much', votes=0)
        q.choice_set.create(choice_text='The sky', votes=0)
        c = q.choice_set.create(choice_text='Just hacking again', votes=0)
        self.assertEqual(c.question, q)
        self.assertEqual(q.choice_set.count(), 3)


class PollsView(TestCase):

    def test_route_to_polls(self):
        response = self.client.get('/polls/')
        self.assertEqual(response.status_code, 200)

    def test_polls_list_returns_message_when_no_questions(self):
        response = self.client.get('/polls/')
        self.assertContains(response, escape("No polls are available."), html=True)

    def test_polls_lists_5_most_recent(self):
        questions = [
            "How long is a piece of string?",
            "How are you today?",
            "What have you done yesterday?",
            "What's your mother's maiden name?",
            "When is your birthday?",
            "Are you happy?",
            "What is the meaning of life?"
        ]
        for question in questions:
            add_question(question)

        response = self.client.get('/polls/')
        for question in questions[-5:]:
            self.assertContains(response, escape(question), html=True)

        for question in questions[:2]:
            self.assertNotContains(response, escape(question), html=True)

    def test_question_details(self):
        response = self.client.get('/polls/5/')
        self.assertEqual(response.status_code, 200)

    def test_question_results_details(self):
        response = self.client.get('/polls/5/results/')
        self.assertEqual(response.status_code, 200)

    def test_question_vote_details(self):
        response = self.client.get('/polls/5/vote/')
        self.assertEqual(response.status_code, 200)
