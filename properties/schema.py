import graphene
from graphene import ObjectType, String, Field, List, ID, Mutation, Boolean, Date, DateTime
from django.core.exceptions import ObjectDoesNotExist
from .models import Property, User, Booking


class PropertyType(ObjectType):
    id = ID()
    title = String()
    description = String()
    price = graphene.Decimal()
    location = String()
    created_at = DateTime()


class UserType(ObjectType):
    id = ID()
    username = String()
    first_name = String()
    last_name = String()
    email = String()
    joined_at = DateTime()


class BookingType(ObjectType):
    id = ID()
    user = Field(UserType)
    property = Field(PropertyType)
    start_date = Date()
    end_date = Date()
    booked_at = DateTime()


# --- User Mutations ---
class CreateUser(Mutation):
    class Arguments:
        username = String(required=True)
        first_name = String(required=True)
        last_name = String(required=True)
        email = String(required=True)

    user = Field(lambda: UserType)

    @staticmethod
    def mutate(root, info, username, first_name, last_name, email):
        user = User.objects.create(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
        )
        return CreateUser(user=user)


class UpdateUser(Mutation):
    class Arguments:
        id = ID(required=True)
        username = String()
        first_name = String()
        last_name = String()
        email = String()

    user = Field(lambda: UserType)

    @staticmethod
    def mutate(root, info, id, username=None, first_name=None, last_name=None, email=None):
        try:
            user = User.objects.get(pk=id)
        except ObjectDoesNotExist:
            raise Exception("User not found")
        if username is not None:
            user.username = username
        if first_name is not None:
            user.first_name = first_name
        if last_name is not None:
            user.last_name = last_name
        if email is not None:
            user.email = email
        user.save()
        return UpdateUser(user=user)


class DeleteUser(Mutation):
    class Arguments:
        id = ID(required=True)

    ok = Boolean()

    @staticmethod
    def mutate(root, info, id):
        try:
            user = User.objects.get(pk=id)
            user.delete()
            return DeleteUser(ok=True)
        except ObjectDoesNotExist:
            return DeleteUser(ok=False)


# --- Booking Mutations ---
class CreateBooking(Mutation):
    class Arguments:
        user_id = ID(required=True)
        property_id = ID(required=True)
        start_date = Date(required=True)
        end_date = Date(required=True)

    booking = Field(lambda: BookingType)

    @staticmethod
    def mutate(root, info, user_id, property_id, start_date, end_date):
        try:
            user = User.objects.get(pk=user_id)
            prop = Property.objects.get(pk=property_id)
        except ObjectDoesNotExist as e:
            raise Exception(f"Related object not found: {e}")

        booking = Booking.objects.create(
            user=user,
            property=prop,
            start_date=start_date,
            end_date=end_date,
        )
        return CreateBooking(booking=booking)


class UpdateBooking(Mutation):
    class Arguments:
        id = ID(required=True)
        user_id = ID()
        property_id = ID()
        start_date = Date()
        end_date = Date()

    booking = Field(lambda: BookingType)

    @staticmethod
    def mutate(root, info, id, user_id=None, property_id=None, start_date=None, end_date=None):
        try:
            booking = Booking.objects.get(pk=id)
        except ObjectDoesNotExist:
            raise Exception("Booking not found")

        if user_id is not None:
            try:
                booking.user = User.objects.get(pk=user_id)
            except ObjectDoesNotExist:
                raise Exception("User not found")
        if property_id is not None:
            try:
                booking.property = Property.objects.get(pk=property_id)
            except ObjectDoesNotExist:
                raise Exception("Property not found")
        if start_date is not None:
            booking.start_date = start_date
        if end_date is not None:
            booking.end_date = end_date
        booking.save()
        return UpdateBooking(booking=booking)


class DeleteBooking(Mutation):
    class Arguments:
        id = ID(required=True)

    ok = Boolean()

    @staticmethod
    def mutate(root, info, id):
        try:
            booking = Booking.objects.get(pk=id)
            booking.delete()
            return DeleteBooking(ok=True)
        except ObjectDoesNotExist:
            return DeleteBooking(ok=False)


# --- Property Mutations (optional) ---
class CreateProperty(Mutation):
    class Arguments:
        title = String(required=True)
        description = String(required=True)
        price = graphene.Decimal(required=True)
        location = String(required=True)

    property = Field(lambda: PropertyType)

    @staticmethod
    def mutate(root, info, title, description, price, location):
        prop = Property.objects.create(
            title=title,
            description=description,
            price=price,
            location=location,
        )
        return CreateProperty(property=prop)


class UpdateProperty(Mutation):
    class Arguments:
        id = ID(required=True)
        title = String()
        description = String()
        price = graphene.Decimal()
        location = String()

    property = Field(lambda: PropertyType)

    @staticmethod
    def mutate(root, info, id, title=None, description=None, price=None, location=None):
        try:
            prop = Property.objects.get(pk=id)
        except ObjectDoesNotExist:
            raise Exception("Property not found")
        if title is not None:
            prop.title = title
        if description is not None:
            prop.description = description
        if price is not None:
            prop.price = price
        if location is not None:
            prop.location = location
        prop.save()
        return UpdateProperty(property=prop)


class DeleteProperty(Mutation):
    class Arguments:
        id = ID(required=True)

    ok = Boolean()

    @staticmethod
    def mutate(root, info, id):
        try:
            prop = Property.objects.get(pk=id)
            prop.delete()
            return DeleteProperty(ok=True)
        except ObjectDoesNotExist:
            return DeleteProperty(ok=False)


class Query(ObjectType):
    property = Field(PropertyType, id=ID(required=True))
    all_properties = List(PropertyType)

    user = Field(UserType, id=ID(required=True))
    all_users = List(UserType)

    booking = Field(BookingType, id=ID(required=True))
    all_bookings = List(BookingType)

    @staticmethod
    def resolve_property(root, info, id):
        try:
            return Property.objects.get(pk=id)
        except ObjectDoesNotExist:
            return None

    @staticmethod
    def resolve_all_properties(root, info):
        return Property.objects.all()

    @staticmethod
    def resolve_user(root, info, id):
        try:
            return User.objects.get(pk=id)
        except ObjectDoesNotExist:
            return None

    @staticmethod
    def resolve_all_users(root, info):
        return User.objects.all()

    @staticmethod
    def resolve_booking(root, info, id):
        try:
            return Booking.objects.get(pk=id)
        except ObjectDoesNotExist:
            return None

    @staticmethod
    def resolve_all_bookings(root, info):
        return Booking.objects.select_related('user', 'property').all()


class Mutation(ObjectType):
    create_user = CreateUser.Field()
    update_user = UpdateUser.Field()
    delete_user = DeleteUser.Field()

    create_booking = CreateBooking.Field()
    update_booking = UpdateBooking.Field()
    delete_booking = DeleteBooking.Field()

    create_property = CreateProperty.Field()
    update_property = UpdateProperty.Field()
    delete_property = DeleteProperty.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)

