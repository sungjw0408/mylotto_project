# lotto/views.py

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required # 1. 로그인 확인
from .models import LottoRound, LottoTicket, Winnings
from django.contrib import messages #수동 번호 기능추가

import random # 2. 자동 번호 생성을 위해 import

@login_required # 3. 로그인한 사용자만 이 뷰에 접근 가능
def lotto_index(request):

    # 4. 현재 진행 중인(추첨 안 된) 첫 번째 로또 회차를 가져옵니다.
    # (관리자 페이지에서 1회차를 미리 만들어둬야 합니다.)
    current_round = LottoRound.objects.filter(is_drawn=False).order_by('round_number').first()

    if request.method == 'POST':
        # --- ▼▼▼ '수동 구매' 로직 추가 ▼▼▼ ---
        if 'manual_buy' in request.POST and current_round:
            # 2. 'num'이라는 name으로 전송된 6개 번호를 리스트로 받음
            numbers = request.POST.getlist('num')

            # 3. 유효성 검사 (숫자 변환, 중복 제거)
            try:
                # 'input' 필드는 문자열이므로 정수(int)로 변환
                manual_numbers = [int(n) for n in numbers]

                # 4. 중복된 번호가 있는지 확인 (set 사용)
                if len(set(manual_numbers)) != 6:
                    messages.error(request, '수동 번호에 중복이 있거나 6개가 아닙니다.')
                # 5. 1~45 범위를 벗어나는지 확인
                elif not all(1 <= n <= 45 for n in manual_numbers):
                    messages.error(request, '번호는 1에서 45 사이여야 합니다.')
                else:
                    # 6. 유효성 검사 통과: 티켓 생성
                    LottoTicket.objects.create(
                        owner=request.user,
                        round=current_round,
                        numbers=sorted(manual_numbers),
                        is_auto=False # 수동
                    )
                    messages.success(request, '수동 구매가 완료되었습니다.')

            except ValueError:
                messages.error(request, '유효한 숫자를 입력하세요.')

            return redirect('lotto:lotto_index') # 처리 후 새로고침
        # 5. '자동 구매' 버튼이 눌렸을 때 (POST)
        if 'auto_buy' in request.POST and current_round:
            # 1~45 사이의 6개 랜덤 숫자 생성
            numbers = sorted(random.sample(range(1, 46), 6))

            # 티켓 생성
            LottoTicket.objects.create(
                owner=request.user,  # 6. 구매자는 현재 로그인한 사용자
                round=current_round,
                numbers=numbers,
                is_auto=True
            )
            # 7. 구매 후 새로고침 (네임스페이스 사용)
            return redirect('lotto:lotto_index') 

    # 1. 현재 진행 중인 회차의 내 티켓 목록
    my_tickets_current = []
    if current_round:
        my_tickets_current = LottoTicket.objects.filter(owner=request.user, round=current_round)

    # 2. 가장 최근에 추첨이 완료된 회차의 내 티켓 목록 및 당첨 여부
    latest_drawn_round = LottoRound.objects.filter(is_drawn=True).order_by('-draw_date').first()
    my_tickets_latest_drawn = []

    if latest_drawn_round:
        # 3. 최근 추첨 회차의 내 티켓들을 가져옵니다.
        my_tickets_latest_drawn = LottoTicket.objects.filter(owner=request.user, round=latest_drawn_round)

        # 4. 당첨 번호를 가져옵니다.
        win_numbers = set(latest_drawn_round.winning_numbers)

        # 5. 각 티켓에 당첨 결과를 '주입'합니다.
        for ticket in my_tickets_latest_drawn:
            user_numbers = set(ticket.numbers)
            match_count = len(user_numbers.intersection(win_numbers))

            # 6. 등수 계산 (간단한 버전)
            if match_count == 6:
                ticket.rank = 1
            elif match_count == 5: # (보너스 번호 로직은 생략)
                ticket.rank = 3 
            elif match_count == 4:
                ticket.rank = 4
            elif match_count == 3:
                ticket.rank = 5
            else:
                ticket.rank = 0 # 낙첨

    context = {
        'current_round': current_round,
        'my_tickets_current': my_tickets_current,
        'latest_drawn_round': latest_drawn_round,
        'my_tickets_latest_drawn': my_tickets_latest_drawn,
    }
    return render(request, 'lotto/index.html', context)

@login_required
def winnings_history(request):
    my_winnings = Winnings.objects.filter(ticket__owner=request.user).order_by('-ticket__round__round_number')
    
    context = {
        'my_winnings': my_winnings,
    }
    return render(request, 'lotto/winnings_history.html', context)

