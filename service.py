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
time = 10000 #in miliseconds
notify = addon.getSetting('notify') 
def upgrade():  

    path=xbmc.translatePath('special://temp/')
    path2=xbmc.translatePath('special://home/')

    if notify:
        xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(addonname,"Comprobando actualizacion", time, icon))
    
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
                   outpath = path2+"addons/plugin.video.pelisalacarta"
                   z.extract(name, outpath)
           fh.close()
        
           os.rename(path+'pelis.zip',path+'pelis.zip.old')
        
           xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(addonname,"Pelisalacarta upgradeado", 2*time , icon))
        
        except:
           xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(addonname,"Error en upgrade", time, icon))
   
    if notify:
        xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(addonname,"Terminada comprobacion", time, icon))
    
    return;

def test():
    xbmc.log('inicio el proceso')  
    
    path=xbmc.translatePath('special://temp/kk/')
    path2=xbmc.translatePath('special://home/')
    
    try:
           xbmc.log('intento abrir '+path+'pelis.zip')
           
           fh = open(path+'pelis.zip', 'rb')
           z = zipfile.ZipFile(fh)
           for name in z.namelist():
               if "main-classic" in str(name):
                   outpath = path2+"addons/plugin.video.pelisalacarta/"
                   xbmc.log('existe '+path+name+' y lo dejo en '+path2)
                   xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(addonname,name, 200, icon))
               else:
                   xbmc.log("porque no lo saca ?"+name+"?")
                   
           fh.close()
    except Exception as e:
           s = str(e)
           xbmc.log('error descomprimiento '+s)
           xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(addonname,"Error descomprimiendo", 10000, icon))
    
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




        