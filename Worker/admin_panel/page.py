from fastui import AnyComponent
from fastui import components as c
from fastui.events import GoToEvent


def demo_page(*components: AnyComponent, title: str | None = None) -> list[AnyComponent]:
    return [
        c.PageTitle(text=f'Admin Panel — {title}' if title else 'Создание шаблонов для рассылки сообщений'),
        c.Navbar(
            title='Admin Panel',
            title_event=GoToEvent(url='/'),
            start_links=[
                c.Link(
                    components=[c.Text(text='Auth')],
                    on_click=GoToEvent(url='/auth/login/password'),
                    active='startswith:/auth',
                ),
            ],
        ),
        c.Page(
            components=[
                *((c.Heading(text=title),) if title else ()),
                *components,
            ],
        ),
        c.Footer(
            extra_text='Admin Panel'
        ),
    ]
