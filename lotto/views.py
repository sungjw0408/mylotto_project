from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required # 로그인 확인
from .models import LottoRound, LottoTicket, Winnings
from django.contrib import messages

import random

@login_required # 로그인한 사용자 접근
def lotto_index(request):

    #  현재 진행 중인 첫 번째 로또 회차 (mdoel.py로 부터가져옴)
    current_round = LottoRound.objects.filter(is_drawn=False).order_by('round_number').first()

    if request.method == 'POST':
        # 수동구매
        if 'manual_buy' in request.POST and current_round:
            # 6개 번호, 리스트로 받음
            numbers = request.POST.getlist('num')

            # 숫자 변환, 중복 제거
            try:
                # (문자열 -> int) 변환
                manual_numbers = [int(n) for n in numbers]

                # 수동 번호 중복 확인
                if len(set(manual_numbers)) != 6:
                    messages.error(request, '수동 번호에 중복이 있거나 6개가 아닙니다.')
                # 범위(1~45) 확인
                elif not all(1 <= n <= 45 for n in manual_numbers):
                    messages.error(request, '번호는 1에서 45 사이여야 합니다.')
                else:
                    # 티켓 생성
                    LottoTicket.objects.create(
                        owner=request.user,
                        round=current_round,
                        numbers=sorted(manual_numbers),
                        is_auto=False
                    )
                    messages.success(request, '수동 구매가 완료되었습니다.')

            except ValueError:
                messages.error(request, '유효한 숫자를 입력하세요.')

            return redirect('lotto:lotto_index') # 처리 후 새로고침
        # 자동 구매
        if 'auto_buy' in request.POST and current_round:
            # 6개 랜덤 숫자 생성(1~45)
            numbers = sorted(random.sample(range(1, 46), 6))

            # 티켓 생성
            LottoTicket.objects.create(
                owner=request.user, 
                round=current_round,
                numbers=numbers,
                is_auto=True
            )
            # 구매 후 새로고침
            return redirect('lotto:lotto_index') 

    # 진행 중인 회차의 나의 로또 티켓 목록
    my_tickets_current = []
    if current_round:
        my_tickets_current = LottoTicket.objects.filter(owner=request.user, round=current_round)

    # 최근 회차 나의 로또 티켓 목록 및 당첨 여부
    latest_drawn_round = LottoRound.objects.filter(is_drawn=True).order_by('-draw_date').first()
    my_tickets_latest_drawn = []

    if latest_drawn_round:
        # 최근 회차의 나의 로또 티켓
        my_tickets_latest_drawn = LottoTicket.objects.filter(owner=request.user, round=latest_drawn_round)

        # 당첨 번호 
        win_numbers = set(latest_drawn_round.winning_numbers)

        # 각 티켓 당첨 여부
        for ticket in my_tickets_latest_drawn:
            user_numbers = set(ticket.numbers)
            match_count = len(user_numbers.intersection(win_numbers))

            # 등수 계산 
            if match_count == 6:
                ticket.rank = 1
            elif match_count == 5:
                ticket.rank = 3 
            elif match_count == 4:
                ticket.rank = 4
            elif match_count == 3:
                ticket.rank = 5
            else:
                ticket.rank = 0 

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

