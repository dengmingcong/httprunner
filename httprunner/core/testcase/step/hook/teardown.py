from httprunner.models import TStep


class TeardownHookMixin:
    """Mixin representing teardown hook."""

    _step_context: TStep

    def teardown_hook(self, hook: str, assign_var_name: str = None):
        if assign_var_name:
            self._step_context.teardown_hooks.append({assign_var_name: hook})
        else:
            self._step_context.teardown_hooks.append(hook)

        return self
