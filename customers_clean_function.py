import pandas as pd


def normalize_titles(col):
    return col.strip().lower().replace(" ", "_")


def clean_gender(x):
    if pd.isna(x):
        return None
    x = x.strip().lower()
    if x in ["f", "female", "femal"]:
        return "F"
    elif x in ["m", "male"]:
        return "M"
    else:
        return None


def clean_column_names(df):
    df.columns = df.columns.map(normalize_titles)
    df = df.rename(columns={"st":"state","monthly_premium_auto":"monthly_premium","number_of_open_complaints":"open_complaints","total_claim_amount":"total_claim"})
    return df


def clean_invalid_values(df):
    df["gender"] = df["gender"].apply(clean_gender)
    state_map = {"Cali": "California","AZ": "Arizona","WA": "Washington" }
    df["state"] = df["state"].replace(state_map)
    vehicle_map = {"Sports Car": "Luxury","Luxury SUV": "Luxury","Luxury Car": "Luxury"}
    df["vehicle_class"] = df["vehicle_class"].replace(vehicle_map)
    df["customer_lifetime_value"] = df["customer_lifetime_value"].str.replace("%", "")
    df["customer_lifetime_value"] = pd.to_numeric(df["customer_lifetime_value"])
    return df


def format_data_types(df):
    df["open_complaints"] = pd.to_numeric(df["open_complaints"].str.split("/").str[1])
    return df


def deal_with_nulls(df):
    df = df.dropna(how="all")
    df = df.dropna(subset=["customer_lifetime_value"])
    df["gender"] = df["gender"].fillna("Unknown")
    numeric_cols = df.select_dtypes(include="number").columns
    df[numeric_cols] = df[numeric_cols].astype(int)
    return df


def remove_duplicates(df):
    df = df.drop_duplicates().reset_index(drop=True)
    return df


def clean_customers_data(df):
    df = clean_column_names(df)
    df = clean_invalid_values(df)
    df = format_data_types(df)
    df = deal_with_nulls(df)
    df = remove_duplicates(df)
    return df