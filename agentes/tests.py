from rest_framework.test import APITestCase
from django.urls import reverse
from .models import Agentes, Seguros

class AgentesTest(APITestCase):

    def setUp(self):
        self.usuario = Agentes.objects.create(
            username="Juan",
            email="juan@gmail.com"
        )
        self.usuario.set_password("juan24")
        self.usuario.save()
        response = self.client.post(reverse('token_obtain_pair'),
                                    {
                                        'username': "Juan",
                                        'password': "juan24"
                                    })
        self.access_token = response.data['access']
        self.refresh_token = response.data['refresh']
        
    def test_crear_cuenta(self):
        url = reverse('crear_cuenta')
        data = {
            "username": "Pedro",
            "email": "pedro@gmail.com",
            "password": "pedro24"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 201)

    def test_administrar_cuenta_put_200(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        url = reverse('administrar_cuenta')
        data = {
            "id": self.usuario.pk,
            "email": "juan24@gmail.com"
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, 200)

    def test_administrar_cuenta_put_400_serializer(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        url = reverse('administrar_cuenta')
        data = {
            "id": self.usuario.pk,
            "email": "juan24.com"
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, 400)
    
    def test_administrar_cuenta_put_403(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        url = reverse('administrar_cuenta')
        data = {
            "id": 2,
            "email": "juan24@gmail.com"
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, 403)

    def test_administrar_cuenta_put_400(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        url = reverse('administrar_cuenta')
        data = {
            "email": "juan24@gmail.com"
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, 400)

class SegurosTest(APITestCase):

    def setUp(self):
        self.usuario = Agentes.objects.create(
            username="Juan",
            email="juan@gmail.com"
        )
        self.seguros = Seguros.objects.create(
            nombre="Vida",
            descripcion="Te asegura la vida bro"
        )
        self.usuario.set_password("juan24")
        self.usuario.save()
        response = self.client.post(reverse('token_obtain_pair'),
                                    {
                                        'username': "Juan",
                                        'password': "juan24"
                                    })
        self.access_token = response.data['access']
        self.refresh_token = response.data['refresh']

    def test_seguros_post_400(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        url = reverse('seguros')
        data = {
            "seguros": ['Vido']
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 400)

    def test_seguros_post_400_sin_seguros(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        url = reverse('seguros')
        data = {
            "seguro": ['Vido']
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 400)

    def test_seguros_post_201(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        url = reverse('seguros')
        data = {
            "seguros": ['Vida']
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 201)