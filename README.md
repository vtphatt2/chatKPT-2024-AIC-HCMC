# chatKPT-2024-AIC-HCMC
The chatKPT team's source code repository for The 2024 AI Challenge HCMC

# Members
| **Name**| **Major**| **University**|
|-|-|-|
| Vo Thinh Phat | Computer Science  | University of Science (VNUHCM) |
| Mai Dang Khoa | Computer Science  | University of Science (VNUHCM) |
| Nguyen Quoc Thang | Information Technology  | University of Science (VNUHCM) |
| Duong Quang Thang | Information Technology  | University of Science (VNUHCM) |
| Ly Nguyen Khang  | Computer Science | University of Technology (VNUHCM) |

# Data organization
All data provided by Organizing Committee is stored in folder **data**

There will be 3 data provision times corresponding to three folders **batch1**, **batch2**, **batch3** 
(path : "data/batch1", "data/batch2", "data/batch3")

In the **batch1** folder (the other two folders are organized similarly), there will be 6 main folders with corresponding paths:

- **video** : data/batch1/video/L0#_V###.mp4 (I don't push any sample video data into github because the storage is too large)

- **clip-features-32** : data/batch1/clip-features-32/L0#_V###.npy

- **keyframes** : data/batch1/keyframes/keyframes_L0#/L0#_V00#/###.jpg
    - For example :
        - data/batch1/keyframes/keyframes_L01/L01_V001/020.jpg
        - data/batch1/keyframes/keyframes_L02/L02_V003/021.jpg

- **map-keyframes** : data/batch1/map-keyframes/L0#_V###.csv

- **metadata** : data/batch1/metadata/L0#_V###.json

- **objects** : data/batch1/objects/L0#_V###/####.json
    - For example :
        - data/batch1/objects/L01_V001/0001.json
        - data/batch1/objects/L02_V002/0003.json

**NOTE:** This is not the complete dataset provided by the Organizing Committee; it is merely a guide on how we organize the data. Kindly maintain this structure and replace it with the actual data downloaded from the Google Sheet : https://docs.google.com/spreadsheets/d/1mO3zS79L1HMLZ-BLpyy8E-n9RROOElms5DS_Gi1gKiU/edit?usp=sharing

