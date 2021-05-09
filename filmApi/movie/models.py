from django.db import models


# Create your models here.

# 电影信息
class Movie(models.Model):
    movie_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)  # 电影名称
    info = models.TextField()  # 电影简介
    poster = models.ImageField(upload_to='img')  # 电影海报
    director = models.CharField(max_length=50)  # 电影导演
    duration = models.IntegerField()  # 电影时长

    class Meta:
        verbose_name = "movie"

    def __str__(self):
        return self.name


# 用户信息
class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=32)
    password = models.CharField(max_length=32)

    class Meta:
        verbose_name = "user"

    def __str__(self):
        return self.username


# 用户认证
class UserToken(models.Model):
    username = models.OneToOneField(to='User', on_delete=models.CASCADE)
    token = models.CharField(max_length=60)

    class Meta:
        verbose_name = "user_token"


# 用户评论
class Comment(models.Model):
    score = (
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5),
    )

    comment_id = models.AutoField(primary_key=True)  # 评论id
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)  # 用户id
    movie_id = models.ForeignKey(Movie, on_delete=models.CASCADE)  # 电影id
    user_score = models.IntegerField(choices=score, default=3)  # 用户评分
    comment_date = models.DateField(auto_now=True)  # 评论日期
    comment_content = models.TextField(max_length=140)  # 用户评论

    class Meta:
        verbose_name = "comment"

    def __str__(self):
        return str(self.comment_id) + ':' + str(self.comment_content)[:10]


# 电影院信息
class Cinema(models.Model):
    cinema_id = models.AutoField(primary_key=True)
    cinema_name = models.CharField(max_length=32, unique=True)

    class Meta:
        verbose_name = "cinema"

    def __str__(self):
        return self.cinema_name


# 放映厅
class Hall(models.Model):
    hall_id = models.AutoField(primary_key=True)
    cinema_id = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=32)

    class Meta:
        verbose_name = "hall"

    def __str__(self):
        return self.name


# 排片
class Schedule(models.Model):
    schedule_id = models.AutoField(primary_key=True)
    movie_id = models.ForeignKey(Movie, on_delete=models.CASCADE)
    hall_id = models.ForeignKey(Hall, on_delete=models.CASCADE)
    show_date = models.DateTimeField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    seat_info = models.TextField()

    class Meta:
        verbose_name = "schedule"


# 用户订单
class Order(models.Model):
    pay_types = (
        (1, '支付宝'),
        (2, '微信'),
    )

    order_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)  # 用户
    schedule_id = models.ForeignKey(Schedule, on_delete=models.CASCADE)  # 场次信息
    order_seat_info = models.CharField(max_length=100)  # 座位信息
    pay_type = models.IntegerField(choices=pay_types, default=1)  # 付费方式

    class Meta:
        verbose_name = "order"
