import pandas as pd
from sklearn.model_selection import train_test_split
import missingno as msno
import matplotlib.pyplot as plt

def show_missing_values(df, str):
    all = len(df)
    graph = msno.bar(df)

    for patch in graph.patches:
    
        val_pres = patch.get_height() * all
        val_empt = all - val_pres
        procent = (patch.get_height() * val_empt) / all * 100
    
        graph.text(
            patch.get_x() + patch.get_width() / 2,
            patch.get_height() - 0.05,
            f'{procent:.1f}%, {val_empt:.1f} lost {str}',
            ha='center', va='top',
            fontsize = 12, color='red', rotation=90
        )

    plt.title("Missing values in ")
    plt.tight_layout()
    plt.subplots_adjust(right = 0.736)
    plt.show()

NASA_URL = (
    "https://exoplanetarchive.ipac.caltech.edu/TAP/sync"
    "?query=select+"
    "pl_name,pl_rade,pl_bmasse,pl_eqt,"
    "pl_orbsmax,"
    "st_teff,st_rad,st_mass"
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

# We get rid of the rows where things are missing
df_fin = df_merge.dropna()

# save the file
df_fin.to_csv("exoplanets.csv", index = False)

# We split the data for the train and test files
train, test = train_test_split(
    df_fin,
    test_size = 0.25,
    random_state = 42,
    stratify=df_fin["P_HABITABLE"]
)

# Saving the files
train.to_csv("train.csv", index=False)
test.to_csv("test.csv", index=False)

# Now we the EDA analysis

# Showing the missing values
show_missing_values(df_merge, "in df_merge")
# Because the surface temperatures of planets are missing in proportion of 24% I chose
# to drop those rows. The surface temperature is important in determining the 
# habitability. If that value is not known we can't make a relevant prediction