from django.db import models
from django.views import View


class Vip(models.Model):
    '''VIP��'''
    name = models.CharField(max_length=32, unique=True, verbose_name='��Ա�ȼ���Ӧ������')
    level = models.IntegerField(verbose_name='VIP �ȼ�')
    price = models.FloatField(verbose_name='��Ա�ȼ���Ӧ�ļ۸�')

    class Meta:
        ordering = ['level']

    @property
    def perms(self):
        '''ȡ����ǰ VIP ӵ�е�����Ȩ��'''
        # ����Ȩ�޹�ϵ��ȡ�����Լ�vip_idһ�µ�����
        relations = VipPermRelation.objects.filter(vip_id=self.id)

        # ȡ��Ȩ��id
        perm_id_list = [rlt.perm_id for rlt in relations]

        # ȥȨ�ޱ�ȡ��Ȩ��
        return Permission.objects.filter(id__in=perm_id_list)

    def has_perm(self, perm_name):
        '''��鵱ǰ VIP �Ƿ�ӵ��ĳȨ��'''
        for perm in self.perms:
            if perm.name == perm_name:
                return True
        return False


class Permission(models.Model):
    '''Ȩ�ޱ�'''
    name = models.CharField(max_length=16, unique=True, verbose_name='Ȩ������')
    desc = models.TextField(verbose_name='��Ȩ�޵�����')


class VipPermRelation(models.Model):
    '''Vip �� Ȩ�� �Ĺ�ϵ��'''
    vip_id = models.IntegerField()
    perm_id = models.IntegerField()
