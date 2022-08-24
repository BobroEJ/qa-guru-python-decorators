import re
import types
import allure

from functools import wraps


def humanify(name: str):
    return ' '.join(re.split('_+', name))


def step(fn):
    @allure.step(humanify(fn.__name__))
    @wraps(fn)
    def fn_with_logging(*args, **kwargs):
        """
        заменил, потому что при добавлении аргумента в функцию given_sign_up_form_opened, а не в метод, вываливается
        ошибка AttributeError

        is_method = (
                args
                and isinstance(args[0], object)
                and isinstance(getattr(args[0], fn.__name__), types.MethodType)
        )
        """
        try:
            is_method = isinstance(getattr(args[0], fn.__name__), types.MethodType)
        except:
            is_method = False

        args_to_log = args[1:] if is_method else args
        args_and_kwargs_to_log_as_strings = [
            *args_to_log,
            *[f'{key} = {value}' for key, value in kwargs.items()]
        ]
        args_and_kwargs_string = (
            ', '.join(map(str, args_and_kwargs_to_log_as_strings))
            if args_and_kwargs_to_log_as_strings
            else ''
        )
        if is_method:
            with allure.step(f'Method of {args[0].__class__.__name__}'):
                pass

        if args_and_kwargs_string:
            allure.attach(f'{args_and_kwargs_string}', 'Human-readable args and kwargs', allure.attachment_type.TEXT)

        print(
            (f'[{args[0].__class__.__name__}] ' if is_method else '')
            + humanify(fn.__name__)
            + args_and_kwargs_string
        )

        return fn(*args, **kwargs)

    return fn_with_logging


class SignUpForm:

    @step
    def fill_name(self, first_name, surname):
        pass
        return self

    @step
    def fill_email(self, value):
        pass
        return self

    @step
    def fill_password(self, value):
        pass
        return self

    @step
    def submit(self):
        pass
        return self


class DashBoard:
    @step
    def go_to_profile(self):
        ...


@step
def given_sign_up_form_opened(arg):
    print(arg)
    ...


sign_up_form = SignUpForm()
dashboard = DashBoard()


def test_allure_notifications():
    given_sign_up_form_opened('test')
    (sign_up_form
     .fill_name('zhenya', surname='tverdun')
     .fill_email('tverdune@ya.ru')
     .fill_password('qwerty')
     .submit()
     )
    dashboard.go_to_profile()
