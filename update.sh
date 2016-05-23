#!/bin/bash

now=$(date +'%d/%m/%Y %R')
echo ${now} Inicia el proceso. > /storage/scripts/upgrade.log


FILE_DIR="/storage/scripts"
URL="https://codeload.github.com/tvalacarta/pelisalacarta/zip/master" 

SIZE=$(curl -sI $URL | grep Content-Length | cut -d ' ' -f 2)

echo El fichero de git pesa: $SIZE >> /storage/scripts/upgrade.log

SIZE_2=$(ls -la $FILE_DIR/pelis.zip.old | awk '{ print $5}')


echo El fichero local pesa: $SIZE_2 >> /storage/scripts/upgrade.log


 if [ $SIZE -ne $SIZE_2 ]; then

  echo Nos traemos el fichero >> /storage/scripts/upgrade.log
  curl -o ${FILE_DIR}/pelis.zip $URL

  echo Unzip del fichero >> /storage/scripts/upgrade.log
  unzip -o ${FILE_DIR}/pelis.zip pelisalacarta-master/python/main-classic/* -d ${FILE_DIR} > /dev/null

  echo copia el plugin >> /storage/scripts/upgrade.log
  cp -rf ${FILE_DIR}/pelisalacarta-master/python/main-classic/* /storage/.kodi/addons/plugin.video.pelisalacarta/ > /dev/null
  echo Unzip del fichero 

  echo renombra zip origen >> /storage/scripts/upgrade.log
  mv $FILE_DIR/pelis.zip $FILE_DIR/pelis.zip.old

  echo borramos directorio descomprimido >> updgrade.log
  rm -rf ${FILE_DIR}/pelisalacarta-master
 fi

now=$(date +'%d/%m/%Y %R')
echo ${now}  proceso acabado >> /storage/scripts/upgrade.log
cat /storage/scripts/upgrade.log
