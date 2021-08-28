from django.forms import ModelForm
from .models import Product,Banner,Image
from django.utils.translation import ugettext_lazy as _

class BannerForm(ModelForm):
    class Meta:
        model = Banner
        fields = (
            'banner_image',
            'is_show',
            'discount',
            'event',
            'describe',
        )
        labels={
            'banner_image': _('Ảnh Banner (1920x725), Background trắng          '),
            'is_show': _('Hiện thị trên trang web không?        '),
            'discount': _('Giảm giá cho sản phẩm trong banner      '),
            'event': _("Sự kiện của banner? "),
            'describe': _("Giới thiệu sự kiện banner")
        }

class BannerFormUpdate(ModelForm):
    class Meta:
        model = Banner
        fields = (
            'is_show',
            'discount',
            'event',
            'describe',
        )
        labels={
            'is_show': _('Hiện thị trên trang web không?        '),
            'discount': _('Giảm giá cho sản phẩm trong banner      '),
            'event': _("Sự kiện của banner? "),
            'describe': _("Giới thiệu sự kiện banner")
        }
class ImageForm(ModelForm):
    class Meta:
        model = Image
        fields =(
            'product_image',
        )
        labels={
            'product_image': _('Ảnh cho sản phẩm(170x170)')
        }
class PostForm(ModelForm):
    class Meta:
        model = Product
        fields = (
            'review_article',
            'specifications',
            'special_offer',
            'product_image',
        )
        labels = {
            'review_article': _('Bài đánh giá '),
            'specifications': _('Thông số kỹ thuật'),
            'special_offer': _('Khuyến mãi đặc biệt '),
            'product_image': _('Ảnh giởi thiệu sản phẩm(170x170)'),
        }

class PostFormUpdate(ModelForm):
    class Meta:
        model = Product
        fields = (
            'review_article',
            'specifications',
            'special_offer',
        )
        labels = {
            'review_article': _('Bài đánh giá '),
            'specifications': _('Thông số kỹ thuật'),
            'special_offer': _('Khuyến mãi đặc biệt '),
        }
