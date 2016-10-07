from django.utils.translation import ugettext_lazy as _


# Array of suspicious URLs which are generally called by Users who have
# malicious intent to harm our system.
SUSPICIOUS_PATHS = [
    '/phpmyadmin/scripts/setup.php',
    '/phpMyAdmin/scripts/setup.php',
    '/pma/scripts/setup.php',
    '/myadmin/scripts/setup.php',
    '/OnlineUpdate/questions.php',
    '/phpmyadmin',
    '/HNAP1/',
    '/wp-login.php',
    '/administrator/index.php',
    '/manager/html',
    '/ip_json.php',
    '/hndUnblock.cgi',
    '/tmUnblock.cgi',
    '/cgi/common.cgi',
    '/stssys.htm',
    '/admin/config.php',
    '/check_proxy',
    '/muieblackcat',
    '/pma/scripts/setup.php',
    '/CHANGELOG.txt',
    '/readme.html',
    '/.git/HEAD',
    '/zabbix/index.php',
    '/xmlrpc.php',
    '/r/errors.log',
    '/license.php',
    '/web-console/ServerInfo.jsp',
    '/jmx-console/HtmlAdaptor',
    '/if youve had a dose of a freaky ghost',
    '/invoker/JMXInvokerServlet',
    '/status',
    '/engine/log.txt',
    '/command.php',
    '/wp-includes/js/wp-util.js',
    '/benutzer/env.cgi',
    '/1phpmyadmin/'
]
