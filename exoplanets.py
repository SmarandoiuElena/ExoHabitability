import pandas as pd
from sklearn.model_selection import train_test_split

NASA_URL = (
    "https://exoplanetarchive.ipac.caltech.edu/TAP/sync"
    "?query=select+"
    "pl_name,pl_rade,pl_bmasse,pl_eqt,"
    "pl_orbper,pl_orbeccen,pl_orbsmax,pl_insol,"
    "st_teff,st_rad,st_mass,st_met"
    "+from+pscomppars"
    "&format=csv"
)

# Here we have al the collums we need from the NASA site
df_nasa = pd.read_csv(NASA_URL)
# Here we have the data from PHL, a simplified astronomy catalog
df_hwc = pd.read_csv("hwc.csv")

cols = [
    'P_NAME',
    'P_HABITABLE',
    "P_ESI",
    "P_HABZONE_CON",
    "P_HABZONE_OPT",
    "P_TEMP_SURF",
    "P_TYPE",
]

# We filter only some of the collums
df_hwc = df_hwc[cols]
# We combine the two data sets
df_hwc['pl_name'] = df_hwc['P_NAME'].copy()
df_merge = df_nasa.merge(df_hwc, on = 'pl_name', how = "inner")
# We get rid of the rows where thins are missing
df_fin = df_merge.dropna()

df_fin.to_csv("exoplanests.csv", index = False)
