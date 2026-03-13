from django.db import models


class AuthRole(models.Model):

    name = models.CharField(max_length=50, unique=True)

    class Meta:
        db_table = "m_auth_role"

    def __str__(self):
        return self.name


class AuthUser(models.Model):

    username = models.CharField(max_length=50, unique=True)

    password = models.CharField(max_length=255)

    role = models.ForeignKey(
        AuthRole,
        on_delete=models.PROTECT,
        db_column="role_id",
        null=True
    )

    class Meta:
        db_table = "m_auth_user"

    def __str__(self):
        return self.username