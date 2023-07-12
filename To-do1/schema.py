import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from models import User as UserModel, Todo as TodoModel
from models import db


class User(SQLAlchemyObjectType):
    class Meta:
        model = UserModel
        interfaces = (graphene.relay.Node,)


class Todo(SQLAlchemyObjectType):
    class Meta:
        model = TodoModel
        interfaces = (graphene.relay.Node,)


class CreateUser(graphene.Mutation):
    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)

    user = graphene.Field(User)

    def mutate(self, info, username, password):
        user = UserModel(username=username, password=password)
        db.session.add(user)
        db.session.commit()

        return CreateUser(user=user)


class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()


class Query(graphene.ObjectType):
    node = graphene.relay.Node.Field()
    all_todos = SQLAlchemyConnectionField(Todo.connection)


schema = graphene.Schema(query=Query, mutation=Mutation)
