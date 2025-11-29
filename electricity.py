import pandas as pd
import geopandas as gpd
import pgeocode
import matplotlib.pyplot as plt

path_to_data = (r"C:/Users/LENOVO/Downloads/Postcode_level_all_meters_electricity_2023.csv")
df = pd.read_csv(path_to_data)

print("Shape:", df.shape)
print("Columns:", df.columns)

postcode_col = "Postcode"   
value_col = "Total_kWh" 

# Prepare postcodes as strings
postcodes = df[postcode_col].astype(str)

# Get coordinates only for UNIQUE postcodes
nomi = pgeocode.Nominatim("GB")   # GB = United Kingdom
unique_pcs = postcodes.unique()

coords_unique = nomi.query_postal_code(list(unique_pcs))
print("coords_unique shape:", coords_unique.shape)

# Build mapping from postcode -> lat/lon
coords_unique = coords_unique[["postal_code", "latitude", "longitude"]]
pc_to_lat = dict(zip(coords_unique["postal_code"], coords_unique["latitude"]))
pc_to_lon = dict(zip(coords_unique["postal_code"], coords_unique["longitude"]))

# Map back to the full dataframe
df["latitude"] = postcodes.map(pc_to_lat)
df["longitude"] = postcodes.map(pc_to_lon)

print(df[[postcode_col, "latitude", "longitude"]].head())

# Drop rows with no coordinates
df = df.dropna(subset=["latitude", "longitude"])

# Convert to GeoDataFrame
gdf = gpd.GeoDataFrame(
    df,
    geometry=gpd.points_from_xy(df["longitude"], df["latitude"]),
    crs="EPSG:4326"
)

print(gdf.head())

# Quick map
ax = gdf.plot(
    column=value_col,
    legend=True,
    figsize=(8, 10),
    markersize=2,
    alpha=0.7
)
plt.title(f"{value_col} by postcode")
plt.tight_layout()
plt.show()
