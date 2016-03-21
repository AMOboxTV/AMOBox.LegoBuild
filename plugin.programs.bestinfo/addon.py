import xbmcaddon
import xbmcgui
 
addon       = xbmcaddon.Addon()
addonname   = addon.getAddonInfo('name')
 
line1 = ' Esta aplicacao android é paga. Presupoe uma assinatura mensal.'
line2 = ''
line3 = '        mais informacoes em [COLOR blue]facebook.com/BestIPTV.PT[/COLOR]' 
 
xbmcgui.Dialog().ok(addonname, line1, line2, line3)
