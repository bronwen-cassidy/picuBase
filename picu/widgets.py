from django.contrib.admin.widgets import ManyToManyRawIdWidget
from django.utils.safestring import mark_safe


class SearchDataListWidget(ManyToManyRawIdWidget):

	template_name = 'picu/reload_datalist.html'
	allow_multiple_selected = True

	def __init__(self, rel, admin_site, attrs=None, using=None):
		super().__init__(rel, admin_site, attrs, using)

	def render(self, name, value, attrs=None):
		output = [super(SearchDataListWidget, self).render(name, value, attrs)]
		if value:
			for v in value:
				curr_model = self.rel.model.objects.get(id=v)
				str_data =  '<div related-field="id_' + str(name) + '  related-value="' + str(v) + '" " class="related-display-input" onclick="clearRelatedSelectedId(this)" >' + str(v) + ': ' + curr_model.render() + '</div>'
				output.append(str_data)
		return mark_safe(''.join(output))

	def base_url_parameters(self):
		return None


	class Media:
		extend = True
		css = {
			'all': ('picu/css/style.css',)
		}
		js = ('picu/js/select.functions.js',)


"""
class DiagnosisRelatedFieldWidgetWrapper(RelatedFieldWidgetWrapper):
"""



