from fileMgmt import downloadFiles
from userDefinedFunctions import extractLAS, buildPyramid, lasdStatistics, classifyPointCloud

workspace = f"E:\Geospatial\Hermiston Lidar Classification"
script_dir = f"{workspace}\scripts"
laz_dir = f"{workspace}\laz_files"
url_file = f"{script_dir}\downloadlist.txt"
las_dir = f"{workspace}\las_files"
las_dataset = f"{las_dir}\Hermiston2019_3DEP.lasd"
dlpk_dir = f"{workspace}\dlpk"
lasd_stats_dir = f"{workspace}\lasd_stats"
skip_list = [''] # If script fails, input full paths to files already run here

downloadFiles(workspace,script_dir,laz_dir,url_file)
extractLAS(laz_dir, laz_dir, las_dataset)
buildPyramid(las_dataset)
lasdStatistics(las_dataset,lasd_stats_dir,"before")
classifyPointCloud(laz_dir, dlpk_dir,skip_list)
lasdStatistics(las_dataset,lasd_stats_dir,"after",True,True)
buildPyramid(las_dataset)