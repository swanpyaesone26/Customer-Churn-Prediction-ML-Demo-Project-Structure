import pandas as pd
from sklearn.preprocessing import OneHotEncoder


def preprocess_features(df):
    """
    Function of OneHotEncoding for Geography and Gender columns.
    Args:
        df (pd.DataFrame): Input DataFrame containing the features to be encoded.
    """
    ohe = OneHotEncoder(drop="if_binary", sparse_output=False)

    # Columns to encode
    cols_to_encode = ["Geography", "Gender"]

    encoded_features = ohe.fit_transform(df[cols_to_encode])
    new_cols = ohe.get_feature_names_out(cols_to_encode)

    # Construct new DataFrame
    encoded_df = pd.DataFrame(encoded_features, columns=new_cols, index=df.index)

    # Drop original columns and concatenate encoded columns
    df_final = pd.concat([df.drop(cols_to_encode, axis=1), encoded_df], axis=1)

    return df_final, ohe
