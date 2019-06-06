class MultiEndpointsViewMixin(TemplateView):
    """
    The base class implements the architecture of
    multi endpoints based on single view.

    How to use mixin:
    ----------

    class SomeView(MultiEndpointsViewMixin):
        POST_VIEWS = {
            'action_name': method_name,
            # Add here other actions
        }

        def method_name:
            pass
    """

    #: Dict to store all available POST handlers
    POST_VIEWS = {}
    #: Dict to store all available GET handlers
    GET_VIEWS = {}

    _POST_TYPE = 'post'

    def get_action_handler(self, action: str, method: Optional[str] = None):
        """
        Returns the name of handler for given action.

        Parameters
        ----------
        action: str
            The name of handler for the action.
        method: str
            The type of request method
        """
        if method == self._POST_TYPE:
            if action in self.POST_VIEWS:
                return getattr(self, self.POST_VIEWS.get(action))
        else:
            if action in self.GET_VIEWS:
                return getattr(self, self.GET_VIEWS.get(action))

    def get(self, request, **kwargs):
        """
        Returns GET handler according action type.
        """
        action = request.GET.get('action')
        data = request.GET.get('data')
        handler_fn = self.get_action_handler(action)

        if isinstance(data, str):
            data = json.loads(data)

        if handler_fn:
            return handler_fn(request, data, **kwargs)
        else:
            context = self.get_context_data(**kwargs)
            return self.render_to_response(context)

    def post(self, request, **kwargs):
        """
        Returns POST handler according action type.
        """
        data = json.loads(request.body)

        action = data.pop('action')
        data = data.pop('data')
        handler_fn = self.get_action_handler(action, self._POST_TYPE)

        if handler_fn:
            return handler_fn(request, data, **kwargs)
        raise Http404()
