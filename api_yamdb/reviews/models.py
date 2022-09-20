from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

roles = (
    ('user', 'Пользователь'),
    ('moderator', 'Модератор'),
    ('admin', 'Администратор')
)


class User(AbstractUser):
    """Модель пользователя"""

    username = models.CharField(
        max_length=150,
        unique=True,
        verbose_name='Никнейм',
        db_index=True,
        help_text='Никнейм пользователя'
    )
    email = models.EmailField(
        max_length=254,
        unique=True,
        verbose_name='Электронная почта',
        help_text='Электронная почта пользователя'
    )
    first_name = models.CharField(
        max_length=150,
        verbose_name='Имя',
        help_text='Имя пользователя',
        blank=True,
        null=True
    )
    last_name = models.CharField(
        max_length=150,
        null=True,
        verbose_name='Фамилия',
        help_text='Фамилия пользователя',
        blank=True
    )
    bio = models.TextField(
        blank=True,
        null=True,
        help_text='Информация о себе',
        verbose_name='Биография'
    )
    role = models.CharField(
        max_length=50,
        default='user',
        choices=roles,
        verbose_name='Роль',
        help_text='Роль пользователя'
    )

    @property
    def is_moderator(self):
        return self.role == 'moderator'

    @property
    def is_admin(self):
        return self.role == 'admin' or self.is_superuser

    class Meta:
        ordering = ('username',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        constraints = [
            models.UniqueConstraint(
                fields=['username', 'email'],
                name='unique_user'
            )
        ]

    def __str__(self):
        return self.username


class Category(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name='Название категории',
        help_text='Название категории',
    )
    slug = models.SlugField(unique=True, max_length=20)

    class Meta:
        ordering = ('id',)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name='Название жанра',
        help_text='Название жанра',
    )
    slug = models.SlugField(unique=True, max_length=20)

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(
        max_length=20,
        verbose_name='Произведение',
        help_text='Назвение произведения',
    )
    year = models.IntegerField(
        help_text='Год выпуска',
    )
    genre = models.ManyToManyField(
        Genre,
        blank=True,
        related_name='titles',
        verbose_name='Жанр',
        help_text='Жанр произведения',
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name='titles',
        null=True,
        blank=True,
        verbose_name='Категория',
        help_text='Категория произведения',
    )
    description = models.CharField(
        max_length=100,
        null=True,
        verbose_name='Описание',
        help_text='Описание произведения',
    )


class Review(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор',
        help_text='Автор отзыва',
    )
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Произведение',
        help_text='Произведение, к которму относится отзыв',
    )
    text = models.TextField(
        verbose_name='Отзыв',
        help_text='Текст отзыва',
    )
    score = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        verbose_name='Рейтинг',
        help_text='Рейтинг произведения',
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name='Дата',
        help_text='Дата публикации отзыва',
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='unique review')
        ]


class Comments(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор',
        help_text='Автор комментария',
    )
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Отзыв',
        help_text='Отзыв, на который оставлен комментарий',
    )
    text = models.TextField(
        verbose_name='Текст',
        help_text='Текст комментария',
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name='Дата',
        help_text='Дата публикации комментария',
    )


class GenreTitle(models.Model):
    genre = models.ForeignKey(
        Genre,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name='Жанр',
        help_text='Жанр',
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name='Произведение',
        help_text='Произведение',
    )

    def __str__(self):
        return f'{self.genre}  ---  {self.title}'
