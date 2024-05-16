from django.shortcuts import render, reverse, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.views import View
from django.contrib.messages.views import SuccessMessageMixin
from random import choice, randint, shuffle
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from django.http import Http404
from django.contrib.auth.mixins import LoginRequiredMixin


# My App imports
from eBirth_reg.models import (
    HospitalProfile,
    HospitalAdminProfile,
    BirthRegistration,
    DeathRegistration,
)

from eBirth_auth.models import (
    User,
)
from eBirth_auth.forms import (
    UserRegistrationForm,
    EditAdminForm,
    ChangePassForm,
)

from eBirth_reg.forms import (
    BirthRegistrationForm,
    DeathRegistrationForm,
    HospitalProfileForm,
)

DEFAULT_PASSWORD = '12345678'

# Create your views here.


def _cert():
    letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L',
               'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

    cert_list = ['M', 'H', 'S', '-']

    [cert_list.append(choice(letters)) for _ in range(3)]
    [cert_list.append(choice(numbers)) for _ in range(3)]

    shuffle(list(cert_list))
    cert = ''.join(cert_list)

    return cert


def _nin():

    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

    nin_list = []

    [nin_list.append(choice(numbers)) for _ in range(10)]
    shuffle(list(nin_list))

    nin = ''.join(nin_list)

    return nin


def generate_nin():
    exists = True
    nin = None

    while exists:
        nin = _nin()
        if not User.objects.filter(nin=nin).exists():
            exists = False

    return nin


def generate_cert():
    exists = True
    cert = None

    while exists:
        cert = _cert()
        if not User.objects.filter(cert_no=cert).exists():
            exists = False

    return cert


def generate_death_cert():
    exists = True
    cert = None

    while exists:
        cert = _cert()
        if not User.objects.filter(cert_no=cert).exists() and not DeathRegistration.objects.filter(certificate_num=cert).exists():
            exists = False

    return cert


class BirthRegistrationView(LoginRequiredMixin, SuccessMessageMixin, CreateView):

    model = BirthRegistration
    form_class = BirthRegistrationForm
    template_name = "auth/birth_reg.html"
    success_message = ""

    def get_success_url(self):
        return reverse("reg:birth_reg")

    def form_valid(self, form):

        place_of_birth = None

        try:
            place_of_birth = HospitalProfile.objects.get(
                user_id=self.request.user)

        except HospitalProfile.DoesNotExist:
            admin_profile = HospitalAdminProfile.objects.filter(
                user_id=self.request.user)

            if admin_profile.exists():
                place_of_birth = admin_profile[0].hospital_id

            else:
                messages.error(self.request, "Unable to get hospital profile!")
                return super().form_invalid(form)
        finally:

            nin = generate_nin()
            cert = generate_cert()

            user_id = User.objects.create_user(
                password=DEFAULT_PASSWORD, nin=nin)

            form.instance.user_id = user_id
            form.instance.place_of_birth = place_of_birth
            form.instance.certificate_num = cert

            self.success_message = f"Birth Registration Successful with NIN No: {nin}"

            return super().form_valid(form)


class ManageBirthRegistrationView(LoginRequiredMixin, ListView):
    template_name = "auth/manage_reg.html"

    def get_queryset(self):
        hospital = None

        try:
            hospital = HospitalProfile.objects.get(
                user_id=self.request.user).hospital_id

        except HospitalProfile.DoesNotExist:

            try:
                hospital = HospitalAdminProfile.objects.get(
                    user_id=self.request.user).hospital_id
            except HospitalAdminProfile.DoesNotExist:
                messages.error(
                    self.request, "Contact Central Mgt, profile doesn't exist!!, therefore birth-registration list can't be displayed")
                return None

        finally:
            queryset = BirthRegistration.objects.filter(
                place_of_birth=hospital).order_by('-date_issue')
            return queryset

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if queryset is None:
            return redirect(reverse('auth:dashboard'))
        return super().get(request, *args, **kwargs)


class EditBirthRegistrationView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = BirthRegistration
    form_class = BirthRegistrationForm
    secondary_form_class = DeathRegistrationForm
    success_message = "Registration has been edited successfully!"

    template_name = "auth/edit_birth_reg.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form2"] = self.secondary_form_class
        return context

    def get_success_url(self):
        return reverse("reg:manage_birth_reg")


class DeleteBirthRegistrationView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = BirthRegistration
    success_message = "Registration has been deleted successfully!"

    def form_valid(self, form):
        user = User.objects.get(nin=self.request.POST.get('nin'))
        user.delete()

        return super().form_valid(form)

    def get_success_url(self):
        return reverse("reg:manage_birth_reg")


class DeathRegistrationView(View):
    template_name = "auth/death_reg.html"

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):

        if 'search' in request.POST:
            nin = request.POST['nin']
            form_class = DeathRegistrationForm

            try:
                # get user
                user_record = User.objects.get(nin=nin)
                birth = BirthRegistration.objects.get(
                    user_id=user_record.user_id)

                context = {
                    'record': 'record',
                    'nin': nin,
                    'birth': birth,
                    'form': form_class,
                    'user_record': user_record
                }

                return render(request, self.template_name, context=context)

            except User.DoesNotExist:
                messages.error(request, "Invalid NIN")
                return render(request, self.template_name, context={'nin': nin})

            except BirthRegistration.DoesNotExist:
                messages.error(request, "Failed to fetch user record")
                return render(request, self.template_name, context={'nin': nin})

        if 'register' in request.POST:
            form = DeathRegistrationForm(request.POST)
            hospital_issued = None

            try:
                hospital_issued = HospitalProfile.objects.get(
                    user_id=self.request.user)

            except HospitalProfile.DoesNotExist:
                admin_profile = HospitalAdminProfile.objects.filter(
                    user_id=self.request.user)

                if admin_profile.exists():
                    hospital_issued = admin_profile[0].hospital_id

                else:
                    messages.error(
                        self.request, "Unable to get hospital profile!")
                    return super().form_invalid(form)
            finally:

                if form.is_valid():

                    data = form.save(commit=False)

                    cert = generate_death_cert()
                    nin = request.POST['nin']
                    user_id = User.objects.get(nin=nin)
                    birth_id = BirthRegistration.objects.get(certificate_num=user_id.nin)

                    data.user_id = user_id
                    data.birth_id = birth_id
                    data.hospital_issued = hospital_issued
                    data.certificate_num = cert

                    if not DeathRegistration.objects.filter(user_id=user_id).exists():

                        data.save()
                        message = f"Registration already exist: {nin}"
                        messages.success(request, message)
                        return redirect("reg:death_reg")

                    message = f"Death Registration already exist with this NIN No: {nin}"
                    messages.error(request, message)
                    return render(request, self.template_name, context={'form':form, 'nin':nin})

                messages.error(request, f'{form.errors.as_text()}')
                return render(request, self.template_name, context={'form':form, 'nin':nin})

class ManageDeathRegistrationView(LoginRequiredMixin, ListView):
    template_name = "auth/manage_death.html"

    def get_queryset(self):
        hospital = None

        try:
            hospital = HospitalProfile.objects.get(
                user_id=self.request.user).hospital_id

        except HospitalProfile.DoesNotExist:

            try:
                hospital = HospitalAdminProfile.objects.get(
                    user_id=self.request.user).hospital_id
            except HospitalAdminProfile.DoesNotExist:
                messages.error(
                    self.request, "Contact Central Mgt, profile doesn't exist!!, therefore death-registration list can't be displayed")
                return None

        finally:
            queryset = DeathRegistration.objects.filter(
                hospital_issued=hospital).order_by('-date_issue')
            return queryset

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if queryset is None:
            return redirect(reverse('auth:dashboard'))
        return super().get(request, *args, **kwargs)

class EditDeathRegistrationView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = DeathRegistration
    form_class = DeathRegistrationForm
    success_message = "Death Registration has been edited successfully!"

    template_name = "auth/edit_death_reg.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_success_url(self):
        return reverse("reg:manage_death_reg")

class DeleteDeathRegistrationView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = DeathRegistration
    success_message = "Registration has been deleted successfully!"

    def get_success_url(self):
        return reverse("reg:manage_death_reg")


class AdminRegistrationView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = "auth/admin_reg.html"
    success_message = "Admin Account created!"

    def get_success_url(self):
        return reverse("reg:admin_reg")

    def form_valid(self, form):
        form.instance.is_hospital_admin = True

        try:
            hospital = HospitalProfile.objects.get(
                user_id=self.request.user)

            print(f'hospital: {hospital}')

            # hospital = HospitalAdminProfile.objects.get(
            #     user_id=self.request.user).hospital_id

            form = super().form_valid(form)

            HospitalAdminProfile.objects.create(
                user_id=self.object, hospital_id=hospital)

            return form
        except HospitalProfile.DoesNotExist:

            messages.error(
                self.request, "Contact Central e-Birth, hospital profile has not been updated!!")
            return redirect('auth:dashboard')


class ManageAdministratorsView(LoginRequiredMixin, ListView):
    template_name = "auth/manage_admin.html"

    # def get_queryset(self):
    #     try:
    #         hospital = HospitalAdminProfile.objects.get(user_id=self.request.user).hospital_id
    #         queryset = HospitalAdminProfile.objects.filter(hospital_id=hospital).exclude(user_id=self.request.user)
    #         return queryset
    #     except HospitalAdminProfile.DoesNotExist:
    #         messages.error(self.request, "Contact Central e-Birth, hospital profile has not been fully updated!!, therefore admin list can't be displayed")
    #         return None

    # def get(self, request, *args, **kwargs):
    #     queryset = self.get_queryset()
    #     if queryset is None:
    #         return redirect(reverse('auth:dashboard'))
    #     return super().get(request, *args, **kwargs)

    def get_queryset(self):
        try:
            # hospital = HospitalAdminProfile.objects.get(user_id=self.request.user).hospital_id
            hospital = HospitalProfile.objects.get(user_id=self.request.user)
            queryset = HospitalAdminProfile.objects.filter(
                hospital_id=hospital).exclude(user_id=self.request.user)
            return queryset
        except HospitalProfile.DoesNotExist:
            messages.error(
                self.request, "Contact Central e-Birth, hospital profile has not been fully updated!!, therefore admin list can't be displayed")
            return None

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if queryset is None:
            return redirect(reverse('auth:dashboard'))
        return super().get(request, *args, **kwargs)


class DeleteAdministratorView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = User
    success_message = "Administrator has been deleted!"

    def get_success_url(self):
        return reverse("reg:manage_admin")


class EditAdminView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = User
    form_class = EditAdminForm
    success_message = "Admin account has been edited successfully!"

    template_name = "auth/edit_admin.html"

    def get_success_url(self):
        return reverse("reg:manage_admin")


class CertificateView(LoginRequiredMixin, SuccessMessageMixin, DetailView):
    model = BirthRegistration

    template_name = "auth/view_certificate.html"

    def get_object(self):
        try:
            return BirthRegistration.objects.get(birth_id=self.kwargs['pk'])
        except BirthRegistration.DoesNotExist:
            try:
                return BirthRegistration.objects.get(user_id=self.kwargs['pk'])
            except BirthRegistration.DoesNotExist:
                raise Http404()

    def get(self, request, *args, **kwargs):
        try:
            self.object = self.get_object()
            if not self.object.place_of_birth.signature:
                messages.error(self.request, "Hospital signature not updated!")
                return redirect('auth:dashboard')
        except Http404:
            messages.error(self.request, "Failed in getting certificate!")
            return redirect('auth:dashboard')

        return self.render_to_response(self.get_context_data())

class DeathCertificateView(LoginRequiredMixin, SuccessMessageMixin, DetailView):
    model = DeathRegistration

    template_name = "auth/view_death_certificate.html"

    def get_object(self):
        try:
            return DeathRegistration.objects.get(death_id=self.kwargs['pk'])
        except DeathRegistration.DoesNotExist:
            raise Http404()

    def get(self, request, *args, **kwargs):
        try:
            self.object = self.get_object()
            if not self.object.hospital_issued.signature:
                messages.error(self.request, "Hospital signature not updated!")
                return redirect('auth:dashboard')
        except Http404:
            messages.error(self.request, "Failed in getting certificate!")
            return redirect('auth:dashboard')

        return self.render_to_response(self.get_context_data())


class EditHospitalProfileView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = HospitalProfile
    form_class = HospitalProfileForm
    success_message = "Hospital profile has been updated successfully!"
    hospital_id = None

    template_name = "auth/hospital_profile.html"

    def get(self, request, *args, **kwargs):
        try:
            self.object = self.get_object()
        except HospitalProfile.DoesNotExist:
            messages.error(
                self.request, "Contact Central Mgt, hospital profile has not been updated!!")
            return redirect('auth:dashboard')

        return self.render_to_response(self.get_context_data())

    def get_object(self):
        return HospitalProfile.objects.get(hospital_id=HospitalProfile.objects.get(user_id=self.kwargs['pk']).hospital_id)


class AccountProfileView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = User
    form_class = EditAdminForm
    success_message = "Account has been updated successfully!"

    template_name = "auth/account_profile.html"


class SearchCertificateView(LoginRequiredMixin, View):
    template_name1 = "auth/view_certificate.html"
    template_name2 = "auth/view_death_certificate.html"

    def get(self, request):
        qs = request.GET.get('qs')
        try:
            place_of_birth = HospitalProfile.objects.get(
                user_id=request.user.user_id)
        except HospitalProfile.DoesNotExist:
            hospital_admin_profile = HospitalAdminProfile.objects.filter(
                user_id=request.user)
            if hospital_admin_profile:
                hospital_profile = HospitalProfile.objects.get(
                    hospital_id=hospital_admin_profile[0].hospital_id.hospital_id).user_id
                place_of_birth = HospitalProfile.objects.get(
                    user_id=hospital_profile.user_id)

        context = {
            'query': request.GET.get('qs')
        }

        result1 = BirthRegistration.objects.filter(certificate_num=qs, place_of_birth=place_of_birth)
        result2 = DeathRegistration.objects.filter(certificate_num=qs, hospital_issued=place_of_birth)

        if result1:
            return redirect('reg:certificate', result1.first().birth_id)

        if result2:
            return redirect('reg:death_certificate', result2.first().death_id)

        messages.error(request, "incorrect certificate number, try again!!")
        return redirect("auth:dashboard")

    def get_context_data(self, **kwargs):
        context = super(SearchCertificateView, self).get_context_data(**kwargs)
        context['query'] = self.request.GET.get('qs')
        return context


class ChangePasswordView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = User
    form_class = ChangePassForm
    success_message = "password has been updated successfully!"
    template_name = "auth/change_password.html"

    def form_valid(self, form):
        old_pass = form.cleaned_data.get('old_pass')
        user_pass = self.request.user.password

        if check_password(old_pass, user_pass):
            form.instance.set_password(form.cleaned_data.get('new_pass'))
            return super().form_valid(form)

        messages.error(self.request, "Incorrect current password!")
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse("auth:login")
