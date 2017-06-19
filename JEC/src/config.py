import cv2


TRAIN_LIST = "../../Data/iaprtc12/iapr_train_2009_2.txt" # cesta k trenovacimu souboru. 
TEST_LIST = "../../Data/iaprtc12/iapr_test_2009_2.txt" #cesta k testovacimu souboru

#mezivysledek, cesta k souboru do ktreho budou ulozeny priznakove vektory z nactenych obrazku z trenovaci sady, predpokladany format .pyc
DATAFILE_TRAIN = "../result/iaprtc12_JEC_datpulka_.pyc" 
#DATAFILE_TRAIN2 = "../result/iaprtc12_JEC_datafile_train_pulka_2.pyc" # pomucka pri malem poctu RAM
#mezivysledek, cesta k souboru do ktreho budou ulozeny priznakove vektory z nactenych obrazku z testovaci sady, predpokladany format .pyc
DATAFILE_TEST = "../result/iaprtc12_JEC_datafile_test.pyc"

PICTURE_RESULT = "../result/picture_result.txt" #obrazky a prirazene klicova slova klasifikatorem
PICTURE_ALL_KEYWORDS = "../result/test_all_keywords.txt" #obrazky s prirazenym slovy od klasifikatoru i s se slovy prirazene clovekem
KEYWORDS_RESULT = "../result/keywords_result.txt" #vysledky klicovych slov, jejich presnost a uplnost

COUNT_NEIGHBORS = 10 # pocet knn (k nejblizsich sousedu)
COUNT_KEYWORDS = 5 # pocet klicovych slov, vyuzivano hlavne v label transfer uvedeneho u algoritmu JEC

#Pri hodnote "TH" bude pouzita s prahem, pri jakokoliv jine hodnote bude nacten originalni z JEC
LABEL_TRANSFER = "TH"

#nastaveni priznaku
#nazev priznaku = True - priznak bude pouzit.
#priznak_DISTANCE = udava ktera vzdalenost se ma pouzit pri porovnavani histogramu pro dany deskriptor.
#KL - KL divergence
#L1 
#L2
RGB = False
RGB_DISTANCE = "L1" 
LAB = False
LAB_DISTANCE = "KL" 
HSV = False
HSV_DISTANCE = "L1"
GABOR = False
GABOR_DISTANCE = "L1"
GABORQ = False
GABORQ_DISTANCE = "L1"
HAAR = False
HAAR_DISTANCE = "L1"
HAARQ = True
HAARQ_DISTANCE = "L1"
POEM = False
POEM_DISTANCE = "L1"
COLOR_POEM = False
COLOR_POEM_DISTANCE = "L1"
