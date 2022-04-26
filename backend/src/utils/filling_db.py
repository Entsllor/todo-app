from datetime import datetime, timedelta

from .. import crud, models
from ..core.database import db


def get_deadline_generator(init_number=1):
    i = init_number
    while True:
        yield datetime.now() + timedelta(i)
        i += 1


def clear_db():
    db.drop_all()
    db.create_all()


def fill_db():
    user_1 = crud.Users.create("user_1", "pass")
    user_2 = crud.Users.create("user_2", "pass")
    user_3 = crud.Users.create("user_3", "pass")
    db.session.add_all([user_1, user_2, user_3])
    db.session.flush()
    deadline_generator = get_deadline_generator()
    user_1_tasks = [
        models.Task(user_id=user_1.id, title="Шок", deadline=next(deadline_generator), is_completed=True),
        models.Task(user_id=user_1.id, title="Отрицание", deadline=next(deadline_generator), is_completed=True),
        models.Task(user_id=user_1.id, title="Злость", deadline=next(deadline_generator), is_completed=True),
        models.Task(user_id=user_1.id, title="Депрессия", deadline=next(deadline_generator), is_completed=True),
        models.Task(user_id=user_1.id, title="Обдумывание", deadline=next(deadline_generator), is_completed=False),
        models.Task(user_id=user_1.id, title="Вовлеченность", deadline=next(deadline_generator), is_completed=False),
        models.Task(user_id=user_1.id, title="Адаптация", deadline=next(deadline_generator), is_completed=False),
    ]

    deadline_generator = get_deadline_generator(-3)
    user_2_tasks = [
        models.Task(user_id=user_2.id, title="Написать backend", deadline=next(deadline_generator), is_completed=True),
        models.Task(user_id=user_2.id, title="Протестировать", deadline=next(deadline_generator), is_completed=True),
        models.Task(user_id=user_2.id, title="Написать frontend", deadline=next(deadline_generator),
                    is_completed=False),
        models.Task(user_id=user_2.id, title="запустить на vds", deadline=next(deadline_generator), is_completed=False),
    ]
    deadline_generator = get_deadline_generator(-2)
    user_3_tasks = [
        models.Task(user_id=user_3.id, title="Foo", deadline=next(deadline_generator), is_completed=True),
        models.Task(user_id=user_3.id, title="Bar", deadline=next(deadline_generator), is_completed=True),
        models.Task(user_id=user_3.id, title="Baz", deadline=next(deadline_generator), is_completed=False),
        models.Task(user_id=user_3.id, title="FooBaz", deadline=next(deadline_generator), is_completed=False),
    ]
    db.session.add_all([*user_1_tasks, *user_2_tasks, *user_3_tasks])
    db.session.commit()
