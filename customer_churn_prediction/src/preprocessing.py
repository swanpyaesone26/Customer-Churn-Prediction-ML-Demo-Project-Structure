from sklearn.preprocessing import OneHotEncoder
import pandas as pd


def build_encoder():
	"""Return a OneHotEncoder fitted to the training categorical scheme.

	The encoder matches the original training categories for 'Geography' and
	'Gender' so downstream code can rely on stable feature names.
	"""
	encoder = OneHotEncoder(drop="if_binary", sparse_output=False, handle_unknown="ignore")
	encoder.fit(pd.DataFrame({
		"Geography": ["France", "Germany", "Spain"],
		"Gender": ["Male", "Female", "Male"],
	})[["Geography", "Gender"]])
	return encoder

