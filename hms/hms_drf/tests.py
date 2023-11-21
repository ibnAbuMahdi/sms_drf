from django.test import TestCase
from .models import User
from ecommerce.models import Item, Order
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
from rest_framework.test import APITestCase
from rest_framework import status
# Create your tests here.

class HMSTestCase(APITestCase):

    client = APIClient()

    #  test case: signup
    def test_sign_up(self):
        dct = {'username': 'john', 'password': 'john@hms', 'role':'Doctor'}
        resp = self.client.post('signup/', dct, format='json')
        data = resp.data
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get('username'),'john')
        self.assertEqual(data.get('id'), 1)
        resp = self.client.post('signup/', dct, format='json')
        data = resp.data
        self.assertEqual(data.get('message'),'Unauthorized')
    #  test case: create login
    def test_login(self):
        dct = {'username': 'james', 'password': 'john@hms', 'role':'Doctor'}
        dct_2 = {'username': 'james', 'password': 'john@hms'}
        resp = self.client.post('signup/', dct, format='json')
        if resp.status == 200:
            response = self.client.post('login/', dct_2, format='json')
            self.assertEqual(response.data.get('message'), 'ok')

         
    #  test case: patient login
    def test_patient_login(self):
        dct = {'username': 'james', 'password': 'john@hms', 'role':'Patient'}
        resp = self.client.post('login', dct, format='json')
        if resp.status == 200:
            response = self.client.post('login/', dct, format='json')
            self.assertEqual(response.data.get('message'), 'ok')
    #  test case: book appointment
    def test_book_appointment(self):
        pass
    # test case: view patient
    def test_view_patient(self):
        pass
    # test case: view information
    def test_view_info(self):
        pass
    # test case: book multiple appointments
    def test_book_multi_appoints(self):
        pass
