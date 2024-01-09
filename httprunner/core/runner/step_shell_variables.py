from httprunner.models import TStep
from httprunner.utils import merge_variables


def get_step_shell_variables(step: TStep, session_variables: dict) -> dict:
    """Get shell variables for step."""
    # parsed parametrize variables > extracted variables > testcase config variables.
    # Note: parsed parametrize variables will be used in skip_if and skip_unless condition
    # fix: variables added by parametrized step should not be exported
    if step.parsed_parametrize_vars:
        # word 'shell' is relative to 'core'
        return merge_variables(step.parsed_parametrize_vars, session_variables)
    else:
        return session_variables
