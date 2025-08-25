from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.views import APIView
from rest_framework import viewsets, mixins
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.core.mail import send_mail

from apps.core.utils.send_mail import send_email
from apps.users.models import User
from apps.users.serializers.user_loan_serializers import LoanUserSerializer
from apps.users.serializers.user_serializers import (
    UserRegisterSerializer,
    UserSerializer,
    UserUpdateSerializer,
)


class RegisterView(APIView):
    @swagger_auto_schema(
        operation_summary="Register user information",
        operation_description="It takes a set of data that defines a user and creates a record in the system database, users whose role is student or teacher can register.",
        request_body=UserRegisterSerializer,
        responses={
            201: openapi.Response(
                "Usuario creado exitosamente", UserRegisterSerializer
            ),
            400: "Error en la solicitud. Verifica los datos.",
        },
    )
    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Obtain authenticated user information",
        operation_description="Returns the authenticated user information using the JWT token in the header.",
        responses={200: UserSerializer},
    )
    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_summary="Update authenticated user data",
        operation_description="It receives the user's information and updates it. A JWT must be sent in the header.",
        request_body=UserUpdateSerializer,
        responses={
            200: openapi.Response("User successfully updated", UserUpdateSerializer),
            400: "Error in the request. Please check the data you have submitted.",
        },
    )
    def put(self, request):
        user = User.objects.get(id=request.user.id)
        serializer = UserUpdateSerializer(user, request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SendEmailTest(APIView):

    def get(self, request):
        user = User.objects.get(id=request.user.id)
        print(user.email)
        # Enviar correo al cliente
        subject = "Actualización de tu préstamo TEST"
        message = (
            f"Hola {user.first_name},\n\n"
            f"Se ha aplicado un interés mensual de ${0:,.2f} "
            f"a tu préstamo con codigo XXX.\n\n"
            f"Tu nuevo saldo de intereses es: ${0:,.2f}.\n"
            f"Tu saldo de capital es: ${0:,.2f}.\n\n"
            "Por favor mantente al día con tus pagos."
        )
        recipient = user.email
        try:
            # response = send_email(recipient, subject, message)
            response = send_email(
                recipient,
                subject,
                message,
            )
            print(response)
            print(f"Correo enviado a {user.email}")
        except Exception as e:
            print(f"Error enviando correo a {user.email}: {e}")
        return Response("Send Email Test")


class UserViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    """
    API endpoint to list, view, update, and delete users.
    """

    permission_classes = [IsAuthenticated]
    queryset = User.objects.filter(is_active=True, rol="guest")
    serializer_class = LoanUserSerializer
