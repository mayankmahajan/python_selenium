from Utils.SetUp import *
from MuralUtils.AlertsHelper import *
setup=SetUp()
# sleep(6)
login(setup,"admin","admin123")


checkDPIAlerts(setup)
setup.d.close()

# createKPIAlert(setup)
# GUIDE_INFO