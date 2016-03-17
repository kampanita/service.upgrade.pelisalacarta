import time 
import xbmc
import xbmcaddon
import xbmcgui
import urllib
import urllib2
import base64
import zipfile
import os

addon       = xbmcaddon.Addon()
addonname   = addon.getAddonInfo('name')
icon = addon.getAddonInfo('icon')
tiempo = addon.getSetting('tiempo') 
time = 5000 #in miliseconds

def upgrade():  

    path=xbmc.translatePath('special://temp/')
    path2=xbmc.translatePath('special://home/')

    file = urllib2.urlopen("https://codeload.github.com/tvalacarta/pelisalacarta/zip/master")
    file_int = int(file.info()['Content-Length'])
    
    try :    
        file_local = int(os.path.getsize(path+'pelis.zip.old'))
    
    except :    
        file_local = 0
    
    if file_int <> file_local:
    
        urllib.urlretrieve ("https://codeload.github.com/tvalacarta/pelisalacarta/zip/master", path+'pelis.zip')
                
        try:
           fh = open(path+'pelis.zip', 'rb')
           z = zipfile.ZipFile(fh)
           for name in z.namelist():
               if "main-classic" in str(name):
                   outpath = path2+"addons/plugin.video.pelisalacarta/"
                   z.extract(name, outpath)
           fh.close()
        
           os.rename(path+'pelis.zip',path+'pelis.zip.old')
        
           xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(addonname,"Pelisalacarta upgradeado", time, icon))
        
        except:
           xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(addonname,"Error en upgrade", time, icon))
    return;

upgrade()

if __name__ == '__main__':

    monitor = xbmc.Monitor()
 
    while not monitor.abortRequested():
        # Sleep/wait for abort for tiempo in minutos
        if monitor.waitForAbort(60*int(tiempo)):
            # Abort was requested while waiting. We should exit
            break
        upgrade()




        
