from Utils.utility import *
from MRXConstants import *
from classes.Components.TimeRangeComponentClass import *
from selenium.webdriver import ActionChains
from MRXUtils import UDHelper
import json

def getNoDataMsg(setup,screen,parent='cb_no_data_msg',child='msgOnChart'):
    logger.info("Method Called : getNoDataMsg")
    h=getHandle(setup,screen,parent)
    if len(h[parent][child])>0:
        return str(h[parent][child][0].text)
    else:
        return "Text not found for No Data"


def getHeader(setup,screen,parent='cb_chart_header',child='text'):
    logger.info("Method Called : getHeader")
    h=getHandle(setup,screen,parent)
    if len(h[parent][child])>0:
        return str(h[parent][child][0].text)
    else:
        return "Header Text Not Found"


def getAxisPoint(h,parent='trend-main',child='xaxis'):
    point=[]
    if len(h[parent][child])>0:
        for ele in h[parent][child][0].find_elements_by_class_name('tick'):
            point.append(str(ele.text).strip())
    return point

def map_YAxisWithColorList(yAxisPointList,color_List):
    logger.info("Method Called : map_YAxisWithColorList")
    barColorDict={}
    if len(yAxisPointList) == len(color_List):
        for index in range(len(yAxisPointList)):
            barColorDict[yAxisPointList[index]] = color_List[index]

        logger.info("Bar Color List With Y axis Point =%s", str(barColorDict))
    else:
        logger.error("Mismatch in Color List and Y axis point : check manually")

    return barColorDict


def validateSortingInTable(cbScreenInstance,data,selectedQuicklink, selectedMeasure):
    index = cbScreenInstance.table.getIndexForValueInArray(data['header'], selectedMeasure)
    selectedMeasure_value_list = [element[index] for element in data['rows']]

    l = []
    for i in range(len(selectedMeasure_value_list)):
        if str(selectedMeasure_value_list[i]).strip()!='':
            l.append(UnitSystem().getRawValueFromUI(selectedMeasure_value_list[i]))

    sorting_Flag = verifySortingWithSomeDifference(l)
    checkEqualAssert(True,sorting_Flag,selectedQuicklink,selectedMeasure,message='Verify that table data order must be highest to lowest wrt selected measure :: Value_List ='+str(selectedMeasure_value_list),testcase_id='MKR-3561')
    return

def validateColorSequence(barColorDict,data,coloumIndexOfColor=0):
    colorSequenceFromTable=[]
    colorSequenceFlag = True

    if data['rows']!=Constants.NODATA:
        for row in data['rows']:
            colorSequenceFromTable.append(row[coloumIndexOfColor])

        logger.info('Got color list from table = %s',str(colorSequenceFromTable))

        if barColorDict!={} and colorSequenceFromTable!=[]:
            for key in barColorDict.keys():
                colorIndexList=[]
                for color in barColorDict[key]:
                    try:
                        colorIndexList.append(colorSequenceFromTable.index(color))
                    except Exception as e:
                        logger.error("Color on bar not found in Table : Bar color = %s Color List From table = %s",str(color),str(colorSequenceFromTable))
                        return False

                if colorIndexList!=sorted(colorIndexList):
                    colorSequenceFlag=False
                    break
    else:
        logger.error("Table Not Found hence can't varify color sequence")

    return colorSequenceFlag


def validateColorOnTooltipWithBar(toolTipData,barColorDict):
    logger.info("Method called : validateColorOnTooltipWithBar")
    try:
        checkEqualAssert(len(barColorDict.keys()), len(toolTipData.keys()),message="Verify hover on each bar",testcase_id="MKR-3564")
        if len(barColorDict.keys())!=0:
            for key in barColorDict.keys():
                logger.info("Going to validate tooltip for %s",str(key))
                toolTipColor=[]
                percentageOnTooltip=[]
                checkEqualAssert(len(barColorDict[key.strip()]),len(toolTipData[key.strip()]),message="Verify equal number of color on bar and tooltip")
                for row in toolTipData[key.strip()]:
                    toolTipColor.append(row[0])
                    percentageOnTooltip.append(float(row[1].split('(')[1].split('%')[0].strip()))

                checkEqualAssert(barColorDict[key.strip()],toolTipColor,message="Verify Color on tooltip with bar for "+str(key))
                if toolTipColor!=[]:
                    checkEqualAssert(100.0,round(sum(percentageOnTooltip),2),message="Verify total percantage on toolTip for "+str(key))
        else:
            logger.info("Bar not found : check manually")

    except Exception as e:
        logger.error("Got Exception during validating tootTip with bar =%s",str(e))


def expandMoreOnCB(setup,screenInstance,screenname,parent='expand_more',child='load_more',barParent='trend-main',checkLoadMore=True):
    if checkLoadMore:
        logger.info("Method called : expandMoreOnCB")
        numberOfBarBeforeClick,barHandles=screenInstance.getAllBar_DCT(getHandle(setup,screenname,barParent))
        h=getHandle(setup,screenname,parent)
        if len(h[parent][child])!=0:
            try:
                h[parent][child][0].click()
                sleep(MRXConstants.SleepForComparativeScreen)
                numberOfBarAfterClick, barHandles = screenInstance.getAllBar_DCT(getHandle(setup, screenname, barParent))
                checkEqualAssert(True, numberOfBarAfterClick - numberOfBarBeforeClick <= 10,message='Verify the functionality of the load more link', testcase_id='MKR-3574')
                if numberOfBarAfterClick-numberOfBarBeforeClick==10:
                    return False
                elif numberOfBarAfterClick-numberOfBarBeforeClick<10:
                    checkEqualAssert(0,len(getHandle(setup,screenname,parent)[parent][child]),message="After click on load more if loaded value less then 10, load more link must disappear")
                    return True

            except ElementNotVisibleException or ElementNotSelectableException or Exception as e:
                return e
        else:
            return True
    else:
        return False

def setQuickLink_Compare_Measure_BreakDown(setup,cbScreenInstance,i='0'):

    quicklink = setup.cM.getNodeElements("cbScreenFilters", 'quicklink')
    CompareDim = setup.cM.getNodeElements("cbScreenFilters", 'compareDim')[str(i)]['locatorText']
    CompareMes = setup.cM.getNodeElements("cbScreenFilters", 'measure')[str(i)]['locatorText']
    BrokenDown = setup.cM.getNodeElements("cbScreenFilters", 'breakDown')[str(i)]['locatorText']

    logger.info("Going to Select Compare =%s, By =%s, Brokendown  =%s",str(CompareDim),str(CompareMes),str(BrokenDown))

    if quicklink[str(i)]['locatorText'] == 'CustomClick':
        selectedQuicklink=quicklink[str(i)]['locatorText']
        calHandler = getHandle(setup, MRXConstants.COMPARATIVESCREEN, "ktrs")
        logger.info("Launching Calendar from UDP Popup")
        calHandler['ktrs']['datepicker'][0].click()
        logger.info("Calendar picker is clicked")

        ################################### For test Calender Scenario #################################################

        if i=='testCalender':
            [year, month, day, hour, min] = str(quicklink[str(i)]['startTime']).split(' ')
            setCalendar(year, month, day, hour, min, cbScreenInstance, setup, page=Constants.CALENDERPOPUP,parent="leftcalendar")

            [et_year, et_month, et_day, et_hour, et_min] = str(quicklink[str(i)]['endTime']).split(' ')
            setCalendar(et_year, et_month, et_day, et_hour, et_min, cbScreenInstance, setup, Constants.CALENDERPOPUP,"rightcalendar")

            valueFromCalender1 = str(getHandle(setup, Constants.CALENDERPOPUP, 'allspans')['allspans']['span'][0].text).strip()

            stepoch,etepoch=parseTimeRange1(valueFromCalender1,timezone=MRXConstants.TIMEZONEOFFSET)
            try:
                if etepoch-stepoch <=0:
                    UDHelper.button_Status(False,"When Start Time > End Time ==> Selected Time Range ="+valueFromCalender1, cbScreenInstance, setup,Constants.CALENDERPOPUP, "Apply",testcase_id='')
                else:
                    checkEqualAssert(True,etepoch-stepoch>=0,"Not allow to choose StartTime > EndTime",testcase_id='MKR-3188')
            except:
                logger.info("Skipping TestCase =")

            monthListFormLeftCalender=getAvailableMonthList(setup,parent='leftcalendar')
            checkEqualAssert(MRXConstants.MONTHLIST,monthListFormLeftCalender,message='Verify that all the months should be there in the custom calendar (Left Calender)',testcase_id='')

            monthListFormRightCalender = getAvailableMonthList(setup, parent='rightcalendar')
            checkEqualAssert(MRXConstants.MONTHLIST, monthListFormRightCalender,message='Verify that all the months should be there in the custom calendar (Right Calender)',testcase_id='')

            cbScreenInstance.clickButton("Cancel", getHandle(setup, Constants.CALENDERPOPUP, Constants.ALLBUTTONS))

            return
        ################################################################################################################


        [year, month, day, hour, min] = str(quicklink[str(i)]['startTime']).split(' ')
        setCalendar(year, month, day, hour, min, cbScreenInstance, setup, page=Constants.CALENDERPOPUP,parent="leftcalendar")

        [et_year, et_month, et_day, et_hour, et_min] = str(quicklink[str(i)]['endTime']).split(' ')
        setCalendar(et_year, et_month, et_day, et_hour, et_min, cbScreenInstance, setup,Constants.CALENDERPOPUP, "rightcalendar")

        valueFromCalender=str(getHandle(setup,Constants.CALENDERPOPUP,'allspans')['allspans']['span'][0].text).strip()
        # Closing Calendar Pop Up
        cbScreenInstance.clickButton("Apply",getHandle(setup, Constants.CALENDERPOPUP, Constants.ALLBUTTONS))
        logger.info("Calendar Selection done at Filter Popup = %s ", valueFromCalender)
        t1 = cbScreenInstance.timeBar.getLabel(getHandle(setup, MRXConstants.UDSCREEN, "ktrs"))
        checkEqualAssert(valueFromCalender, t1, selectedQuicklink,message="verify quicklink label")

    else:
        cbScreenInstance.timeBar.setQuickLink(quicklink[str(i)]['locatorText'], getHandle(setup, MRXConstants.COMPARATIVESCREEN, "ktrs"))
        isError(setup)
        selectedQuicklink = cbScreenInstance.timeBar.getSelectedQuickLink(getHandle(setup, MRXConstants.COMPARATIVESCREEN, "ktrs"))
        t = TimeRangeComponentClass().get_Label(str(quicklink[str(i)]['locatorText']).replace(' ','').lower())
        t1 = cbScreenInstance.timeBar.getLabel(getHandle(setup, MRXConstants.COMPARATIVESCREEN, "ktrs"))
        checkEqualAssert(t[1], t1, selectedQuicklink,message="verify quicklink label")


    selectedCompareDim = cbScreenInstance.dropdown.doSelectionOnVisibleDropDown(getHandle(setup, MRXConstants.COMPARATIVESCREEN, "allselects"), str(CompareDim), index=0,parent="allselects")
    selectedCompareMes = cbScreenInstance.dropdown.doSelectionOnVisibleDropDown(getHandle(setup, MRXConstants.COMPARATIVESCREEN, "allselects"), str(CompareMes), index=1,parent="allselects")
    selectedBrokenDown = cbScreenInstance.dropdown.doSelectionOnVisibleDropDown(getHandle(setup, MRXConstants.COMPARATIVESCREEN, "allselects"), str(BrokenDown), index=2,parent="allselects")

    timeRangeFromPopup = str(t1)

    return timeRangeFromPopup,selectedCompareDim,selectedCompareMes,selectedBrokenDown