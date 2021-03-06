from Utils.utility import *
from Utils.Constants import *
from Utils.SetUp import *
from classes.Pages.SitePageClass import *
from classes.Components.SearchComponentClass import *
from classes.Pages.QuickTrendsPageClass import *


# Getting Setup Details and Launching the application
setup = SetUp()
# Logging into the appliction
login(setup, "admin", "Admin@123")

exploreScreenInstance = ExplorePageClass(setup.d)
exploreHandle = getHandle(setup,"explore_Screen")
exploreScreenInstance.exploreList.launchScreen(exploreHandle,"exploreList","site_Screen")
# Get the Instance of the screen
screenInstance = SitePageClass(setup.d)

# Get the handles of the screen
siteScreenHandle = getHandle(setup,"site_Screen")

data = screenInstance.btv.getData(siteScreenHandle)
#btvdata = getBTVData(setup.d,setup.dH)
#print data
# print data['BTVCOLUMN1']
# print data['BTVCOLUMN1'][1]
# print data['BTVCOLUMN1'][2]
# print data['BTVCOLUMN1'][3]
# length = len(data['BTVCOLUMN1'])
# index = 2
sitesname = ""
for index in range(2,len(data['BTVCOLUMN1'])):
    print data['BTVCOLUMN1'][index]
    sitesname = sitesname + data['BTVCOLUMN1'][index]

print sitesname
# print a

screenInstance.cm.activateContextMenuOptions1(siteScreenHandle)

screenInstance.cm.launchTrends(siteScreenHandle)

qtScreenInstance = QuickTrendsPageClass(setup.d)
qtScreenHandle = getHandle(setup,"qt_Screen")

list = qtScreenInstance.quicktrends.getLegendList(qtScreenHandle)
legends = ""
for i in range(len(list)):
    legends = legends +list[i]

checkEqualAssert(sitesname,legends,"","","DATA IS VALIDATE FOR ALL THE LEGENDS IN THE QUICK TRENDS")
#print btvdata
xaxis  = qtScreenInstance.quicktrends.getXAxis(qtScreenHandle)
yaxis  = qtScreenInstance.quicktrends.getYAxis(qtScreenHandle)

t = qtScreenInstance.quicktrends.moveTotick(setup.dH,qtScreenHandle)



setup.d.close()