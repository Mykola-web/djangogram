import logging

from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.db import IntegrityError
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.decorators import method_decorator
from django.utils.http import urlsafe_base64_decode
from django.views import View
from django.views.decorators.http import require_POST
from django.views.generic import TemplateView

from .forms import RegistrationForm, EditProfileForm, LoginForm, PostForm, PostImageFormSet
from .models import PostModel, ProfileModel
from .services import send_activation_email, generate_activation_link

logger = logging.getLogger(__name__)

class HomeView(TemplateView):
    template_name = 'myapp/home.html'


class RegisterView(View):
    def get(self, request):
        if request.user.is_authenticated:
            logout(request)
        form = RegistrationForm()
        return render(request, 'myapp/registration.html', {'form': form})

    def post(self, request):
        if request.user.is_authenticated:
            logout(request)
        form = RegistrationForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            try:
                user = User.objects.create(username = username, email = email, is_active = False)
                user.set_password(password)
                user.save()

                activation_link = generate_activation_link(user)
                send_activation_email(user, activation_link)
                return render(request, 'myapp/sent_email.html')
            except IntegrityError:
                form.add_error('username', 'A user with this username is already registered')
                return render(request, 'myapp/registration.html', {'form':form})
        return render(request, 'myapp/registration.html', {'form': form})


class ActivateAccount(View):
    def get(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk = uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return render(request, 'myapp/activation.html',
                          {'message': 'The activation link is invalid or expired.'})

        if user is not None and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return render(request, 'myapp/activation.html',
                          {'message': '🎉Activation completed🎉'})
        else:
            return render(request, 'myapp/activation.html',
                          {'message': 'The activation link is invalid.'})


class EditProfileView(LoginRequiredMixin, View):
    def get(self, request):
        form = EditProfileForm(instance = request.user.profile)
        return render(request, 'myapp/edit_profile.html', {'form': form})

    def post(self, request):
        form = EditProfileForm(request.POST,request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
        else:
            return render(request, 'myapp/edit_profile.html', {'form': form})


class LoginView(View):
    def get(self, request):
        if request.user.is_authenticated:
            logout(request)
            return redirect(request.GET.get('next', request.META.get('HTTP_REFERER', 'login')))
        form = LoginForm()
        return render(request, 'myapp/login.html', {'form': form})

    def post(self, request):
        if request.user.is_authenticated:
            logout(request)

        form = LoginForm(request.POST)
        if not form.is_valid():
            print('Form errors:', form.errors)
            return render(request, 'myapp/login.html', {'form': form})

        user = authenticate(
            username = form.cleaned_data['username'],
            password = form.cleaned_data['password']
        )
        if user is None:
            print('Authentication failed:', user)
            form.add_error(None, 'Invalid login credentials')
            return render(request, 'myapp/login.html', {'form': form})

        login(request, user)

        next_url = request.POST.get('next')

        return redirect(next_url if next_url else 'feed')


class FeedView(LoginRequiredMixin, View):
    def get(self, request):
        posts = PostModel.objects.all().order_by("-created_at")
        return render(request, 'myapp/feed.html', {'posts': posts})

class SubFeedView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        subscribed_profiles = user.subscribed.all()  # Это ProfileModel
        subscribed_users = [profile.user for profile in subscribed_profiles]
        if len(subscribed_users) <= 0:
            subscribtions = False
        else:
            subscribtions = True
        posts = PostModel.objects.filter(author__in=subscribed_users).order_by('-created_at')
        return render(request, 'myapp/sub_feed.html',
                      {'posts': posts, 'subscribtions': subscribtions})


class PostingView(LoginRequiredMixin, View):
    def get(self, request):
        form = PostForm()
        formset = PostImageFormSet()
        return render(request, 'myapp/new_post.html', {'form': form, 'formset': formset})

    def post(self, request):
            post_form = PostForm(request.POST)
            formset = PostImageFormSet(request.POST, request.FILES)

            if post_form.is_valid() and formset.is_valid():
                post = post_form.save(commit = False)
                post.author = request.user
                post.save()
                post_form.save_m2m()

                images = formset.save(commit = False)
                for image in images:
                    image.post = post
                    image.save()

                return redirect('profile')
            else:
                return render(request, 'myapp/new_post.html',
                              {'form': post_form, 'formset' : formset})


class ProfileView(LoginRequiredMixin, View):
    def get(self, request, username = None):
        # Here it is decided whose page will be opened, the current user or another
        if username:
            profile_owner = get_object_or_404(User, username = username)
        elif request.user.is_authenticated:
            profile_owner = request.user
        else:
            return HttpResponse("The user is not authorized", status = 401)

        is_own_profile = request.user.is_authenticated and request.user == profile_owner

        profile = get_object_or_404(ProfileModel, user = profile_owner)
        is_subscribed = request.user in profile.subscribers.all()
        posts = PostModel.objects.filter(author = profile_owner).order_by("-created_at")
        return render(request, 'myapp/profile.html', {'profile_owner': profile_owner,
                                                               'posts': posts,
                                                               'is_own_profile': is_own_profile,
                                                               'is_subscribed': is_subscribed,})

    def post(self, request, username = None):
        if username:
            profile_owner = get_object_or_404(User, username = username)
        elif request.user.is_authenticated:
            profile_owner = request.user
        else:
            return HttpResponse("The user is not authorized", status = 401)

        profile = profile_owner.profile

        if request.user == profile_owner:
            # cannot subscribe to yourself, do nothing
            pass
        else:
            if profile.subscribers.filter(id=request.user.id).exists():
                profile.subscribers.remove(request.user)
            else:
                profile.subscribers.add(request.user)

        return redirect('profile', username = username or request.user.username)



class LikePostView(LoginRequiredMixin, View):
    @method_decorator(require_POST)
    def post(self, request, post_id):
        post = get_object_or_404(PostModel, id = post_id)
        if request.user in post.likes.all():
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)
        return JsonResponse({'likes_count': post.likes.count()})

class RestorePasswordView(View):
    def get(self, request):
        if request.user.is_authenticated:
            logout(request)

        return render(request, 'myapp/restore_profile.html')
    # def post(self, request):
