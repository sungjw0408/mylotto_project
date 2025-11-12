# users/views.py

from django.shortcuts import render, redirect
from .forms import SignUpForm  # 10단계에서 만든 폼

def signup(request):
    if request.method == 'POST':
        # 1. 폼(Form)이 전송되었을 때 (POST)
        form = SignUpForm(request.POST)

        if form.is_valid():
            form.save()  # 2. 폼이 유효하면 사용자를 저장
            # 3. 회원가입 성공 후 로그인 페이지로 이동
            return redirect('login') 
    else:
        # 4. 페이지에 처음 접속했을 때 (GET)
        form = SignUpForm()

    return render(request, 'users/signup.html', {'form': form})