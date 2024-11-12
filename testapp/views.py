import os.path
from datetime import datetime
from django.core.mail import EmailMessage, get_connection, send_mail, send_mass_mail, mail_admins
from django.http import FileResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from samplesite.settings import BASE_DIR
from testapp.forms import ImgForm

FILES_ROOT = BASE_DIR / 'files'


def index(request):

    if 'counter' in request.sessions:
        print('SESSIONS: counter =', request.sessions['counter'])
        cnt = int(request.sessions['counter']) + 1
    else:
        cnt = 1

    imgs = []

    for entry in os.scandir(FILES_ROOT):
        imgs.append(os.path.basename(entry))

    context = {'imgs': imgs}
    response = render(request, 'testapp/index.html', context)
    response.set_cookie('counter', cnt)
    request.session['counter'] = cnt
    return response


def get(request, filename):
    fn = os.path.join(FILES_ROOT, filename)

    return FileResponse(open(fn, 'rb'), context_type='application/octet-stream')


def add(request):
    if request.method == 'POST':
        form = ImgForm(request.POST, request.FILES)
        if form.is_valid():
            upload_file = request.FILES['img']
            fn = '%s%s' % (datetime.now().timestamp(),
                           os.path.splitext(upload_file.name)[1])
            fn = os.path.join(FILES_ROOT, fn)
            with open(fn, 'wb+') as destination:
                for chunk in upload_file.chunks():
                    destination.write(chunk)
            return redirect('bboard:index')
    else:
        form = ImgForm()

    context = {'form': form}
    return render(request, 'testapp/add.html', context)


def test_cookie(request):
    if request.method == 'POST':
        if request.session.test_cookie_worked():
            request.session.delete_test_cookie()

        else:
            pass

    request.session.set_test_cookie()
    return render(request, 'testapp/test_cookie.html')


def test_email(request):
    # em = EmailMessage(subject='Ваш новый пароль', body='Ваш новый пароль находится во вложении',
    #                   attachments=[('requirements.txt', '123456789', 'text/plain')],
    #                   to=['user@supersite.ru'])
    # em.send()
    #
    # em = EmailMessage(subject='Ваш новый пароль',
    #                   body='Ваш новый пароль находится во вложении',
    #                   to=['user@supersite.ru'])
    # em.attach_file(r'requirements.txt')
    # em.send()
    # context = {'user': 'Вася Пупкин'}
    # s = render_to_string('email/letter.txt', context)
    # em = EmailMessage(subject='Оповещение', body=s, to=['user@supersite.ru'])
    # em.send()
    # con = get_connection()
    # con.open()

    # email1 = EmailMessage(..., connection=con)
    # email1.send()
    # email2 = EmailMessage(..., connection=con)
    # email2.send()
    # email3 = EmailMessage(..., connection=con)
    # email3.send()

    # email1 = EmailMessage(...)
    # email2 = EmailMessage(...)
    # email3 = EmailMessage(...)
    #
    # con.send([email1, email2, email3])
    # con.close()

    # send_mail('Test email', 'TEst!!!', 'webmaster@localhost', ['user@othersite.kx'],
    #           html_message='<h1>Test!!!</h1>')

    # msg1 = ('Подписка', 'Подтвердите, пожалуйста, одписку', 'subcribe@supersite.kz',
    #         ['user@othersite.kz', 'user2@thirdsite.kz'])
    # msg2 = ('Подписка', 'Ваша подписка подтверждена', 'subcribe@supersite.kz',
    #         ['megauser@supersite.kz'])
    #
    # send_mass_mail((msg1, msg2))
    #
    pass

    mail_admins('Подъём!', 'Админ, не спи!', html_message='<strong>Админ, не спи!!</strong>')
    pass


from django.contrib.auth import authenticate, login, logout


def my_view(request):
    username = request.POST['username']
    password = request.POST['password']

    user = authenticate(username=username, password=password)
    if user is not None:
        login
    else:
        pass

    if request.user.is_authenticated:
        pass
    else:
        pass


def logout_view(request):
    logout(request)
