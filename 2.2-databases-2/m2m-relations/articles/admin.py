from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet

from .models import Article, Tag, Scope


class RelationshipInlineFormset(BaseInlineFormSet):
    def clean(self):
        total_tags = 0

        for form in self.forms:
            main_tag = form.cleaned_data.get('is_main', 0)
            total_tags += int(main_tag)

            if total_tags > 1:
                raise ValidationError('Основным может быть только один раздел')

            elif total_tags == 0:
                raise ValidationError('укажите основной раздел')

        return super().clean()


class ScopeInline(admin.TabularInline):
    model = Scope
    extra = 3
    formset = RelationshipInlineFormset


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    inlines = (ScopeInline, )


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass
