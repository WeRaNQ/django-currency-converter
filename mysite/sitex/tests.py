from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from sitex.forms import RegisterForm, LoginForm

User = get_user_model()


class PageTests(TestCase):
    def test_register_page(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register.html')

    def test_login_page(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')


class FormTests(TestCase):
    def test_register_form_valid(self):
        form = RegisterForm(data={
            'email': 'new_form_test@example.com',
            'nickname': 'newuser',
            'password1': 'QwErTy!2345',
            'password2': 'QwErTy!2345',
        })
        self.assertTrue(form.is_valid(), form.errors)

    def test_register_form_passwords_dont_match(self):
        form = RegisterForm(data={
            'email': 'new_form_test2@example.com',
            'nickname': 'newuser2',
            'password1': 'QwErTy!2345',
            'password2': 'Different!9876',
        })
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)

    def test_login_form_valid(self):
        form = LoginForm(data={
            'email': 'test@example.com',
            'password': 'QwErTy!2345',
        })
        self.assertTrue(form.is_valid(), form.errors)


class RegistrationFlowTest(TestCase):
    def test_register_and_login(self):
        # 1. Регистрация
        response = self.client.post(reverse('register'), {
            'email': 'flow_unique_123@example.com',
            'nickname': 'flowuser',
            'password1': 'QwErTy!2345',
            'password2': 'QwErTy!2345',
        })
        # Отладка: если не 302 — покажет ошибки формы
        if response.status_code != 302:
            print("REGISTER STATUS:", response.status_code)
            if response.context and 'form' in response.context:
                print("FORM ERRORS:", response.context['form'].errors)

        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            User.objects.filter(email='flow_unique_123@example.com').exists()
        )

        # 2. Логин
        response = self.client.post(reverse('login'), {
            'email': 'flow_unique_123@example.com',
            'password': 'QwErTy!2345',
        })
        if response.status_code != 302:
            print("LOGIN STATUS:", response.status_code)
            if response.context and 'form' in response.context:
                print("FORM ERRORS:", response.context['form'].errors)

        self.assertEqual(response.status_code, 302)