import gi

import utils
import switcher

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

gi.require_version('AppIndicator3', '0.1')
from gi.repository import AppIndicator3 as appindicator

gi.require_version('Notify', '0.7')
from gi.repository import Notify
import os

APPINDICATOR_ID = 'prime-switcher'


def reboot(widget, *data):
    """GTK Event (On click on reboot button in success notificatiob)

    Reboot the system
    """
    os.system('shutdown -r now')


def switch(widget, *data):
    """GTK Event (On click on 'Switch Button')

    Execute command to switch to selected mode and display notification depending on result.

    Parameters
    ----------
    data[0] : Notify.Notification
        The success notification
    data[1] : Notify.Notification
        The failure notification
    data[2] : str
        Target mode
    """
    success = os.system('pkexec /usr/bin/prime-switcher -s {}'.format(data[2])) == 0
    data[int(not success)].show()


def open_gui():
    """Create and display the indicator"""
    modes_names = [_('Power Saving'), _('Balanced')]

    # Notifications Declaration BEGIN
    Notify.init("Prime Switcher")

    success_notify = Notify.Notification.new(_("Reboot required"), _("Reboot is required to apply modifications"))
    success_notify.add_action('reboot', _('Reboot now'), reboot, None, None)

    error_notify = Notify.Notification.new(_("Error"), _("An error has occurred."), "error")

    # Notifications Declaration END

    # Menu BEGIN
    menu = Gtk.Menu()

    is_powersaved = switcher.is_powersaved()

    item = Gtk.MenuItem(_('Switch to {} mode').format(modes_names[int(not is_powersaved)]))
    item.connect('activate', switch, success_notify, error_notify,
                 switcher.modes[int(is_powersaved)])
    menu.append(item)

    menu.append(Gtk.SeparatorMenuItem())

    current_mode = Gtk.MenuItem(_('Current Mode : {}').format(modes_names[int(is_powersaved)]))
    current_mode.set_sensitive(False)
    menu.append(current_mode)

    # Menu END

    indicator = appindicator.Indicator.new(APPINDICATOR_ID, os.path.join(
        utils.get_debug_path('assets') if os.getenv('DEBUG', 0) else '/usr/share/prime-switcher/', "intel.png" if is_powersaved else "nvidia.png"),
                                           appindicator.IndicatorCategory.SYSTEM_SERVICES)
    indicator.set_menu(menu)
    indicator.set_status(appindicator.IndicatorStatus.ACTIVE)

    menu.show_all()

    Gtk.main()
    Notify.uninit()
