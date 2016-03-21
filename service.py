import time 
import xbmc
import xbmcaddon
import xbmcgui
import urllib
import urllib2
import base64
import zipfile
import os
import shutil

addon       = xbmcaddon.Addon()
addonname   = addon.getAddonInfo('name')
icon = addon.getAddonInfo('icon')

path= addon.getSetting('temp')
path2=xbmc.translatePath('special://home/')
tiempo = addon.getSetting('tiempo')  
notify = addon.getSetting('notify')    

time = 7000 #in miliseconds



def upgrade():  
    
    notify = addon.getSetting('notify') 
    tiempo = addon.getSetting('tiempo')     
    path= addon.getSetting('temp')
    
    if notify:
        xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(addonname,"checking git-master", time, icon))
    
    file = urllib2.urlopen("https://codeload.github.com/tvalacarta/pelisalacarta/zip/master")
    file_int = int(file.info()['Content-Length'])
    
    try :    
        file_local = int(os.path.getsize(xbmc.translatePath(path+'pelis.zip.old')))
    
    except :    
        file_local = 0
        xbmc.log("No encuentro el fichero");
        
    if file_int <> file_local:
        
        if notify:
            xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(addonname,"downloading new version", time, icon))            
        
        urllib.urlretrieve ("https://codeload.github.com/tvalacarta/pelisalacarta/zip/master",  xbmc.translatePath(path+'pelis.zip'))
                
        try:
           fh = open( xbmc.translatePath(path+'pelis.zip'), 'rb')
           z = zipfile.ZipFile(fh)
          
           for name in z.namelist():
               if "main-classic" in str(name):
                   
                   z.extract(name,xbmc.translatePath(path))                
                 
           fh.close()
           
           shutil.move(xbmc.translatePath(path+'pelisalacarta-master/python/main-classic/*'), xbmc.translatePath(path2+'/addons/plugin.video.pelisalacarta/'))
           os.remove(xbmc.translatePath(path+'pelis.zip.old'))
           os.rename(xbmc.translatePath(path+'pelis.zip'),xbmc.translatePath(path+'pelis.zip.old'))
        
           xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(addonname,"upgraded from git-master", 2*time , icon))
        
        except Exception as e:
           s = str(e)
           xbmc.log('UpdPelisALaCarta - Error en el proceso '+s)  
           xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(addonname,"Error upgrade", time, icon))
   
    else:
        if notify:
           xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(addonname,"No need to upgrade", time , icon))
           
    if notify:
        xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(addonname,"finished checking", time, icon))
    
    return;

def test():
	
    xbmc.log('inicio el proceso')    
    return;
  
#test()

upgrade()

if __name__ == '__main__':

    monitor = xbmc.Monitor()
 
    while not monitor.abortRequested():
        # Sleep/wait for abort for 10 seconds ( media hora )
        if monitor.waitForAbort(60*int(tiempo)):
            # Abort was requested while waiting. We should exit
            break
        upgrade()
