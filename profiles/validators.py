"""

The **profiles.validators.py** file involves specific methods that validates the input entered into the Settings field (through Edit Settings) if it meets minimum requirements.

"""
import re

from django.core.exceptions import ValidationError
from django.core.validators import URLValidator

def validate_alphanumeric(value):
	"""Checks if the input only includes alphanumeric characters.

	**Arguments:**
		* value: the string input in the field.

	**Raises:**
		* Validation Error:
			``Must only be in alphanumeric characters``

	"""
	if not re.match("^[\w]+$", value):
		raise ValidationError(u"Must only be in alphanumeric characters")

def validate_exclude_space(value):
	"""Checks if the input does not contain any whitespaces

	**Arguments:**
		* value: the string input in the field.

	**Raises:**
		* Validation Error:
			``Must not include whitespaces``

	"""
	if re.search("\s", value):
		raise ValidationError(u"Must not include whitespaces")

def validate_not_spaces(value):
	"""
	Checks if the input is not all whitespaces

	**Arguments:**
		* value: the string input in the field.

	**Raises:**
		* Validation Error:
			``All whitespaces are not valid.``

	"""
	if not value.strip():
		raise ValidationError(u"All whitespaces are not valid.")