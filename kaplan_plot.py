import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from astropy.table import Table
import matplotlib.transforms as transforms
from astropy.time import Time
from matplotlib.lines import Line2D


months_jd = Time(np.array(["2019-03-01T00:00:00","2019-04-01T00:00:00", "2019-05-01T00:00:00","2019-06-01T00:00:00","2019-07-01T00:00:00","2019-08-01T00:00:00","2019-09-01T00:00:00","2019-10-01T00:00:00","2019-11-01T00:00:00","2019-12-01T00:00:00","2020-01-01T00:00:00","2020-02-01T00:00:00","2020-03-01T00:00:00","2020-04-01T00:00:00"]), format="isot",scale="utc").jd

months_jd_labels = np.array(["2019-03","2019-04", "2019-05","2019-06","2019-07","2019-08","2019-09","2019-10","2019-11","2019-12","2020-01","2020-02","2020-03","2020-04"])

data_file = "superevents_data.txt"

data_tab = Table.read(data_file,format="ascii")

superevent_ids = data_tab["id"]
superevent_times = data_tab["time"]
superevent_FAR = data_tab["FAR"]
superevent_BNS_prob = data_tab["BNS"]
superevent_NSBH_prob = data_tab["NSBH"]
superevent_BBH_prob = data_tab["BBH"]
superevent_MassGap_prob = data_tab["MassGap"]
superevent_Terrestrial_prob = data_tab["Terrestrial"]
superevent_dist = data_tab["dist"]
superevent_90_per_area = data_tab["90% area"]

logscaled_superevent_FAR = 1 - ((np.log10(superevent_FAR) - np.min(np.log10(superevent_FAR)))/(np.max(np.log10(superevent_FAR)) - np.min(np.log10(superevent_FAR))))

for i in range(len(logscaled_superevent_FAR)):
    if (logscaled_superevent_FAR[i] < 0.1):
        logscaled_superevent_FAR[i] = 0.1


def draw_wedge(ax, drawing_origin, radius, prob1, prob2, prob3, prob4, prob5, col_alpha):

    box_height = 1
    box_width = 1
    
    origin = np.array([0,0])
    trans = (fig.dpi_scale_trans + transforms.ScaledTranslation(drawing_origin[0],drawing_origin[1], ax.transData))

    ang1 = prob1*360
    ang2 = prob2*360
    ang3 = prob3*360
    ang4 = prob4*360
    ang5 = prob5*360

    if (prob1 != 0):
        wedge1 = mpatches.Wedge(origin, radius, 0, ang1, facecolor="y", edgecolor=None, transform=trans, alpha=col_alpha)
        ax.add_patch(wedge1)
    if (prob2 != 0):
        wedge2 = mpatches.Wedge(origin, radius,ang1,ang1+ang2, facecolor="b", edgecolor=None, transform=trans, alpha=col_alpha)
        ax.add_patch(wedge2)
    if (prob3 != 0):
        wedge3 = mpatches.Wedge(origin, radius,ang1+ang2,ang1+ang2+ang3, facecolor="g", edgecolor=None, transform=trans, alpha=col_alpha)
        ax.add_patch(wedge3)
    if (prob4 != 0):    
        wedge4 = mpatches.Wedge(origin, radius,ang1+ang2+ang3,ang1+ang2+ang3+ang4, facecolor="purple", edgecolor=None, transform=trans, alpha=col_alpha)
        ax.add_patch(wedge4)
    if (prob5 != 0):
        wedge5 = mpatches.Wedge(origin, radius,ang1+ang2+ang3+ang4,ang1+ang2+ang3+ang4+ang5, facecolor="k", edgecolor=None, transform=trans, alpha=col_alpha)
        ax.add_patch(wedge5)

    return 0

def get_radius(area):
    return np.sqrt(area/np.pi)

fig, ax = plt.subplots(figsize=(8,16/3))

ax.set_ylim([10, 6000])
ax.set_xlim(min(months_jd),max(months_jd))
ax.set_xticks(months_jd)
ax.set_xticklabels(months_jd_labels,rotation=30,ha="right")
ax.set_yscale('log')
ax.set_ylabel("Luminosity Distance (Mpc)")
radius_scale = 0.2*6

size_legend_x = np.sum(Time(np.array(["2019-04-01T00:00:00", "2019-05-01T00:00:00"]), format="isot",scale="utc").jd)/2.0

size_legend_y1 = 60
c1_trans = (fig.dpi_scale_trans + transforms.ScaledTranslation(size_legend_x,size_legend_y1, ax.transData))
circle1 = mpatches.Circle(np.array([0,0]), radius_scale/get_radius(100),facecolor="b",edgecolor=None, transform=c1_trans, alpha=0.5)
ax.add_patch(circle1)
ax.text(size_legend_x+20,size_legend_y1,r"100 deg$^{{2}}$", verticalalignment="center",horizontalalignment="left")

size_legend_y2 = 40
c2_trans = (fig.dpi_scale_trans + transforms.ScaledTranslation(size_legend_x,size_legend_y2, ax.transData))
circle2 = mpatches.Circle(np.array([0,0]), radius_scale/get_radius(500),facecolor="b",edgecolor=None, transform=c2_trans, alpha=0.5)
ax.add_patch(circle2)
ax.text(size_legend_x+20,size_legend_y2,r"500 deg$^{{2}}$", verticalalignment="center",horizontalalignment="left")

size_legend_y3 = 30
c3_trans = (fig.dpi_scale_trans + transforms.ScaledTranslation(size_legend_x,size_legend_y3, ax.transData))
circle3 = mpatches.Circle(np.array([0,0]), radius_scale/get_radius(1000),facecolor="b",edgecolor=None, transform=c3_trans, alpha=0.5)
ax.add_patch(circle3)
ax.text(size_legend_x+20,size_legend_y3,r"1000 deg$^{{2}}$", verticalalignment="center",horizontalalignment="left")

size_legend_y4 = 23
c4_trans = (fig.dpi_scale_trans + transforms.ScaledTranslation(size_legend_x,size_legend_y4, ax.transData))
circle4 = mpatches.Circle(np.array([0,0]), radius_scale/get_radius(5000),facecolor="b",edgecolor=None, transform=c4_trans, alpha=0.5)
ax.add_patch(circle4)
ax.text(size_legend_x+20,size_legend_y4,r"5000 deg$^{{2}}$", verticalalignment="center",horizontalalignment="left")

size_legend_y5 = 18
c5_trans = (fig.dpi_scale_trans + transforms.ScaledTranslation(size_legend_x,size_legend_y5, ax.transData))
circle5 = mpatches.Circle(np.array([0,0]), radius_scale/get_radius(10000),facecolor="b",edgecolor=None, transform=c5_trans, alpha=0.5)
ax.add_patch(circle5)
ax.text(size_legend_x+20,size_legend_y5,r"10000 deg$^{{2}}$", verticalalignment="center",horizontalalignment="left")

for i in range(len(superevent_ids)):
    
    do = np.array([superevent_times[i],superevent_dist[i]])
    r = radius_scale/get_radius(superevent_90_per_area[i])

    draw_wedge(ax, do, r, superevent_BNS_prob[i], superevent_NSBH_prob[i], superevent_BBH_prob[i], superevent_MassGap_prob[i], superevent_Terrestrial_prob[i], logscaled_superevent_FAR[i])


###### GW170817 #######

gw170817_2_time = Time("2019-08-17T00:00:00", format="isot", scale="utc").jd
gw170817_dist = 40

draw_wedge(ax,np.array([gw170817_2_time,gw170817_dist]), radius_scale/get_radius(40), 1.0, 0.0, 0.0, 0.0, 0.0, 1.0)
ax.text(Time("2019-09-15T00:00:00", format="isot", scale="utc").jd,40,"GW170817+2yr", va="center")
legend_elements = [Line2D([],[], marker="o", color="y",linestyle="None", label="BNS"), Line2D([0],[0], marker="o", color="b",linestyle="None", label="NSBH"), Line2D([0],[0], marker="o", color="g",linestyle="None", label="BBH"), Line2D([0],[0], marker="o", color="purple",linestyle="None", label="MassGap"), Line2D([0],[0], marker="o", color="k",linestyle="None", label="Terrestrial")]

ax.legend(handles=legend_elements, loc="lower right")

plt.savefig("Kaplan_plot_Feb_2020.pdf")
