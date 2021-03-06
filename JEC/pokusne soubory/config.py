import cv2

TRAIN_LIST = "../../Data/image_labelling_datasets/iaprtc12/iapr_train_2009_2.txt"
TEST_LIST = "../../Data/image_labelling_datasets/iaprtc12/iapr_test_2009_3.txt"


DATAFILE_TRAIN = "../result/datafile_train.py"
DATAFILE_TEST = "../result/datafile_test.py"

DATEFILE_TEST_NEIGHBORS = "../result/datafile_test_neigbors.py"

KEYWORDS_RESULT = "../result/keywords_result.txt" #vysledky klicovych slov, jejich presnost a uplnost
PICTURE_RESULT = "../result/picture_result.txt" #obrazky a prirazene klicova slova klasifikatorem
PICTURE_TEST_KEYWORDS = "../result/test_keywords.txt" #obrazky s prirazenym slovy od klasifikatoru i s se slovy prirazene clovekem

COUNT_NEIGHBORS = 5
COUNT_KEYWORDS = 5


#nastaveni priznaku
#KL - divergence cv2.HISTCMP_KL_DIV
#euklidovska v2.NORM_L1
RGB = True
RGB_DISTANCE = cv2.NORM_L1 # hele tohle neni uplne dobrej napad mas tam totiz dve metody compare a norm
LAB = True
LAB_DISTANCE = cv2.HISTCMP_KL_DIV 
HSV = True
HSV_DISTANCE = cv2.NORM_L1

