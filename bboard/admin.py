from django.contrib import admin
from django.db.models import F
from bboard.models import Bb, Rubric


# def title_and_rubric(rec):
#     return f'{rec.title} ({rec.rubric.name})'

class PriceListFilter(admin.SimpleListFilter):
    title = 'Категория оценок'
    parameter_name = "price"

    def lookups(self, request, model_admin):
        return (
            ('low', 'Низкая цена'),
            ('medium', 'Средняя цена'),
            ('high', 'Высокая цена'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'low':
            return queryset.filter(price__lt=500)
        elif self.value() == 'medium':
            return queryset.filter(price__gte=500, price__lte=5000)
        elif self.value() == 'high':
            return queryset.filter(price__gte=5000)


@admin.action(description='Уменьшить цену вдвое')
def discount(modeladmin, request, queryset):
    f = F('price')
    for rec in queryset:
        rec.price = f / 2
        rec.save()
    modeladmin.message_user(request, 'Действие выполнено')


@admin.register(Bb)
class BbAdmin(admin.ModelAdmin):
    # list_display = ('title', 'content', 'price', 'published', 'rubric')
    # list_display = ('title_and_price', 'content', 'price', 'published', 'rubric')
    list_display = ('title_and_rubric', 'content', 'price', 'published', 'rubric')
    # list_display = (title_and_rubric, 'content', 'price', 'published', 'rubric')
    # list_display_links = ('title', 'content')
    # search_fields = ('title', 'content')

    # @admin.display(description='Название и рубрика', ordering='title')
    @admin.display(description='Название и рубрика', ordering='-title')
    # @admin.display(description='Название и рубрика', ordering='rubric__name')
    def title_and_rubric(self, rec):
        return f'{rec.title} ({rec.rubric.name})'

    # title_and_rubric.short_decsription = 'Название и рубрика'
    # title_and_rubric.admin_order_field = 'rubric_name'

    # def get_list_display(self, request):
    #     ld = ['title', 'content', 'price']
    #     if request.user.is_superuser:
    #         ld += ['published', 'rubric']
    #     return ld

    # list_display_links = ('title', 'content')

    # def get_list_display_links(self, request, list_display):
    #     return  list_display

    list_editable = ('price',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        else:
            return qs.filter(is_hidden=False)

    search_fields = ('title', 'content')
    list_filter = (PriceListFilter,'title', 'rubric__name')

    # fields = ('title', 'price', 'content')
    # fields = (('title', 'price'), 'content')
    # exclude = ('rubric', 'kind')
    fields = ('title', 'content', 'price', 'published')
    readonly_fields = ('published',)
    actions = (discount,)

    def discount(self, request, queryset):
        f = F('price')
        for rec in queryset:
            rec.price = f / 2
            rec.save()
        self.message_user(request, 'Действие выполнено')


class BbIline(admin.StackedInline):
    model = Bb
    extra = 1
    max_nuum = 3


@admin.register(Rubric)
class RubricAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'order')
    inlines = (BbIline,)





# admin.site.register(Bb, BbAdmin)
# admin.site.register(Rubric, RubricAdmin)
