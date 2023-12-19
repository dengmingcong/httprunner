from httprunner.models import TStep


class SetupHookMixin:
    _step_context: TStep

    def setup_hook(self, hook: str, assign_var_name: str = None):
        if assign_var_name:
            self._step_context.setup_hooks.append({assign_var_name: hook})
        else:
            self._step_context.setup_hooks.append(hook)
        return self
