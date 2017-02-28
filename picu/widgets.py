import floppyforms as forms

class SearchDataListWidget(forms.widgets.Input):

	template_name = 'picu/reload_datalist.html'

	class Media:
		extend = True
		css = {
			'all': ('picu/css/style.css',)
		}
		js = ('picu/js/select.functions.js',)