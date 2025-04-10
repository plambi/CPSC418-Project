from seed_gen import *
from generate_numbers import *
from bbs import *
from lcg import *

import time


"""
    This file contains functions used to measure the runtime of various functions across this project.
"""

def average_seed_generation(seeds, algorithm):
    """
        Gets the average time required to generate a seed using urand. Uses a new BBS number for each generation.

        Args:
            seeds (int): The number of seeds to generate.
            algorithm (string): One of "urand", "rand", "time"
        
        Returns:
            float: The average time taken to generate each seed in ms

    """

    if(algorithm == "urand"):
        func = seed_bbs_urand
    elif(algorithm == "rand"):
        func = seed_bbs_rand
    elif(algorithm == "time"):
        func = seed_bbs_time
    else:
        print("Error! Invalid algorithm argument.")
        return None

    runtimes = []
    for i in range(seeds):
        bbs = BBS()
        m = bbs.get_m()

        start_time = time.time()
        __ = func(m)
        finish_time = time.time()
        runtimes.append(finish_time - start_time)

    total_time = 0.0
    for runtime in runtimes:
        total_time += runtime
    
    return round((total_time / seeds) * 1000, 4)

def get_bbs_seeds(number_of_seeds):
    """
        Generates and returns bbs seeds generated using urand.

        Returns:
            list: A list containing bbs seeds

    """

    seeds = []
    for _ in range(number_of_seeds):
        bbs = BBS()
        m = bbs.get_m()
        seed = seed_bbs_urand(m)
        seeds.append(seed)

    return seeds


def average_number_generation_bbs(numbers):
    """
        Gets the average time required to generate a 1 million bit string using BBS. Does not include seeding time.

        Args:
            numbers (int): The amount of numbers to generate.
        
        Returns:
            float: The average time taken to generate each number in seconds

    """
    runtimes = []
    for i in range(numbers):
        bbs = BBS()
        m = bbs.get_m()
        seed = seed_bbs_urand(m)
        bbs.seed(seed)
        
        start_time = time.time()
        _ = bbs.generate_nist_output(1_000_000)
        finish_time = time.time()
        runtimes.append(finish_time - start_time)
    
    total_time = 0.0
    for runtime in runtimes:
        total_time += runtime
    
    return round((total_time / numbers) * 1000, 4)


def average_number_generation_lcg(seeds, algorithm):
    """
        Gets the average time required to generate a 1 million bit string. Does not include seeding.

        Args:
            seeds (list): A list containing valid bbs seeds.
            algorithm (string): One of "lcg_whole", "lcg_lsb"
        
        Returns:
            float: The average time taken to generate each number in seconds

    """

    lcg = LCG()
    runtimes = []

    if(algorithm == "lcg_whole"):
        for i in range(len(seeds)):
            lcg.seed(seeds[i])
            start_time = time.time()
            _ = lcg.generate_bits(1_000_000)
            finish_time = time.time()
            runtimes.append(finish_time - start_time)

    elif(algorithm == "lcg_lsb"):
        for i in range(len(seeds)):
            lcg.seed(seeds[i])
            start_time = time.time()
            _ = lcg.generate_bits_lsb(1_000_000)
            finish_time = time.time()
            runtimes.append(finish_time - start_time)
    else:
        print("Error! Invalid algorithm argument.")
        return None
    
    total_time = 0.0
    for runtime in runtimes:
        total_time += runtime
    
    return round((total_time / len(seeds)) * 1000, 4)

def average_bbs_init(bbs_count):
    """
        Gets the average time required to initialize bbs.

        Args:
            seeds (int): The number of seeds to generate.
            algorithm (string): One of "urand", "rand", "time"
        
        Returns:
            float: The average time taken to generate each seed in ms

    """

    runtimes = []
    for _ in range(bbs_count):
        start_time = time.time()
        bbs = BBS()
        finish_time = time.time()
        runtimes.append(finish_time - start_time)
    
    total_time = 0.0
    for runtime in runtimes:
        total_time += runtime
    
    return round((total_time / bbs_count) * 1000, 4)


if __name__ == "__main__":
    # print(average_seed_generation(50, "urand"))   # 0.0136ms
    # print(average_seed_generation(50, "rand"))    # 0.0115ms
    # print(average_seed_generation(50, "time"))    # 0.0059ms

    # These were generated with get_bbs_seeds, there are 100 of them
    valid_bbs_seeds = [126604568049877858247161895462253253149, 224037881215807385832087415834057236932, 319576693964713282021043027711335242337, 22525474533278631726620768077264968481, 40241145357284776767962903632776527710, 22320661632092191013951163824574262893, 65524103303646984601814727641652856518, 62743896430416809422327984656677532561, 102784791376209782121350293370914041096, 733538689091476527231232784581588986, 204776595722583424684005069016759222786, 298613338500529261040086665441593790602, 85316278747213484469530880865835241532, 131479600911269053126714717396504430204, 171389526123178258472815443359745278029, 276034822358915844030654605477810750583, 76520590617286793768063516582103893737, 175879721312096495231689147771165064234, 61988567234155954545938430550832032207, 109011501306407541519639811277724426008, 201586466964018942894271656592117138117, 311756970636118972068912009257088237072, 139077785789536259492141979922140703004, 286408827659611073635420785810971324674, 246170104114553152175628603328475088577, 141791685525142153521733388652785774418, 10670118007589920096539264117152935361, 302779582436612594233068232100200766690, 139027308797593168018066908134941275234, 65175252250171060025449002169450845456, 206260960970248508932088855366615376828, 87246698288048863928424955529017671205, 47936395212102517351831251066404546082, 34390346747625589308005663834536957009, 88311836909299542606012073273282476330, 78581791873758092857115612524760734507, 4342181268375487035404826932482440044, 227538529035481902604607413259793433166, 214432421570669747954446964152848470254, 116662783102341385381827557425950541660, 117452192425804327918485937096745119757, 100544532316742376400780504608899667194, 312755952464244319942833568321257497779, 338131859054962151311150682368081787792, 270494935202794678491340332042344051576, 199078585483434049632915960325384634006, 79594450083832530694451027757403447224, 205804502171157380726920189158710934282, 33077011062336362865556451214208030388, 219715291721790317065843910738933161200, 17089863202028868939744120555181948710, 132930557580180389716462436174014446316, 91832683159238840646701090783200037372, 96274376475858491486095518031897207484, 301733067189483474253640982809448879187, 306831370840477458091370046412632958610, 245922682127856610959883976060908566957, 246527895573486218181483959370774555096, 215360408310102054878602069385153759955, 307947928492183592971459576542002884315, 270607109623658864947668921505696502109, 307753193368301342296542856214069925389, 48963776928624270016316939387712501078, 297560265604972616642117424156793682379, 55800409516522832329477130361394694867, 268950914531060859652250492957471032734, 15260968685267038371421885766696412355, 90562637596548844066037679152157447140, 142819340231923539452857646021718512185, 276297552771777455171311045232470619589, 197563807286464383417262407811639999493, 285529885643782046131377186854629246246, 132720714223863336489038386516130862999, 290681956128461014482398955623057696656, 244529987209422916127997229244997804950, 47366378195626136713129646308481064434, 332358621869139835568484212634032965369, 268854244459844569007680972035366978808, 329682274386953725358716477864533140600, 197714953949449216539786348731672605018, 309956397668508429627527758016159304192, 98357890638924814423856749151385263881, 331899316636892206792468951127517519369, 217715450360739692820194790560049077268, 57705262731374894294760372988187930380, 312062074291809440187074041781186243630, 81952292989519497841831039370107299221, 83949753258909481218189083349957861107, 167585714218141550913719622943143657505, 200745739255989398273388079818688375692, 113705533910986428662503384169908323177, 56434827538390392733081425516064571936, 69609671181580021808952069278228374771, 182469499542660266780669235982350087598, 110169294808762168062602474118532809213, 67925949203240126382514152126636844573, 240335659610720079549301209593132235840, 193549214102936762535822475362691289949, 74372951435473218387511606832235731024, 217718167082884549546759077282772825159]

    # print(average_number_generation_lcg(valid_bbs_seeds, "lcg_whole"))    # 23.5043ms
    # print(average_number_generation_lcg(valid_bbs_seeds, "lcg_lsb"))      # 481.081ms

    # print(average_bbs_init(100))                  # 2641.8598ms
    # print(average_number_generation_bbs(100))     # 8848.161ms