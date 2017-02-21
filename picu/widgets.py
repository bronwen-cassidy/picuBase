from django import forms

class SelectSearchWidget(forms.TextInput):

	class Media:
		extend = True

		css = {
			'all': ('picu/css/style.css',)
		}
		js = ('picu/js/select.functions.js',)