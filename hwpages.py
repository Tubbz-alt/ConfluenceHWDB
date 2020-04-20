#
# To add a new HW type to the database, add the Class and Type (page title)
# to the classToType dictionary.
#

# The space where the HW Pages exist
HW_PAGE_SPACE = "airtrack"

## @brief Map device class to a list of valid hardware description pages.
#
# Valid titles for hardware description pages. 
classToType = dict(
    COB   = ["PC_248_101_01_C05", 
             "PC_248_101_01_C06", 
             "PC_248_101_01_C07", 
             "PC_248_101_01_C08",
             "PC_248_101_01_C09",
             "PC_248_101_01_C10",
             "PC_248_101_01_C11"],

    PGP_CARD =
            ["PC_260_101_02_C00",
             "PC_260_101_02_C01",
             "PC_260_101_02_C02",
             "PC_260_101_02_C03"],

    PGP_G3_CARD =
            ["PC_260_101_03_C00",
             "PC_260_101_03_C01",
             "PC_260_101_03_C02",
             "PC_260_101_03_C03"],

    EVR_CARD_G2 = ["PC_260_101_04_C02",],

    COB_RTM  = [ 
             "PC_248_101_20_C00", 
             "PC_248_101_20_C01", 
             "PC_248_101_20_C02", 
             "PC_248_101_20_C03", 
             "PC_248_101_20_C04", 
             "PC_248_101_20_C05", 
             "PC_248_101_28_C00", 
             "PC_248_101_28_C01", 
             "PC_248_101_28_C02", 
             "PC_248_101_31_C00", 
             "PC_248_101_31_C01", 
             "PC_248_101_31_C02", 
             "PC_256_100_84_C01", 
             "PC_256_100_85_C01"],


    LBNE_RTM = ["PC_264_810_02_C00",
             "PC_264_810_02_C01"],
    LCLS     = [
             "PC_261_100_53_C00",
             "PC_144_118_01_R1",
             "PC_144_119_02_R1",
             "PC_261_100_53_C00",
             "PC_261_100_53_C01",
             "PC_261_100_53_C02"],

    LCLS_II  = [
             "PC_376_210_01_C00",
             "PC_379_366_55_C01",
             "PC_379_396_25_C00"],

    RMB   = ["PC_256_100_86_C01"],
    
    ATLAS_GBT_RMB   = ["PC_256_100_94_C00"],

    AMC_CARRIER = [
             "PC_379_396_01_C00",
             "PC_379_396_01_C01",
             "PC_379_396_01_C02",
             "PC_379_396_01_C03",
             "PC_379_396_01_C04",
             "PC_379_396_01_C05",
             "PC_379_396_01_C06",
             "PC_379_396_01_C07"],
             
    AMC_CARRIER_GEN2  = [
             "PC_379_396_38_C00",
             "PC_379_396_38_C01",
             "PC_379_396_38_C02",
             "PC_379_396_38_C03"],             
                
    GENERIC_ADC_DAC_AMC = [
             "PC_379_396_13_C00",
             "PC_379_396_13_C01",
             "PC_379_396_13_C02",
             "PC_379_396_13_C03"],

    STRIPLINE_BPM_AMC = [
             "PC_379_396_03_C00",
             "PC_379_396_03_C01",
             "PC_379_396_03_C02",
             "PC_379_396_03_C03",
             "PC_379_396_03_C04",
             "test"],             
            
    MISC_AMC_CARD = [
             # Demo JESD ADC/DAC
             "PC_379_396_02_C00",
             # Loopback Tester 
             "PC_379_396_04_C00",
             "PC_379_396_04_C01",
             # MPS Digital Inputs
             "PC_379_396_06_C00",
             "PC_379_396_06_C01",
             # MPS SFP
             "PC_379_396_09_C00",
             "PC_379_396_09_C01",
             "PC_379_396_09_C02",
             # Timing Digital I/O
             "PC_379_396_14_C00",
             # LLRF Precision Downconvert/ADC Card
             "PC_379_396_16_C00",
             "PC_379_396_16_C01",
             "PC_379_396_16_C02",
             # LLRF Upconvert/ADC Card
             "PC_379_396_17_C00",
             "PC_379_396_17_C01",
             "PC_379_396_17_C02",             
             # Cryo-Sensor High Speed ADC/DAC Board
             "PC_379_396_23_C00"],
            
    MPS_TIMING_RTM = [
             "PC_379_396_07_C00",
             "PC_379_396_07_C01",
             "PC_379_396_07_C02",
             "PC_379_396_07_C03",
             "PC_379_396_07_C04"],              
            
    MISC_AMC_RTM = [
             # Digital Debug
             "PC_379_396_10_C00",
             "PC_379_396_10_C01",
             "PC_379_396_10_C02",   
             "PC_379_396_10_C03",   
             # RF Interlocks RTM
             "PC_379_396_19_C00",
             "PC_379_396_19_C01",
             # Loopback Tester 
             "PC_379_396_22_C00",
             "PC_379_396_22_C01",   
             # Fast Wire Scanner RTM
             "PC_379_396_26_C00"],             
            
    FLASH = ["PC_248_101_11_C00"],

    DTM   = ["PC_248_101_19_C00", 
             "PC_248_101_19_C01", 
             "PC_248_101_19_C02"],

    DPM   = ["PC_248_101_18_C00", 
             "PC_248_101_18_C01", 
             "PC_248_101_18_C02"],

    DUNE =  [
             "PC_264_810_95_C00",
             "PC_264_810_95_C01"],

    LSST = [
            # AUX Boards
            "LCA-15704-A",
            "LCA-15707-A",
            "LCA-15776-A",
	    "LCA-15776-B",
            "LCA-16361-A",
            "LCA-15796-A",
            "LCA-15800-A",
            # DAQ Boards
            "LCA-11566-A",
            "LCA-11566-B ",
            "LCA-11566-C",
            "LCA-11569-A",
            "LCA-11569-B",
            "LCA-11572-A",
            "LCA-11572-B",
            "LCA-11726-A",
            "LCA-14998-A",
            "LCA-15002-A",
            "LCA-15006-A",
            "LCA-15010-A",
            "PC_264_101_02_C00",
            # Ion Pump Boards
            "LCA-14959-A",
            "LCA-14959-B",
            "LCA-15111-A",
            "LCA-15111-B",
            # xREB Boards
            "LCA-10976-A",
            "LCA-10976-B",
            "LCA-10979-A",
            "LCA-11967-A",
            "LCA-13405-A",
            "LCA-13540-A",
            "LCA-13537-A",
            "LCA-15743-A",
            # xREB DAQ Intfc Boards
            "LCA-11545-A",
            "LCA-11545-B",
            "LCA-11545-C",
            "PC_259_100_31_C02",
            "LCA-10955-A",
            "LCA-10955-B",
            # xREB CCD Intfc Boards
            "LCA-11654-A",
            "LCA-11654-B",
            "LCA-11654-C",
            "LCA-11708-A",
            "LCA-11708-B",
            "LCA-11731-A",
            "LCA-11734-A",
            "LCA-11743-A",
            "LCA-11815-A",
            "LCA-13353-A",
            "LCA-13353-B",
            "LCA-13356-A",
            "LCA-13356-B",
            "LCA-13359-A",
            "LCA-13359-B",
            "LCA-13362-A",
            "LCA-13362-B",
            "LCA-13362-C",
            "LCA-13362-D",
            "LCA-13362-E",
            "LCA-13441-A",
            "LCA-13441-B",
            "LCA-13441-C",
            "LCA-13441-D",
            "LCA-14981-A",
            "LCA-14981-B",
            "LCA-14984-A",
            "LCA-14984-B",
            # REB Power Boards
            "LCA-10834-A",
            "LCA-10834-B",
            "LCA-15092-A",
            "LCA-15092-B",
            "LCA-15141-A",
            "LCA-15768-A",
            "LCA-15768-B",
            "LCA-15764-A",
            "LCA-15764-B",
            "LCA-15772-A",
            # Shutter Boards
            "LCA-15022-A",
            "LCA-15044-A",
            # Miscellaneous Boards
            "LCA-15049-A"],

    OTM   = ["LCA-11545", "LCA-11545-B"],

    SCI   = ["LCA-11726-A"],
    
    HSIO  = ["PC_256_100_83_C00",
             "PC_256_100_83_C01",
             "PC_256_100_83_C02",
             "PC_256_100_83_C03",
             "PC_256_100_83_C04"],

    HSIO_TTC = ["PC_256_100_89_C00","PC_256_100_89_C01"],

    POHANG_CAVITY_BPM = ["PC_144_163_01_C00"],

    uTCA_RTM_PI = ["PC_714_102_14_C00"],

    IPM_V2_BOX = ["PC_261_201_54_C00"],

    HSIO_RJ45_RTM = ["PC_256_100_88_C00"],
    
    ATLAS_CHESS2_CARRIER = ["PC_256_100_91_C00"],
    
    ATLAS_ATCA_LINK_AGG =
            ["PC_256_101_02_C00",
             "PC_256_101_02_C01"],    

    HEAVY_PHOTON_SEARCH = ['PC_249_901_07_C01']
    )

################################################################################
################################################################################
################################################################################

CLASSES = classToType.keys()
CLASSES.sort()

## @brief Map device page title to device class.
typeToClass = dict()
for _class, _pages in classToType.iteritems():
    for _p in _pages:
        typeToClass[_p] = _class
