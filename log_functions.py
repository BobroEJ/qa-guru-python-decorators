import re
import types
from functools import wraps


def humanify(name: str):
    return ' '.join(re.split('_+', name))


def step(fn):
    @wraps(fn)
    def fn_with_logging(*args, **kwargs):
        is_method = (
                args
                and isinstance(args[0], object)
                and isinstance(getattr(args[0], fn.__name__), types.MethodType)
        )

        args_to_log = args[1:] if is_method else args
        args_and_kwargs_to_log_as_strings = [
            *args_to_log,
            *[f'{key} = {value}' for key, value in kwargs.items()]
        ]
        args_and_kwargs_string = (
            ': ' + ', '.join(map(str, args_and_kwargs_to_log_as_strings))
              if args_and_kwargs_to_log_as_strings
              else ''
        )

        print(
            (f'[{args[0].__class__.__name__}] ' if is_method else '')
            + humanify(fn.__name__)
            + args_and_kwargs_string
        )

        return fn(*args, **kwargs)

    return fn_with_logging


@step
def given_sign_up_form_opened():
    # print(given_sign_up_form_opened.__name__)
    ...


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


sign_up_form = SignUpForm()
dashboard = DashBoard()

given_sign_up_form_opened()
(sign_up_form
 .fill_name('zhenya', surname='tverdun')
 .fill_email(value='tverdune@ya.ru')
 .fill_password('qwerty')
 .submit()
 )
dashboard.go_to_profile()
