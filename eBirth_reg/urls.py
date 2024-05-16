from django.urls import path

from eBirth_reg.views import (
    BirthRegistrationView,
    ManageBirthRegistrationView,
    EditBirthRegistrationView,
    DeleteBirthRegistrationView,

    DeathRegistrationView,
    ManageDeathRegistrationView,
    EditDeathRegistrationView,
    DeleteDeathRegistrationView,

    AdminRegistrationView,
    ManageAdministratorsView,
    DeleteAdministratorView,
    EditAdminView,

    CertificateView,
    DeathCertificateView,

    EditHospitalProfileView,
    AccountProfileView,
    ChangePasswordView,

    SearchCertificateView,
)

app_name = "reg"

urlpatterns = [
    path('birth_reg', BirthRegistrationView.as_view(), name="birth_reg"),
    path('manage_birth_reg', ManageBirthRegistrationView.as_view(), name="manage_birth_reg"),
    path('edit_birth_reg/<str:pk>', EditBirthRegistrationView.as_view(), name="edit_birth_reg"),
    path('delete_birth_reg/<str:pk>', DeleteBirthRegistrationView.as_view(), name="delete_birth_reg"),
    path('certificate/<str:pk>', CertificateView.as_view(), name="certificate"),

    path('death_reg', DeathRegistrationView.as_view(), name="death_reg"),
    path('manage_death_reg', ManageDeathRegistrationView.as_view(), name="manage_death_reg"),
    path('edit_death_reg/<str:pk>', EditDeathRegistrationView.as_view(), name="edit_death_reg"),
    path('delete_death_reg/<str:pk>', DeleteDeathRegistrationView.as_view(), name="delete_death_reg"),
    path('death_certificate/<str:pk>', DeathCertificateView.as_view(), name="death_certificate"),

    path('admin_reg', AdminRegistrationView.as_view(), name="admin_reg"),
    path('manage_admin', ManageAdministratorsView.as_view(), name="manage_admin"),
    path('delete_admin/<str:pk>', DeleteAdministratorView.as_view(), name="delete_admin"),
    path('edit_admin/<str:pk>', EditAdminView.as_view(), name="edit_admin"),


    path('hospital_profile/<str:pk>', EditHospitalProfileView.as_view(), name="hospital_profile"),
    path('account_profile/<str:pk>', AccountProfileView.as_view(), name="account_profile"),

    path('search', SearchCertificateView.as_view(), name="search"),

    path('change_password/<str:pk>', ChangePasswordView.as_view(), name="change_password"),
]

