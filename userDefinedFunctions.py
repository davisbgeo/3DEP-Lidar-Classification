import arcpy, os, ssl
from urllib.request import urlretrieve
ssl._create_default_https_context = ssl._create_unverified_context

def buildPyramid(las_dataset):
    # Needed to make las dataset more performant
    arcpy.management.BuildLasDatasetPyramid(
    las_dataset,
    'Closest to Center'
    )
def classifyPointCloud(
    las_dir,  # directory where las files are saved
    dlpk_dir, # directory where deep learning packages are saved
    skip_list=None # list of las files to skip in the las directory
    ):
    # classify LAS data based on deep learning packages
    dlpk_list = os.listdir(dlpk_dir)
    las_list = filterFiles(las_dir,'.las')
    for dlpk in dlpk_list:
        dlpk_path = f"{dlpk_dir}\{dlpk}"
        arcpy.AddMessage(f"Working on {dlpk_path}")
        for las in las_list:
            if las in skip_list:
                print(f"skipped {las}")
                pass
            else:
                print(f"processing {las} for {dlpk}")
                arcpy.ddd.ClassifyPointCloudUsingTrainedModel(
                    las,
                    dlpk_path,
                    determineOutputClasses(dlpk),
                    'EDIT_SELECTED',
                    [1] #only unassigned class is updated
                )
def determineOutputClasses(dlpk):
    # The Downloaded Deep Learning Packages
    if dlpk == "PointCNN_PowerLines.dlpk":
        return [14, 15]
    elif dlpk == 'building_point_classification.dlpk':
        return [6]
    elif dlpk == 'Tree_point_classification.dlpk':
        return[5]
def downloadFiles(workspace,script_dir,laz_dir,url_file):

    # Open the file in read mode
    with open(url_file, 'r') as file:
        # Read the content and split by lines
        url_list = file.readlines()

    # Strip newline characters from each line
    url_list = [line.strip() for line in url_list]

    # Download file at each url
    for url in url_list:
        file_path = f"{laz_dir}\{url.split('_')[-1]}"
        urlretrieve(url,file_path)
def extractLAS(laz_dir,las_dir,las_dataset):
    # Converts LAZ files to LAS, needed for ArcGIS
    laz_list = os.listdir(laz_dir)
    arcpy.conversion.ConvertLas(
        laz_dir,
        las_dir,
        las_options = ['REMOVE_VLR', 'REMOVE_EXTRA_BYTES', 'REARRANGE_POINTS'],
        out_las_dataset = las_dataset
    )
def filterFiles(dir, ext):
    # get a list of file paths for a given file extention
    # in a directory
    file_list = []
    for file in os.listdir(dir):
        if file.endswith(ext):
            file_list.append(f"{dir}\{file}")
    return file_list
def lasdStatistics(             # Calculate statistics on a lasd dataset, which provides a statistics report and also builds spatial and attribute indexes
    las_dataset,                # The input dataset on which statistics will be calculated              
    lasd_stats_dir,status,      # The folder location where the stats file will be saved
    skip_existing=True,         # Indicates whether stats are being run "before" or "after" the classification
    individual_las_calc=False   # True means stats will be calculated for individual LAS files, False means they'll be calculated for the whole dataset
    ):
    if status == "before":
        lasd_stats = f"{lasd_stats_dir}\statsBeforeClassification.txt"
    elif status == "after":
        lasd_stats = f"{lasd_stats_dir}\statsAfterClassification.txt"
    
    if skip_existing == True:
        calc_type= 'SKIP_EXISTING_STATS'
    elif skip_existing == False:
        calc_type = 'OVERWRITE_EXISTING_STATS'

    if individual_las_calc==True:
        summary_lvl='LAS_FILES'
    elif individual_las_calc==False:
        summary_lvl='DATASET'

    arcpy.management.LasDatasetStatistics(
        las_dataset,
        calc_type,
        lasd_stats,
        summary_lvl
    )
