# lotto/admin.py

from django.contrib import admin
from .models import LottoRound, LottoTicket, Winnings
import random # 추첨을 위해 import

# 1. LottoTicket 모델을 관리자 페이지에 등록
@admin.register(LottoTicket)
class LottoTicketAdmin(admin.ModelAdmin):
    # 관리자 페이지 목록에 보여줄 필드
    list_display = ('owner', 'round', 'numbers', 'is_auto', 'purchase_date')
    # 필터 옵션 추가
    list_filter = ('round', 'is_auto')
    # 검색 기능 추가
    search_fields = ('owner__username',)


# 2. Winnings 모델을 관리자 페이지에 등록
@admin.register(Winnings)
class WinningsAdmin(admin.ModelAdmin):
    list_display = ('ticket', 'rank', 'prize_amount')
    search_fields = ('ticket__owner__username',)


# 3. LottoRound 모델 관리자 설정
@admin.register(LottoRound)
class LottoRoundAdmin(admin.ModelAdmin):
    list_display = ('round_number', 'draw_date', 'winning_numbers', 'is_drawn')
    list_filter = ('is_drawn',)
    
    # 4. 관리자 페이지에 'actions' 추가
    actions = ['draw_winning_numbers']

    @admin.action(description='선택한 회차 추첨하기')
    def draw_winning_numbers(self, request, queryset):
        # 5. 선택한 회차(queryset)들에 대해 반복
        for round in queryset:
            # 6. 이미 추첨했으면 건너뛰기
            if round.is_drawn:
                continue

            # 7. 당첨 번호 생성
            winning_numbers = sorted(random.sample(range(1, 46), 6))
            round.winning_numbers = winning_numbers
            round.is_drawn = True # 추첨 완료로 표시
            round.save()

            # 8. 이 회차의 모든 티켓을 가져와서 당첨 여부 확인
            tickets_in_round = LottoTicket.objects.filter(round=round)
            for ticket in tickets_in_round:
                # 9. 일치하는 번호 개수 확인
                user_numbers = set(ticket.numbers)
                win_numbers = set(winning_numbers)
                match_count = len(user_numbers.intersection(win_numbers))

                # 10. 당첨 내역 생성 (6개 일치 시 1등)
                if match_count == 6:
                    Winnings.objects.create(
                        ticket=ticket,
                        rank=1,
                        prize_amount=1000000000 # (예시: 10억)
                    )
                # (TODO: 5개 일치(2등) 등 다른 등수 로직 추가)