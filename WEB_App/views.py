from datetime import datetime
import random
import string

import requests
from django.conf import settings
from django.contrib.auth import login

from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.views.generic.base import View

from Scanner.settings import API_TOKEN
from WEB_App.forms import UserRegistrationForm, RecoveryPass, ChangeInfoForm, FileForm, CommentForm
from WEB_App.models import Recovery, UserPhoto, GoodsOnModeration, Picture, Comment

from django.views import View
from django.views.generic import TemplateView
from django.contrib.auth.mixins import PermissionRequiredMixin

from django.http import HttpResponse



def signup(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password2'])
            new_user.save()
            login(request, new_user)
            return render(request, 'main/index.html', {'username': user_form.data['username']})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'registration/registration.html', {'user_form': user_form})


def recovery_password(request):
    context = {'step': '1'}
    user_ip = request.META.get('REMOTE_ADDR', '') or request.META.get('HTTP_X_FORWARDED_FOR', '')
    form = RecoveryPass(request.POST)
    if request.method == 'POST':
        if request.POST.get('start_procedure'):
            data = request.POST.get('start_procedure')
            target_user = None
            if User.objects.filter(username=data):
                target_user = User.objects.get(username=data)
            elif User.objects.filter(email=data):
                target_user = User.objects.get(email=data)
            if target_user:
                code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
                send_recovery_code(code, target_user)
                rec = Recovery(target_user=target_user, from_ip=user_ip, code=code)
                rec.save()
                context['step'] = '2'
            else:
                context['error'] = 'Пользователь не найден'
        if request.POST.get('code'):
            code = request.POST.get('code')
            target_user = None
            if Recovery.objects.filter(code=code):
                data = Recovery.objects.filter(code=code)
                for item in data:
                    if user_ip == item.from_ip:
                        target_user = item.target_user
                        context['step'] = '3'
                        context['form'] = form
                        request.session['id_user'] = target_user.id
            if target_user is None:
                context['step'] = '2'
                context['error'] = 'Неверный код'
        if request.POST.get('password'):
            if form.is_valid():
                target_user = request.session.get('id_user')
                new_pass = form.data['password']
                target_user = User.objects.get(id=target_user)
                target_user.set_password(new_pass)
                target_user.save()
                login(request, target_user)
                data_for_delete = Recovery.objects.filter(target_user=target_user)
                for item in data_for_delete:
                    item.delete()
                context['step'] = '4'
            else:
                context['step'] = '3'
                context['form'] = form
                context['error'] = 'Ошибка при заполнении полей'
    return render(request, 'registration/recovery_password.html', context)


def send_recovery_code(code, user):
    email_subject = 'EVILEG :: Сообщение через контактную форму '
    email_body = "Код для восстановления пароля: {}".format(code)
    send_mail(email_subject, email_body, settings.EMAIL_HOST_USER, ['{}'.format(user.email)],
              fail_silently=False)


def profile(request):
    context = {}
    context['user'] = User.objects.get(id=request.user.id)
    current_user = User.objects.get(id=request.user.id)
    if UserPhoto.objects.filter(user=current_user):
        context['photo'] = UserPhoto.objects.get(user=current_user).img
    else:
        context['photo'] = 'profile/profile_icon.png'
    return render(request, 'profile/profile.html', context)


def change_info(request):
    current_user = User.objects.get(id=request.user.id)
    form = ChangeInfoForm(request.POST)
    form.fields['username'].widget.attrs['placeholder'] = current_user.username
    form.fields['email'].widget.attrs['placeholder'] = current_user.email
    photo = FileForm(request.POST, request.FILES)
    context = {'form': form, 'photo': photo}
    if UserPhoto.objects.filter(user=current_user):
        context['userphoto'] = UserPhoto.objects.get(user=current_user).img
    else:
        context['userphoto'] = 'profile/profile_icon.png'
    if request.method == 'POST':
        if request.POST.get('old_password'):
            old_password = request.POST.get('old_password')
            if current_user.check_password('{}'.format(old_password)) is False:
                form.set_old_password_flag()
                return render(request, 'profile/change_info.html', {'form': form})
        if form.is_valid():
            if request.POST.get('username'):
                current_user.username = request.POST.get('username')
            if request.POST.get('email'):
                current_user.email = request.POST.get('email')
            if request.POST.get('old_password'):
                old_password = request.POST.get('old_password')
                if current_user.check_password('{}'.format(old_password)) is False:
                    form.set_old_password_flag()
                    return render(request, 'profile/change_info.html', {'form': form})
                else:
                    current_user.set_password('{}'.format(form.data['new_password2']))
            current_user.save()
            login(request, current_user)
        else:
            return render(request, 'profile/change_info.html', context)
        if photo.is_valid():
            if UserPhoto.objects.filter(user=current_user):
                userphoto = UserPhoto.objects.get(user=current_user)
            else:
                userphoto = UserPhoto(user=current_user, img='profile/profile_icon.png')
            if request.FILES.get('file'):
                userphoto.img = request.FILES.get('file')
                userphoto.save()
    if request.POST.get('status'):
        return redirect('/profile')
    return render(request, 'profile/change_info.html', context)


def index(request):
    context = {'data': datetime.now()}
    reg_form = UserRegistrationForm()
    errors = []
    if request.method == 'POST':
        if request.POST.get('status') == 'SignUp':
            reg_form = UserRegistrationForm(request.POST)
            if reg_form.is_valid():
                new_user = reg_form.save(commit=False)
                new_user.set_password(reg_form.cleaned_data['password2'])
                new_user.save()
                login(request, new_user)
        if request.POST.get('status') == 'SignIn':
            identification = request.POST.get('identification')
            password = request.POST.get('password')

            user = None
            if User.objects.filter(username=identification):
                user = User.objects.get(username=identification)
            elif User.objects.filter(email=identification):
                user = User.objects.get(email=identification)
            if user is None:
                errors.append('Пользователь не найден!')
            elif user.check_password(password) is False:
                errors.append('Неправильный пароль!')
            else:
                login(request, user)
        if request.FILES:
            if not request.user.is_authenticated:
                context['show_modal'] = 'true'
            else:
                picture = Picture(
                    user=request.user,
                    file=request.FILES['file'],
                )
                picture.save()

                response = requests.get('http://api.scanner.savink.in/api/v1/goods/get_product/',
                                        files={'file': picture.file},
                                        params={'user': request.user.id,
                                                'platform': 'web'},
                                        headers={'Authorization': '{}'.format(API_TOKEN)}
                                        ).json()

                if response['status'] == 'ok':
                    return redirect(to='/product/{}/?image={}'.format(response['good'], picture.id))
                else:
                    return redirect(to='/add_product/?image={}'.format(picture.id))

    context['reg_form'] = reg_form
    context['login_errors'] = errors

    return render(request, 'main/index.html', context)


class PhotoPage(TemplateView):
    context = {}

    def post(self, request):
        picture = Picture(
            user=request.user,
            file=request.FILES['file'],
        )
        picture.save()

        response = requests.get('http://api.scanner.savink.in/api/v1/goods/get_product/',
                                files={'file': picture.file},
                                params={'user': request.user.id,
                                        'platform': 'web'},
                                headers={'Authorization': '{}'.format(API_TOKEN)}
                                ).json()

        if response['status'] == 'ok':
            return redirect(to='/product/{}/?image={}'.format(response['good'], picture.id))
        else:
            return redirect(to='/add_product/?image={}'.format(picture.id))


class ProductPage(TemplateView):
    context = {}

    def get(self, request, good):
        try:
            self.context['name'] = good
            image_id = request.GET.get('image')
            if image_id:
                image = Picture.objects.get(id=image_id)
                image.target_good = good
                image.save()
                self.context['img'] = image.file.url
            else:
                image = Picture.objects.filter(target_good=good)
                self.context['img'] = image[0].file.url

            response = requests.get('http://api.scanner.savink.in/api/v1/goods/get_by_name/{}/'.format(good),
                                    headers={'Authorization': '{}'.format(API_TOKEN)}
                                    ).json()

            self.context['comment_form'] = CommentForm()
            self.context['positives'] = response['positives']
            self.context['negatives'] = response['negatives']
            self.context['points'] = response['points']
            self.context['categories'] = response['categories']
            self.context['comments'] = Comment.objects.filter(good=good)
            return render(request, self.template_name, self.context)
        except Exception:
            return render(request, '404.html', self.context)

    def post(self, request, good):
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = Comment(
                text=comment_form.cleaned_data.get('text'),
                user=User.objects.get(id=request.user.id),
                good=good
            )
            new_comment.save()
            return render(request, self.template_name, self.context)
        elif request.POST.get('response-to-comment'):
            new_children_comment = ChildrenComment(
                text=request.POST.get('response-to-comment'),
                user=User.objects.get(id=request.user.id),
                parent=Comment.objects.get(id=request.POST.get('comment_id'))
            )
            new_children_comment.save()
            return render(request, self.template_name, self.context)
        else:
            return render(request, '500.html', self.context)


class AddProductPage(View):
    template_name = 'photo/add_product.html'
    context = {}

    def get(self, request):
        self.context['img'] = Picture.objects.get(id=request.GET.get('image')).file.url
        return render(request, self.template_name, self.context)

    def post(self, request):
        good = GoodsOnModeration(
            name=request.POST.get('name'),
            image=Picture.objects.get(id=request.GET.get('image')).file,
            user=request.user
        )
        response = requests.get('http://api.scanner.savink.in/api/v1/getbarcode/',
                                files={'file': good.image.file},
                                headers={'Authorization': '{}'.format(API_TOKEN)}
                                ).json()

        if response['status'] == 'ok':
            good.barcode = response['barcode']

        good.save()

        return redirect('/thanks/')


class AcceptPage(PermissionRequiredMixin, View):
    template_name = 'admin/accept.html'
    permission_required = 'WEB_App.view'
    login_url = '/login/'

    def get(self, request):
        return render(request, self.template_name, self.get_context())

    def post(self, request):
        if request.POST.get('action') == 'accept':
            moderation_good = GoodsOnModeration.objects.get(id=request.POST.get('id'))
            name = request.POST.get('name')
            barcode = request.POST.get('barcode') if request.POST.get('barcode') != 'None' else None
            points = request.POST.get('points') or '?'
            category = request.POST.get('category')
            image = None

            if request.FILES:
                image = request.FILES.get('image')

            requests.post('http://api.scanner.savink.in/api/v1/goods/create/',
                          files={'file': image},
                          data={'user': request.user.id,
                                'name': name,
                                'category': category,
                                'barcode': barcode,
                                'points_rusControl': points
                                },
                          headers={'Authorization': '{}'.format(API_TOKEN)}
                          )
            moderation_good.status = 2
            moderation_good.save()

        elif request.POST.get('action') == 'deny':
            moderation_good = GoodsOnModeration.objects.get(id=request.POST.get('id'))
            moderation_good.status = 3
            moderation_good.save()

        elif request.POST.get('action') == 'create_category':
            name = request.POST.get('name')
            parent_id = request.POST.get('category') or None
            image = request.FILES.get('image') or None
            requests.post('http://api.scanner.savink.in/api/v1/category/create/',
                          files={'file': image},
                          data={'user': request.user.id,
                                'name': name,
                                'parent': parent_id,
                                },
                          headers={'Authorization': '{}'.format(API_TOKEN)}
                          )

        return render(request, self.template_name, self.get_context())

    def get_context(self):
        context = {}

        data_goods_on_moderation = GoodsOnModeration.objects.filter(status=1)
        context['goods_data'] = data_goods_on_moderation

        categories = requests.get('http://api.scanner.savink.in/api/v1/category/all/',
                                  headers={'Authorization': '{}'.format(API_TOKEN)}
                                  ).json()
        context['categories'] = categories
        return context


class CategoryView(TemplateView):
    def get(self, request, *args, **kwargs):
        try:
            context = self.get_context_data(**kwargs)
            context['children'] = requests.get('http://api.scanner.savink.in/api/v1/category/filter/'
                                               '{}'.format(context['category']),
                                               headers={'Authorization': '{}'.format(API_TOKEN)}).json()
            context['goods'] = requests.get('http://api.scanner.savink.in/api/v1/goods/get_by_category/'
                                            '{}'.format(context['category']),
                                            headers={'Authorization': '{}'.format(API_TOKEN)}).json()
            return render(request, self.template_name, context)

        except ValueError:
            return render(request, self.template_name, context)


