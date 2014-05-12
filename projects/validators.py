import re

from django.core.exceptions import ValidationError



def validate_not_spaces(value):
    """
    A simple validation function in which 

    :param value: The value to be evaluated.

    Raises: :py:class:`ValidationError`
    
    """
    if not value.strip():
        raise ValidationError(u"You must provide more than just whitespace.")

def validate_alphanumeric(value):
    """
    A function that validates the user input such that the input must only contain the following:

    * alphanumeric
    * underscores
    * dashes
    * spaces

    :param value: The value to be evaluated.

    Raises: :py:class:`ValidationError`

    """
    if not re.match("^[\w\s-]+$", value):
		raise ValidationError(u"This field can only consist of alphanumeric characters, underscores, dashes, and spaces.")
