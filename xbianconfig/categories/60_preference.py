import xbmcgui

from resources.lib.xbmcguie.xbmcContainer import *
from resources.lib.xbmcguie.xbmcControl import *
from resources.lib.xbmcguie.tag import Tag
from resources.lib.xbmcguie.category import Category, Setting
from resources.lib.utils import *
import resources.lib.translation

_ = resources.lib.translation.language.gettext

dialog = xbmcgui.Dialog()


class advancedLabel(Setting):
    CONTROL = CategoryLabelControl(Tag('label', _('Advanced')))


class advancedMode(Setting):
    DIALOGHEADER = _('Advanced_mode')
    CONTROL = RadioButtonControl(Tag('label', DIALOGHEADER))

    def onInit(self):
        self.key = 'advancedmode'

    def getUserValue(self):
        return str(self.getControlValue())

    def setControlValue(self, value):
        self.control.setValue(value)

    def getXbianValue(self):
        rc = self.getSetting(self.key)
        if rc == '1' or rc == 1 or rc == True or rc == 'True':
            setvisiblecondition(self.key, True)
        else:
            setvisiblecondition(self.key, False)
        return rc

    def setXbianValue(self, value):
        # xbmc.executebuiltin('Skin.ToggleSetting(%s)'%self.key)
        setvisiblecondition(self.key, self.setSetting(self.key, value))
        return True


class notificationLabel(Setting):
    CONTROL = CategoryLabelControl(Tag('label', _('Notifications')))


class notifyonError(advancedMode):
    DIALOGHEADER = _('Notify on error')
    CONTROL = RadioButtonControl(Tag('label', DIALOGHEADER))

    def onInit(self):
        self.key = 'notifyonerror'


class notifyonSuccess(advancedMode):
    DIALOGHEADER = _('Notify on success')
    CONTROL = RadioButtonControl(Tag('label', DIALOGHEADER))

    def onInit(self):
        self.key = 'notifyonsuccess'


class notifyonBusy(advancedMode):
    DIALOGHEADER = _('Show messages while playing media')
    CONTROL = RadioButtonControl(Tag('label', DIALOGHEADER))

    def onInit(self):
        self.key = 'notifywhenbusy'


class confirmonChange(advancedMode):
    DIALOGHEADER = _('Ask confirmation before saving new settings')
    CONTROL = RadioButtonControl(Tag('label', DIALOGHEADER))

    def onInit(self):
        self.key = 'confirmationonchange'


class enableAllHintsControl(MultiSettingControl):
    XBMCDEFAULTCONTAINER = False

    def onInit(self):
        if getHiddenHints() == 0:
            self.enableHints = ButtonControl(
                Tag('label', _('Enable all Hints')),
                Tag('visible', 'False'))
        else:
            self.enableHints = ButtonControl(
                Tag('label', _('Enable all Hints')),
                Tag('visible', '!%s' % (visiblecondition('hideresethints'),)))
        self.enableHints.onClick = lambda enablehints: self.enableAllHints()
        self.addControl(self.enableHints)

    def enableAllHints(self):
        pass


class enableAllHintsGui(Setting):
    CONTROL = enableAllHintsControl(ADVANCED)
    DIALOGHEADER = _('Enable all Hints')

    def onInit(self):
        self.control.enableAllHints = self.enableAllHints

    def enableAllHints(self):
        self.APPLYTEXT = _('Do you want to continue?')
        if self.askConfirmation():
            setvisiblecondition('hideresethints', True, xbmcgui.getCurrentWindowId())
            enableAllHints()

# CATEGORY CLASS
class preference(Category):
    TITLE = 'Preferences'
    SETTINGS = [advancedLabel, advancedMode, notificationLabel,
                confirmonChange, notifyonError, notifyonSuccess, notifyonBusy, enableAllHintsGui]
