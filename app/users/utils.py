from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.core.validators import RegexValidator
from rest_framework.pagination import PageNumberPagination
import os


def validate_image(value):
    valid_extensions = ['.jpg', '.jpeg', '.png', '.svg']
    ext = os.path.splitext(value.name)[1]
    if not ext.lower() in valid_extensions:
        raise ValidationError('Faqat JPG, JPEG, PNG, SVG  formatidagi rasmlarni yuklang.')

    max_size = 10 * 1024 * 1024
    if value.size > max_size:
        raise ValidationError('Rasm hajmi 4 MB dan katta bo\'lishi mumkin emas.')


phone_regex = RegexValidator(
    regex=r'^\+998([- ])?(90|91|93|94|95|98|99|33|97|71|88|20|77|50|55|)([- ])?(\d{3})([- ])?(\d{2})([- ])?(\d{2})$',
    message='Invalid phone number'
)


class CustomPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100
