import requests
from ligo.gracedb.rest import GraceDb
import ast
import pandas as pd
from PIL import Image
import pytesseract
from io import BytesIO
from astropy.time import Time
from astropy.table import Table
import numpy as np

#client = GraceDb()
#
#superevent_iterator = client.superevents('is_public: True')
#superevent_list = [superevent for superevent in superevent_iterator]
#
#for i in range(len(superevent_list)):
#    my_evt_id = superevent_list[i]['superevent_id']
#    my_evt_files_url = superevent_list[i]['links']['files']
#    page = requests.get(my_evt_files_url)
#    data = page.text
#
#    if ("Retraction.xml") in data:
#        superevent_list[i] = "Retracted"
#
#remove_indices = [i for i,x in enumerate(superevent_list) if x=="Retracted"]
#
#for index in sorted(remove_indices, reverse=True):
#    del superevent_list[index]
#
#superevent_file = open('sel_superevents.txt','w')
#
#print("Found %d superevents that match search criteria!"%len(superevent_list))
#
#for superevent in superevent_list:
#    superevent_file.write("%s\n"%superevent)

superevent_file = open('sel_superevents.txt','r')

superevent_list = []
for line in superevent_file:
    superevent_list.append(ast.literal_eval(line[:-1]))

n = len(superevent_list)

superevent_ids = []
superevent_times = np.zeros(n)
superevent_FAR = np.zeros(n)
superevent_BNS_prob = np.zeros(n)
superevent_NSBH_prob = np.zeros(n)
superevent_BBH_prob = np.zeros(n)
superevent_Terrestrial_prob = np.zeros(n)
superevent_MassGap_prob = np.zeros(n)
superevent_dist = np.zeros(n)
superevent_50_per_area = np.zeros(n)
superevent_90_per_area = np.zeros(n)

for i in range(n):
    my_evt = superevent_list[i]
    my_evt_files_url = my_evt['links']['files']
    
    my_evt_id = my_evt['superevent_id'] #############
    superevent_FAR[i] = my_evt['far'] #############
    superevent_ids.append(my_evt_id)
    print(my_evt_id)
    try :
    
        my_evt_time = Time(my_evt['created'][:-4],format="iso",scale="utc").jd #############
        superevent_times[i] = my_evt_time

        probs_text = requests.get(my_evt_files_url+'p_astro.json').text
        probs_dict = ast.literal_eval(probs_text)
    
        BNS_prob = probs_dict["BNS"] #############
        NSBH_prob = probs_dict["NSBH"] #############
        BBH_prob = probs_dict["BBH"] #############
        Terrestrial_prob = probs_dict["Terrestrial"] #############
        Mass_gap_prob = probs_dict["MassGap"] #############
        superevent_BNS_prob[i] = BNS_prob
        superevent_NSBH_prob[i] = NSBH_prob
        superevent_BBH_prob[i] = BBH_prob
        superevent_Terrestrial_prob[i] = Terrestrial_prob
        superevent_MassGap_prob[i] = Mass_gap_prob

        my_evt_bayestar_url = my_evt_files_url+'bayestar.html'
        tables = pd.read_html(my_evt_bayestar_url)
        my_tab = tables[0]
        dist_row = my_tab.loc[my_tab["Keyword"]=="DISTMEAN"]
        my_evt_dist = dist_row.iloc[0]["Value"] #############
        superevent_dist[i] = my_evt_dist
    
        my_evt_bayestar_png = my_evt_files_url+'bayestar.png'
        img_r = requests.get(my_evt_bayestar_png)
        bayestar_png_str = pytesseract.image_to_string(Image.open(BytesIO(img_r.content))).split("\n")
        per_50_area_str = ""
        per_90_area_str = ""
        for string in bayestar_png_str:
            if ("50% area") in string:
                per_50_area_str = string
            if ("90% area") in string:
                per_90_area_str = string
            
        #print(per_50_area_str.split(" "))
        print(per_90_area_str.split(" "))
        a = np.array(per_50_area_str.split(" "))
        b = np.array(per_90_area_str.split(" "))
        id_50 = np.where( a == '50%')[0]
        id_90 = np.where( b == '90%')[0]
        #per_50_area = float(a[id_50+2]) #############
        per_90_area = float(b[id_90+2]) #############
        #superevent_50_per_area[i] = per_50_area
        superevent_90_per_area[i] = per_90_area
        print("====================================================================")

    except:
        print("Something wrong with this trigger. Go back and check!")
        print("====================================================================")

superevent_tab = Table([superevent_ids,superevent_times,superevent_dist,superevent_FAR, superevent_BNS_prob,superevent_NSBH_prob,superevent_BBH_prob,superevent_Terrestrial_prob,superevent_MassGap_prob,superevent_50_per_area,superevent_90_per_area], names=["id","time","dist","FAR","BNS","NSBH","BBH","Terrestrial","MassGap","50% area","90% area"])
superevent_tab.write("superevents_data.txt",format="ascii",overwrite=True)

