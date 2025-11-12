from django.db import models
# Django의 기본 사용자 모델(User)을 가져옵니다.
from django.contrib.auth.models import User 

class LottoRound(models.Model):
    """로또 회차 정보 (관리자가 생성)"""
    round_number = models.PositiveIntegerField(unique=True, verbose_name="회차")
    draw_date = models.DateTimeField(verbose_name="추첨일")
    # 당첨 번호 (JSONField는 리스트 [1, 10, 20, ...] 를 저장하기 좋습니다)
    winning_numbers = models.JSONField(null=True, blank=True, verbose_name="당첨 번호")
    is_drawn = models.BooleanField(default=False, verbose_name="추첨 완료 여부")

    def __str__(self):
        return f"{self.round_number}회차"

class LottoTicket(models.Model):
    """사용자가 구매한 로또 티켓"""
    # 구매자 (User 모델과 1:N 관계)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="구매자")
    # 회차 (LottoRound 모델과 1:N 관계)
    round = models.ForeignKey(LottoRound, on_delete=models.CASCADE, verbose_name="회차")
    numbers = models.JSONField(verbose_name="선택 번호") # 예: [5, 12, 22, 28, 35, 41]
    is_auto = models.BooleanField(default=False, verbose_name="자동 구매 여부")
    purchase_date = models.DateTimeField(auto_now_add=True) # 구매 시각 자동 저장

    def __str__(self):
        return f"{self.owner.username}님의 {self.round.round_number}회차 티켓"

class Winnings(models.Model):
    """당첨 내역"""
    # 당첨된 티켓 (LottoTicket 모델과 1:1 관계)
    ticket = models.OneToOneField(LottoTicket, on_delete=models.CASCADE, verbose_name="당첨 티켓")
    rank = models.PositiveIntegerField(verbose_name="등수") # 1, 2, 3, 4, 5
    prize_amount = models.DecimalField(max_digits=12, decimal_places=0, verbose_name="당첨금")

    def __str__(self):
        return f"{self.ticket} - {self.rank}등 당첨"