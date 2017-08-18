from BaseComponentClass import BaseComponentClass
from Utils.ConfigManager import ConfigManager
from Utils.logger import *
from selenium.common.exceptions import *
import time

class SwitcherComponentClass(BaseComponentClass):

    def __init__(self):
        BaseComponentClass.__init__(self)
        self.configmanager = ConfigManager()


    def doSingleSelection(self):
        BaseComponentClass.click()

    def setSelection(self,index,h,parent="switcherView"):
        data = {}
        toSelect = 'Chart' if index==0 else 'Table'
        handlers = self.compHandlers(parent,h)
        for key,value in handlers.iteritems():
            if toSelect.upper() in key.upper():
                if self.configmanager.componentSelectors[parent][key]["action"] == "click":
                    for i in range(len(handlers[key]),0,-1):
                        if handlers[key][i-1].is_displayed():
                            handlers[key][i-1].click()
                            return handlers[key][i-1].text

    def getSelection(self,h,parent="switcherView"):
        data = {}
        handlers = self.compHandlers(parent,h)
        for key,value in handlers.iteritems():
            if self.configmanager.componentSelectors[parent][key]["action"] == "click":
                # for i in range(0,len(handlers)):
                if handlers[key][len(handlers[key]) - 1].is_displayed() and 'SELECTED' in handlers[key][len(handlers[key]) - 1].get_attribute('class').upper():
                    logger.debug("SwitcherCard Selection : %s", handlers[key][len(handlers[key]) - 1].text)
                    return handlers[key][len(handlers[key]) - 1].text


    def switchTo(self,index,h,parent="createdialog",child="switcher"):
        try:
            h[parent][child][len(h[parent][child])-1].find_elements_by_tag_name("li")[index].click()
            time.sleep(2)
            return True
        except NoSuchElementException or StaleElementReferenceException or ElementNotVisibleException or Exception as e:
            raise e("%s %s",parent,child)
            return e

    # for mural
    def measureChangeSwitcher(self,index,h,parent="measureChangeSection",child="switcher",occurence = 0):
        try:
            logger.info("Going to click Switcher index = %d",index)
            h[parent][child][occurence].find_elements_by_tag_name('div')[index].click()
            try:
                h[parent][child][occurence].find_elements_by_tag_name('div')[index].click()
            except:
                pass
            time.sleep(2)
            return True
        except Exception as e:
            logger.error("Got Exception while using Measure Switcher %s",str(e))
            return e

    def measureChangeSwitcher_UD(self,index,h,parent="switcher",child="switches"):
        try:
            logger.info("Going to click Switcher index = %d",index)
            h[parent][child][index].click()
            try:
                h[parent][child][index].click()
            except:
                pass
            time.sleep(2)
            return True
        except Exception as e:
            logger.error("Got Exception while using Switcher %s",str(e))
            return e

    def getMeasureChangeSelectedSwitcher_UD(self,h,parent="switcher",child="switches"):
        try:
            if not h[parent][child]:
                return False
            divs = h[parent][child]
            selectedSwitcher = []
            for i in range(len(divs)):
                if "selected" in str(divs[i].get_attribute("class")).lower():  # changes "ng-reflect-class" to "class" in get_attribute
                    selectedSwitcher.append(i)
            time.sleep(2)
            return selectedSwitcher
        except Exception as e:
            logger.error("Got Exception while getting Measure Switcher Selection = %s", str(e))
            return e


    # for mural
    def getMeasureChangeSelectedSwitcher(self,h,parent="measureChangeSection",child="switcher",occurence = 0):
        try:
            if not h[parent][child]:
                return False
            divs = h[parent][child][occurence].find_elements_by_tag_name('div')
            selectedSwitcher = []
            for i in range(len(divs)):
                if "active" in str(divs[i].get_attribute("class")).lower():
                    selectedSwitcher.append(i)
            time.sleep(2)
            return selectedSwitcher
        except Exception as e:
            logger.error("Got Exception while getting Measure Switcher Selection = %s",str(e))
            return e

    def getMeasureChangeSelectedSwitcherText(self,h,parent="measureChangeSection",child="switcher",occurence=0):
        try:
            if not h[parent][child]:
                return False
            divs = h[parent][child][occurence].find_elements_by_tag_name('div')
            selectedSwitcher = []
            for i in range(len(divs)):
                if "active" in str(divs[i].get_attribute("class")).lower():
                    selectedSwitcher.append(str(divs[i].text).strip().strip('\n').strip())
            time.sleep(2)
            return selectedSwitcher
        except Exception as e:
            logger.error("Got Exception while getting Measure Switcher Selection = %s",str(e))
            return e


    def isMeasureChangeSwitcherEnabled(self,index,h,parent="measureChangeSection",child="switcher",occurence = 0):
        try:
            if not h[parent][child]:
                return False
            logger.info("Going to check whether Switcher with index = %d enable or not",index)
            if 'disable' in str(h[parent][child][occurence].find_elements_by_tag_name('div')[index].get_attribute('class')).lower():
                return False
            return True

        except Exception as e:
            logger.error("Got Exception while getting Measure Switcher status (Enable or Disable) = %s",str(e))
            return e

