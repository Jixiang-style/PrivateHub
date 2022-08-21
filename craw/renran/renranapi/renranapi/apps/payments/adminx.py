import xadmin

from .models import Reward
class RewardModelAdmin(object):
    pass
xadmin.site.register(Reward,RewardModelAdmin)