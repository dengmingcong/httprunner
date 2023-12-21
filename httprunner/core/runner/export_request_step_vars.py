from httprunner.models import TStep


def export_request_step_variables(step: TStep) -> dict:
    """Export variables from step request (HTTP request)."""
    export_mapping = {}

    # export local variables to make them usable for steps next
    for var in step.globalize:
        if isinstance(var, dict):
            if len(var) != 1:
                raise ValueError(
                    f"length of dict can only be 1 but got {len(var)} for: {var}"
                )
            local_var_name = list(var.keys())[0]
            export_as = list(var.values())[0]
        else:
            if not isinstance(var, str) or not var:
                raise ValueError(
                    "type of var can only be dict or str, and must not be empty"
                )
            local_var_name = var
            export_as = var

        if local_var_name not in step.variables:
            raise ValueError(
                f"failed to export local step variable {local_var_name}, "
                f"all step variables now: {step.variables.keys()}"
            )

        export_mapping[export_as] = step.variables[local_var_name]

    return export_mapping
