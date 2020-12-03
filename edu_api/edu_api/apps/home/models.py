from django.db import models


class BaseModel(models.Model):
    """基础表"""
    is_show = models.BooleanField(default=False, verbose_name="是否显示")
    orders = models.IntegerField(default=1, verbose_name="图片排序")
    is_delete = models.BooleanField(default=False, verbose_name="是否删除")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        # 声明此属性后，不会再数据库为此表创建对应的表结构
        abstract = True


class Banner(models.Model):
    """
    轮播图模型
    """
    img = models.ImageField(upload_to="banner", max_length=256, verbose_name="轮播图片")
    link = models.CharField(max_length=256, verbose_name="图片链接")
    title = models.CharField(max_length=80, verbose_name="图片标题")
    is_show = models.BooleanField(default=False, verbose_name="是否显示")
    orders = models.IntegerField(default=1, verbose_name="图片排序")
    is_delete = models.BooleanField(default=False, verbose_name="是否删除")

    class Meta:
        db_table = "bz_banner"
        verbose_name = "轮播图"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title


class Nav(BaseModel):
    """导航栏"""

    POSITION_OPTION = (
        (1, "顶部导航"),
        (2, "底部导航"),
    )

    title = models.CharField(max_length=80, verbose_name="导航标题")
    link = models.CharField(max_length=256, verbose_name="导航链接")
    is_site = models.BooleanField(default=False, verbose_name="是否是外部链接")
    is_position = models.IntegerField(choices=POSITION_OPTION, default=1, verbose_name="导航栏位置")

    class Meta:
        db_table = "bz_nav"
        verbose_name = "导航栏"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title
