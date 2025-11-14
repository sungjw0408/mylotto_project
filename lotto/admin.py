from django.contrib import admin
from .models import LottoRound, LottoTicket, Winnings
import random 

# LottoTicket model -> admin 페이지에 등록
@admin.register(LottoTicket)
class LottoTicketAdmin(admin.ModelAdmin):
    # 관리자 페이지 목록에 보여줄 필드
    list_display = ('owner', 'round', 'numbers', 'is_auto', 'purchase_date')
    # 필터 옵션 추가
    list_filter = ('round', 'is_auto')
    # 검색 기능 추가
    search_fields = ('owner__username',)


# 2. Winnings model -> admin 페이지에 등록
@admin.register(Winnings)
class WinningsAdmin(admin.ModelAdmin):
    list_display = ('ticket', 'rank', 'prize_amount')
    search_fields = ('ticket__owner__username',)


# 3. LottoRound model 관리자 설정
@admin.register(LottoRound)
class LottoRoundAdmin(admin.ModelAdmin):
    list_display = ('round_number', 'draw_date', 'winning_numbers', 'is_drawn')
    list_filter = ('is_drawn',)
    
    # admin 페이지 actions 추가
    actions = ['draw_winning_numbers']

    @admin.action(description='선택한 회차 추첨하기')
    def draw_winning_numbers(self, request, queryset):
        # 선택한 회차 반복
        for round in queryset:
            
            if round.is_drawn:
                continue

            # 당첨 번호 생성
            winning_numbers = sorted(random.sample(range(1, 46), 6))
            round.winning_numbers = winning_numbers
            round.is_drawn = True # 추첨 완료 표시
            round.save()

            # 이 회차의 모든 구매티켓 당첨 여부 확인
            tickets_in_round = LottoTicket.objects.filter(round=round)
            for ticket in tickets_in_round:
                # 일치하는 번호 개수 확인
                user_numbers = set(ticket.numbers)
                win_numbers = set(winning_numbers)
                match_count = len(user_numbers.intersection(win_numbers))
                

                # 당첨 내역 생성
                rank = 0
                prize_amount = 0

                if match_count == 6:
                    Winnings.objects.create(
                        ticket=ticket,
                        rank=1,
                        prize_amount=1000000000 # 당첨금
                    )
                elif match_count == 5:
                    Winnings.objects.create(
                        ticket=ticket,
                        rank=2,
                        prize_amount=50000000 # 당첨금
                    )  
                elif match_count == 4:
                    Winnings.objects.create(
                        ticket=ticket,
                        rank=3,
                        prize_amount=5000000 # 당첨금
                    )
                elif match_count == 3:
                    Winnings.objects.create(
                        ticket=ticket,
                        rank=4,
                        prize_amount=100000 # 당첨금
                    )  
                #낙첨인 경우(3개 이하) Winnings 데이터 생성 X
                if rank > 0:
                    Winnings.objects.create(
                        ticket=ticket,
                        rank=rank,
                        prize_amount=prize_amount
                    )
            

