import factory
from factory import fuzzy

from todo.models import Todo, TodoState


class TodoFactory(factory.Factory):
    class Meta:
        model = Todo

    title = factory.Faker('text')
    description = factory.Faker('text')
    state = fuzzy.FuzzyChoice(TodoState)
    user_id = 1
