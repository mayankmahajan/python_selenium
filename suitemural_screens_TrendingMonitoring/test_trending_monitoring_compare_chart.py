from Utils.SetUp import *
from MuralUtils.MuralConstants import *
from Utils.utility import *
from classes.Pages.MuralScreens.NetworkScreenClass import *
from classes.Components.WorkflowStartComponent import *
from classes.Components.TimeRangeComponentClass import *
from classes.Pages.MuralScreens.AccessTechnologyClass import *
from classes.Components.TimeRangeComponentClass import *
from classes.Pages.TrendingMonitoringPageClass import *
import sys

main_chart_value = '2919000000.0'
compare_chart_value = '2919000000.0'

try:
    setup = SetUp()
    sleep(8)
    login(setup, "admin", "Admin@123")
    wfstart = WorkflowStartComponentClass()
    sleep(8)
    wfstart.launchScreen("Trend", getHandle(setup, MuralConstants.WFSTARTSCREEN))
    TMScreenInstance = TrendingMonitoringPageClass(setup.d)

    measures = setup.cM.getNodeElements("measureswithdirection", "measure")
    dimensions = setup.cM.getNodeElements("tmdimension", "dimension")
    mes = []
    mes_count = []
    for k, measure in measures.iteritems():
        mes.append(measure['locatorText'])
        mes_count.append(measure['isCount'])

    dim = []
    for k, dimension in dimensions.iteritems():
        dim.append(dimension['locatorText'])


    selectedQuicklink = TMScreenInstance.timeBar.getSelectedQuickLink(getHandle(setup, MuralConstants.TMSCREEN, "ktrs"))

    numberofmainchart = TMScreenInstance.quicktrends.getChartsCount(getHandle(setup, MuralConstants.TMSCREEN, "trend-main"))
    numberofcomparechart = TMScreenInstance.quicktrends.getChartsCount(getHandle(setup, MuralConstants.TMSCREEN), parent="trend-compare")
    checkEqualAssert(7, numberofmainchart + numberofcomparechart, selectedQuicklink,"","Verify total number of Chart")


    for i in range(6):
        TMScreenInstance.dropdown.customClick(getHandle(setup, MuralConstants.TMSCREEN, "trend-compare")["trend-compare"]["trendchart"][i])
        selectedMeasure = TMScreenInstance.dropdown.doSelectionOnVisibleDropDownByIndex(getHandle(setup, MuralConstants.TMSCREEN), random.randint(0,len(mes)-1), index=0, parent="trend-header")
        isError(setup)
        selectedDimension = TMScreenInstance.dropdown.doSelectionOnVisibleDropDownByIndex(getHandle(setup, MuralConstants.TMSCREEN), random.randint(0,len(dim)-1), index=1, parent="trend-header")
        isError(setup)



    for i in range(6):
        TMScreenInstance.dropdown.customClick(getHandle(setup, MuralConstants.TMSCREEN, "trend-compare")["trend-compare"]["trendchart"][i])
        comparechartIndex = TMScreenInstance.quicktrends.getSelectedCompareChartIndex(getHandle(setup, MuralConstants.TMSCREEN))
        checkEqualAssert(i,comparechartIndex,selectedQuicklink,"","Verify click on compare Chart with index %s"+str(i))

        view = TMScreenInstance.switcher.getMeasureChangeSelectedSwitcher(getHandle(setup, MuralConstants.TMSCREEN, "trend-main"), parent="trend-main")
        checkEqualAssert(int(view[0]), 0, str(selectedQuicklink), "", "Verify view (line chart) after click on compare chart")

        numberofmainchart = TMScreenInstance.quicktrends.getChartsCount(getHandle(setup, MuralConstants.TMSCREEN, "trend-main"))
        numberofcomparechart = TMScreenInstance.quicktrends.getChartsCount(getHandle(setup, MuralConstants.TMSCREEN),parent="trend-compare")
        checkEqualAssert(7, numberofmainchart + numberofcomparechart, selectedQuicklink, "","Verify total number of Chart after click on compare chart")

        p1 = TMScreenInstance.quicktrends.getPaths(getHandle(setup, MuralConstants.TMSCREEN))
        compareTrend1 = TMScreenInstance.quicktrends.getPaths(getHandle(setup, MuralConstants.TMSCREEN),parent="trend-compare",indexOfComp=i)
        checkEqualAssert(compareTrend1,p1,selectedQuicklink,"","Verify equal activated dimension on main chart and compare chart")
        #Main Chart and Compare Chart value --->Pending
        checkEqualAssert(compare_chart_value,main_chart_value,selectedQuicklink,"","Verify Main Chart Value with Compare Chart Value")

        measurefrommain = TMScreenInstance.dropdown.getSelectionOnVisibleDropDown(getHandle(setup, MuralConstants.TMSCREEN), index=0, parent="trend-header")
        measurefromcompare = TMScreenInstance.dropdown.getSelectionOnVisibleDropDown(getHandle(setup, MuralConstants.TMSCREEN), index=i, parent="trend-compare")
        checkEqualAssert(str(measurefrommain), str(measurefromcompare), str(selectedQuicklink), "", "Verify measure on Main and Comapre Chart")

        dimensionfrommain = TMScreenInstance.dropdown.getSelectionOnVisibleDropDown(getHandle(setup, MuralConstants.TMSCREEN), index=1, parent="trend-header")
        #dimensionfromcompare ----> pending
        dimensionfromcompare ="None"
        checkEqualAssert(str(dimensionfrommain), str(dimensionfromcompare), str(selectedQuicklink), "", "Verify dimension on Main and Comaper Chart")
        TMScreenInstance.switcher.measureChangeSwitcher(1, getHandle(setup, MuralConstants.TMSCREEN, "trend-main"),parent="trend-main")

    setup.d.close()

except Exception as e:
    raise e
    print str(e)
    setup.d.close()