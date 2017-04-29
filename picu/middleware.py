class UrlHistoryMiddleware(object):
	url_history = []

	def __init__(self, get_response):

		self.get_response = get_response
	# One-time configuration and initialization.


	def __call__(self, request):
		# Code to be executed for each request before
		# the view (and later middleware) are called.

		referrer = request.META.get('HTTP_REFERER')
		if referrer and referrer not in self.url_history and 'add' not in referrer and 'change' not in referrer and 'home' not in referrer:
			self.url_history.append(referrer)

		request.session['URL_HISTORY'] = self.url_history
		response = self.get_response(request)

		# Code to be executed for each request/response after
		# the view is called.

		return response
