from __future__ import annotations as _annotations
from fastapi import Depends
from fastui.events import AuthEvent
from Worker.admin_panel.auth_user import User
from admin_panel.page import demo_page
from __future__ import annotations as _annotations
from typing import Annotated
from fastapi import APIRouter
from fastui import AnyComponent, FastUI
from fastui import components as c
from fastui.events import GoToEvent, PageEvent
from fastui.forms import Textarea, fastui_form
from models.messages import FormModel, LoginForm


router = APIRouter(tags=['Admin Panel'])


@router.post('/login', response_model=FastUI, response_model_exclude_none=True)
async def login_form_post(form: Annotated[LoginForm, fastui_form(LoginForm)]) -> list[AnyComponent]:
    user = User(email=form.email, extra={})
    token = user.encode_token()
    return [c.FireEvent(event=AuthEvent(token=token, url='/profile'))]


@router.post('/new', response_model=FastUI, response_model_exclude_none=True)
async def form_post(form: Annotated[FormModel, fastui_form(FormModel)]):
    print(form)
    return [c.FireEvent(event=GoToEvent(url='/'))]


@router.get('/profile', response_model=FastUI, response_model_exclude_none=True)
async def profile(user: Annotated[User, Depends(User.from_request)]) -> list[AnyComponent]:
    return demo_page(
        c.Paragraph(text=f'You are logged in as "{user.email}".'),
        c.Button(text='Logout', on_click=PageEvent(name='submit-form')),
        c.Link(
            components=[c.Text(text='Создать новый шаблон')],
            on_click=PageEvent(name='change-form', push_path='/new'),
            active='/new',
        ),
        c.Form(
            submit_url='/logout',
            form_fields=[c.FormFieldInput(name='test', title='', initial='data', html_type='hidden')],
            footer=[],
            submit_trigger=PageEvent(name='submit-form'),
        ),
        title='Authentication',
    )


@router.post('/logout', response_model=FastUI, response_model_exclude_none=True)
async def logout_form_post() -> list[AnyComponent]:
    return [c.FireEvent(event=AuthEvent(token=False, url='/login/password'))]
