import cv2

TRAIN_LIST = "../../Data/iaprtc12/iapr_train_2009_pulka_1.txt"
#TRAIN_LIST = "../../Data/ESP-ImageSet/esp_train_2009_pulka_2.txt"
TEST_LIST = "../../Data/iaprtc12/iapr_test_2009.txt"
#TEST_LIST = "../../Data/ESP-ImageSet/esp_test_2009.txt"


#DATAFILE_TRAIN = "../result/datafile_train.pyc"
DATAFILE_TRAIN = "../result/datafile_train_pulka_1.pyc"
DATAFILE_TRAIN2 = "../result/datafile_train_pulka_2.pyc"
DATAFILE_TEST = "../result/datafile_test.pyc"

#DATEFILE_TEST_NEIGHBORS = "../result/datafile_test_neigbors.py"

PICTURE_RESULT = "../result/picture_result.txt" #obrazky a prirazene klicova slova klasifikatorem
PICTURE_ALL_KEYWORDS = "../result/test_all_keywords.txt" #obrazky s prirazenym slovy od klasifikatoru i s se slovy prirazene clovekem
KEYWORDS_RESULT = "../result/keywords_result.txt" #vysledky klicovych slov, jejich presnost a uplnost

COUNT_NEIGHBORS = 8
COUNT_KEYWORDS = 5

#Pri hodnote "TH" bude pouzita s prahem, pri jakokoliv jine hodnote bude nacten originalni z JEC
LABEL_TRANSFER = "STANDARD"

#nastaveni priznaku
#KL - KL divergence
#L1 
#L2
RGB = True
RGB_DISTANCE = "L1" 
LAB = True
LAB_DISTANCE = "KL" 
HSV = True
HSV_DISTANCE = "L1"
GABOR = True
GABOR_DISTANCE = "L1"
GABORQ = True
GABORQ_DISTANCE = "L1"
HAAR = True
HAAR_DISTANCE = "L1"
HAARQ = True
HAARQ_DISTANCE = "L1"
POEM = False
POEM_DISTANCE = "L1"
COLOR_POEM = False
COLOR_POEM_DISTANCE = "L1"