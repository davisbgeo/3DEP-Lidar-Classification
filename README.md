# 3DEP-Lidar-Classification
A script that allows the user to process data retrieved from the 3DEP Lidar Explorer and classify it using Esri Deep Learning Packages. The script has two basic functions--download and extract LAZ files from a list of urls, and then perform a point cloud classification for power lines, buildings, and trees. The script will iterate through multiple LAS files for each deep learning package.

This tool requires some knowledge of python to use effectively. It is not setup to run out of the box.

## Overall Flow
```Mermaid
graph TD
downloadFiles-->extractLAS-->buildPyramid-->lasdStatistics-->classifyPointCloud-->lasdStatistics-->buildPyramid
classifyPointCloud-->powerLines
classifyPointCloud-->buildings
classifyPointCloud-->trees
downloadFiles[Download Files]
extractLAS[Extract LAS]
buildPyramid[Build Pyramids]
lasdStatistics[Calculate LASD Stats]
classifyPointCloud[Classify Point Clouds]
powerLines[[Power Lines]]
buildings[[Buildings]]
trees[[Trees]]
```

## Iteration through each deep learning package and LAS file
```Mermaid
graph LR
start-->a--Yes-->d
a--No-->stop
d-->b-->c--Yes-->b
c--No-->a
start([start])
a@{ shape: diamond, label: "More Deep Learning Packages"}
b[Process LAS]
c@{ shape: diamond, label: "More LAS Files"}
d[Move to Next Deep Learning Package]
stop([end])

```