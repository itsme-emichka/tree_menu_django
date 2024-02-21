from django.db import models


class Menu(models.Model):
    title = models.CharField('Название меню', max_length=256, unique=True,)

    def __str__(self) -> str:
        return self.title

    class Meta:
        ordering = ('title',)


class Section(models.Model):
    menu = models.ForeignKey(
        Menu,
        related_name='sections',
        on_delete=models.CASCADE,
    )
    title = models.CharField('Название раздела', max_length=256,)
    url = models.URLField('Ссылка на страницу раздела', max_length=1024)
    parent = models.ForeignKey(
        'self',
        related_name='child_section',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    def __str__(self) -> str:
        return self.title

    class Meta:
        ordering = ('title',)
