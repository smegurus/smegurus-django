from smegurus.settings import env_var
from smegurus import constants


def base_constants(request):
    """
    The purpose of this context processor is to attach all our constants
    to every request template.
    """
    return {
        'constants': constants,
    }
