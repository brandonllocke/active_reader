import json

from django.test import TestCase
from rest_framework.test import APIClient


class BookTestCase(TestCase):
    ACTIVE = 'active'
    API_ENDPOINT = '/api/books/'
    ERROR = 'error'
    DATA = 'data'
    PRIMARY_TITLE = 'The Cool Bean'
    SECONDARY_TITLE = 'The Smart Cookie'
    STATUS = 'status'
    SUCCESS = 'success'
    TITLE = 'title'

    def test_list_none(self):
        client = APIClient()
        response = client.get(self.API_ENDPOINT)
        content = json.loads(response.content)
        self._assertSuccess(content)
        self.assertEquals(len(content[self.DATA]), 0)

    def test_add_book(self):
        self._successfully_add_book(self.PRIMARY_TITLE)

    def test_list_one(self):
        self._successfully_add_book(self.PRIMARY_TITLE)
        client = APIClient()
        response = client.get(self.API_ENDPOINT)
        content = json.loads(response.content)
        self._assertSuccess(content)
        self.assertEquals(len(content[self.DATA]), 1)

    def test_edit_active(self):
        self._successfully_add_book(self.PRIMARY_TITLE)
        client = APIClient()
        data = {self.ACTIVE: False}
        response = client.post(f'{self.API_ENDPOINT}1', data)
        content = json.loads(response.content)
        self._assertSuccess(content)
        self._assertTitle(content, self.PRIMARY_TITLE)
        self._assertActive(content, False)

    def test_add_two_of_same_title(self):
        self._successfully_add_book(self.PRIMARY_TITLE)
        client = APIClient()
        data = {self.TITLE: self.PRIMARY_TITLE}
        response = client.post(self.API_ENDPOINT, data)
        content = json.loads(response.content)
        self._assertFailure(content)

    def test_add_two_books(self):
        self._successfully_add_book(self.PRIMARY_TITLE)
        self._successfully_add_book(self.SECONDARY_TITLE)
        client = APIClient()
        response = client.get(self.API_ENDPOINT)
        content = json.loads(response.content)
        self._assertSuccess(content)
        self.assertEquals(len(content[self.DATA]), 2)

    def test_change_title_fails(self):
        self._successfully_add_book(self.PRIMARY_TITLE)
        client = APIClient()
        data = {self.TITLE: self.SECONDARY_TITLE}
        response = client.post(f'{self.API_ENDPOINT}1', data)
        content = json.loads(response.content)
        self._assertFailure(content)
        self._assertValidationErrorMessage(content, self.TITLE, "Cannot update book title after creation.")

    def _successfully_add_book(self, title):
        content = self._add_book(title)
        self._assertBookAdded(content, title)

    def _add_book(self, title):
        client = APIClient()
        data = {self.TITLE: title}
        response = client.post(self.API_ENDPOINT, data)
        return json.loads(response.content)

    def _assertBookAdded(self, content, title):
        self._assertSuccess(content)
        self._assertTitle(content, title)
        self._assertActive(content, True)

    def _assertSuccess(self, content):
        self.assertEqual(content[self.STATUS], self.SUCCESS, "Did not receive success status")

    def _assertFailure(self, content):
        self.assertEqual(content[self.STATUS], self.ERROR, "Did not receive error status")

    def _assertTitle(self, content, title):
        self.assertEqual(content[self.DATA][self.TITLE], title)

    def _assertActive(self, content, active):
        self.assertEqual(content[self.DATA][self.ACTIVE], active)

    def _assertValidationErrorMessage(self, content, field_name, message):
        self.assertEqual(content[self.DATA][field_name], [message])
