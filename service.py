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

path=xbmc.translatePath('special://temp/')
path2=xbmc.translatePath('special://home/')

time = 7000 #in miliseconds

def upgrade():  
    
    notify = addon.getSetting('notify') 
    tiempo = addon.getSetting('tiempo')     
    
    if notify:
        xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(addonname,"checking git-master", time, icon))
    
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
                   xbmc.log('UpdPelisALaCarta - '+name+' -> '+outpath)
                   
           fh.close()
        
           os.rename(path+'pelis.zip',path+'pelis.zip.old')
        
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
