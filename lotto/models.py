from django.db import models
# Django 기본 사용자 모델(User)
from django.contrib.auth.models import User 
# 로또 회차 정보
class LottoRound(models.Model):
    # 로또 회차(조건:양수, 중복 X)
    round_number = models.PositiveIntegerField(unique=True, verbose_name="회차")
    draw_date = models.DateTimeField(verbose_name="추첨일")
    # 당첨 번호
    winning_numbers = models.JSONField(null=True, blank=True, verbose_name="당첨 번호")
    is_drawn = models.BooleanField(default=False, verbose_name="추첨 완료 여부")

    class Meta:
        verbose_name = 'Lotto Round'      
        verbose_name_plural = '로또 회차'

    def __str__(self):
        return f"{self.round_number}회차"
#로또 티켓 정보
class LottoTicket(models.Model):
    # 구매자(user)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="구매자")
    # 로또 회차
    round = models.ForeignKey(LottoRound, on_delete=models.CASCADE, verbose_name="회차")
    numbers = models.JSONField(verbose_name="선택 번호") 
    is_auto = models.BooleanField(default=False, verbose_name="자동 구매 여부")
    purchase_date = models.DateTimeField(auto_now_add=True) # 구매 시각 자동 저장
    class Meta:
        verbose_name = 'Lotto Ticket'
        verbose_name_plural = '로또 티켓'

    def __str__(self):
        return f"{self.owner.username}님의 {self.round.round_number}회차 티켓"
#당첨 내역
class Winnings(models.Model):
    #당첨된 번호
    ticket = models.OneToOneField(LottoTicket, on_delete=models.CASCADE, verbose_name="당첨 티켓")
    rank = models.PositiveIntegerField(verbose_name="등수")
    prize_amount = models.DecimalField(max_digits=12, decimal_places=0, verbose_name="당첨금")
    class Meta:
        verbose_name = 'Winning'
        verbose_name_plural = '당첨자'

    def __str__(self):
        return f"{self.ticket} - {self.rank}등 당첨"