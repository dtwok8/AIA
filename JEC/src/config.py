import cv2


TRAIN_LIST = "../../Data/iaprtc12/iapr_train_2009_pulka_2.txt" # cesta k trenovacimu souboru. 
#TRAIN_LIST = "../../Data/ESP-ImageSet/esp_train_2009_pulka_2.txt"
TEST_LIST = "../../Data/iaprtc12/iapr_test_2009.txt" #cesta k testovacimu souboru
#TEST_LIST = "../../Data/ESP-ImageSet/esp_test_2009.txt"

#mezivysledek, cesta k souboru do ktreho budou ulozeny priznakove vektory z nactenych obrazku z trenovaci sady, predpokladany format .pyc
#DATAFILE_TRAIN = "../result/datafile_train.pyc"
DATAFILE_TRAIN = "../result/iaprtc12_POEM_datafile_train_pulka_2.pyc" 
DATAFILE_TRAIN2 = "../result/iaprtc12_POEM_datafile_train_pulka_2.pyc"
#mezivysledek, cesta k souboru do ktreho budou ulozeny priznakove vektory z nactenych obrazku z testovaci sady, predpokladany format .pyc
DATAFILE_TEST = "../result/iaprtc12_POEM_datafile_test.pyc"

PICTURE_RESULT = "../result/picture_result.txt" #obrazky a prirazene klicova slova klasifikatorem
PICTURE_ALL_KEYWORDS = "../result/test_all_keywords.txt" #obrazky s prirazenym slovy od klasifikatoru i s se slovy prirazene clovekem
KEYWORDS_RESULT = "../result/keywords_result.txt" #vysledky klicovych slov, jejich presnost a uplnost

COUNT_NEIGHBORS = 5 # pocet knn (k nejblizsich sousedu)
COUNT_KEYWORDS = 5 # pocet klicovych slov, vyuzivano hlavne v label transfer uvedeneho u algoritmu JEC

#Pri hodnote "TH" bude pouzita s prahem, pri jakokoliv jine hodnote bude nacten originalni z JEC
LABEL_TRANSFER = "STANDART"

#nastaveni priznaku
#nazev priznaku = True - priznak bude pouzit.
#priznak_DISTANCE = udava ktera vzdalenost se ma pouzit pri porovnavani histogramu pro dany deskriptor.
#KL - KL divergence
#L1 
#L2
RGB = True
RGB_DISTANCE = "L1" 
LAB = True
LAB_DISTANCE = "KL" 
HSV = True
HSV_DISTANCE = "L1"
GABOR = False
GABOR_DISTANCE = "L1"
GABORQ = False
GABORQ_DISTANCE = "L1"
HAAR = False
HAAR_DISTANCE = "L1"
HAARQ = False
HAARQ_DISTANCE = "L1"
POEM = True
POEM_DISTANCE = "L1"
COLOR_POEM = False
COLOR_POEM_DISTANCE = "L1"