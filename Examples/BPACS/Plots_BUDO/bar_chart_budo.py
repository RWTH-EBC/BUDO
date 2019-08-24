import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt

import seaborn as sns
sns.set(style="whitegrid", color_codes=True)

# np.random.seed(sum(map(ord, "categorical")))
# titanic = sns.load_dataset("titanic")

# d = {'number of observations': [26, 18, 15, 11, 10, 9, 5, 4, 4, 3],
#      'categories_db': ["building",
#                     "floor device",
#                     "facility/site/\nplant",
#                     "trade",
#                     "room number \ndevice",
#                     "building section",
#                     "zone",
#                     "production line",
#                     "information focus",
#                     "business entity/\ntype of cost"]}

d = {'Anzahl der Beobachtungen': [26, 18, 15, 11, 10, 9, 5, 4, 4, 3],
     'Kategorien': ["Gebäude",
                    "Geschoss Gerät",
                    "Liegenschaft/Standort/\nWerk",
                    "Gewerk",
                    "Raumnummer \nGerät",
                    "Gebäudeteil \nGerät",
                    "Zone",
                    "Fertigungslinie",
                    "Informationsschwerpunkt",
                    "Wirtschaftseinheit/\nKostengruppe"]}





df = pd.DataFrame(data=d)
sns.set_context("talk", font_scale=2.3)
#clrs = ['grey' if (x == 3) else "OrRd_r" for x in df.values ]
fig, ax = plt.subplots()
# fig.set_size_inches(16, 9)
fig.set_size_inches(32, 9)
pal = sns.color_palette('PuBu_r', 10)
abc=pal.as_hex()
abc[3]="#CD2626"

# plot=sns.barplot(x='categories_db',
#             y='number of observations',
# #            palette="OrRd_r",
#             palette=abc,
#             data=df)

plot=sns.barplot(x='Kategorien',
            y='Anzahl der Beobachtungen',
            palette=abc,
            data=df)


# plt.xlabel('categories_db', fontweight='bold')
# plt.ylabel('number of observations', fontweight='bold')

plt.xlabel('Kategorien', fontweight='bold')
plt.ylabel('Anzahl der Beobachtungen', fontweight='bold')


ax.set_ylim([0, 30])
plot.set_xticklabels(plot.get_xticklabels(), 
                     rotation=60,
                     ha="right",
                     rotation_mode='anchor')



#plot.set_size_inches(11.7, 8.27)
fig.savefig('plot_categories_standards.png', bbox_inches='tight')
