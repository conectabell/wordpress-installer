# -*- coding: utf-8 -*-
import sys
import os
import fileinput
import getpass
import MySQLdb
from urllib import urlretrieve, urlcleanup
import tarfile
import webbrowser


def main():
    print ("===========Instalador de Wordpress Express================\n"
           "-------------------- Version 0.2 Beta --------------------\n"
           "--- Se necesitan privilegios de root@localhost de MySQL --")
    print ("-----Se necesitan privilegios de root en el sistema-------")
    print ("==========================================================")
    pwsql = getpass.getpass("Contraseña root MySQL: ")
    #print (pwsql)
    bd = MySQLdb.connect(host="localhost",
                     user="root",
                      passwd=pwsql)
    cursor = bd.cursor()
    cursor.execute("SELECT VERSION()")
    versiondb = cursor.fetchone()
    bd.close()
    print ("==========================================================")
    print ("Version de la Base de datos %s" % versiondb)
    print ("==========================================================")
    nombre = raw_input("Escriba el nombre del Wordpress: ")
    nombreuser = nombre + "user@localhost"
    passdb = getpass.getpass("Introduzca el nuevo password"
                                " del usuario MySQL %s: " % nombreuser)
    createdb(pwsql, nombre)
    createuser(pwsql, nombreuser)
    setuserpass(pwsql, nombreuser, passdb)
    grantuser(pwsql, nombre, nombreuser, passdb)
    descargawp()
    extraertar()
    replaceAll("wordpress/wp-config-sample.php", "database_name_here", nombre)
    replaceAll("wordpress/wp-config-sample.php", "username_here", nombre +
                                                                    "user")
    replaceAll("wordpress/wp-config-sample.php", "password_here", passdb)
    cmd0 = "cp ./wordpress/wp-config-sample.php ./wordpress/wp-config.php"
    os.system(cmd0)
    print ("====> Generado wp-config.php")
    cmd1 = "mkdir /var/www/html/" + nombre
    cmdrm1 = "rm ./wordpress/readme.html"
    cmdrm2 = "rm ./wordpress/license.txt"
    cmd2 = "cp ./wordpress/* /var/www/html/" + nombre + " -R"
    cmd3 = "rm -rf ./wordpress"
    cmd4 = "rm ./latest.tar.gz"
    cmd5 = "chown www-data:www-data /var/www -R"
    print ("====> Eliminando readme.html y license.txt")
    os.system(cmdrm1)
    os.system(cmdrm2)
    print ("====> Moviendo Ficheros")
    os.system(cmd1)
    os.system(cmd2)
    print ("====> Eliminando archivos temporales")
    os.system(cmd3)
    os.system(cmd4)
    print ("====> Aisgnando permisos para www-data")
    os.system(cmd5)
    print ("====> Todo terminado :)")
    print ("====> Abriendo página web de configuración")
    print ("====> http://127.0.0.1/" + nombre + "/wp-admin/")
    #webbrowser.open_new("http://127.0.0.1/" + nombre + "/wp-admin/")


def createdb(pwsql, nombre):
    try:
        bd = MySQLdb.connect(host="localhost",
                     user="root",
                      passwd=pwsql,
                      db="mysql")
        cursor = bd.cursor()
        cursor.execute("CREATE DATABASE " + nombre)
        #data2 = cursor.fetchone()
        #print ("====> %s" % data2)
        print ("====> Base de datos OK")
        bd.close()
    except MySQLdb.ProgrammingError, e:
        print ("====> ERROR: Base de datos ya existe")
        print ("====> " + e)


def createuser(pwsql, nombreuser):
    try:
        bd = MySQLdb.connect(host="localhost",
                     user="root",
                      passwd=pwsql,
                      db="mysql")
        cursor = bd.cursor()
        cursor.execute("CREATE USER " + nombreuser)
        #data2 = cursor.fetchone()
        print ("==========================================================")
        print ("====> Creacion de usuario OK")
        #print (data2)
        bd.close()
    except MySQLdb.OperationalError:
        print ("====> ERROR: Usuario existente")
        print ("==========================================================")


def setuserpass(pwsql, nombreuser, passdb):
    try:
        bd = MySQLdb.connect(host="localhost",
                     user="root",
                      passwd=pwsql)
        cursor = bd.cursor()
        cursor.execute("SET PASSWORD FOR " + nombreuser +
                        "= PASSWORD( \"" + passdb + "\" )")
        print ("====> Password Creado")
        bd.close()
    except MySQLdb.ProgrammingError, e:
        print e


def grantuser(pwsql, nombre, nombreuser, passdb):
    try:
        bd = MySQLdb.connect(host="localhost",
                         user="root",
                          passwd=pwsql,
                          db="mysql")
        cursor = bd.cursor()
        cursor.execute("GRANT ALL PRIVILEGES ON " + nombre + ".* TO "
                        + nombreuser + " IDENTIFIED BY \'" + passdb + "\'")
        cursor.execute("FLUSH PRIVILEGES")
        print ("====> Privilegios Otorgados")
        bd.close()
    except MySQLdb.ProgrammingError, e:
        print e


def status(count, data_size, total_data):
    procent = int(count * data_size * 100 / total_data)
    #print count, file_size_dl, data_size, total_data
    global con
    if procent == 10:
        if con == 0:
            con = 1
            print "====> Descargando " + (str(procent) + "%")
    if procent == 27:
        if con == 1:
            con = 2
            print "====> Descargando " + (str(procent) + "%")
    if procent == 52:
        if con == 2:
            con = 3
            print "====> Descargando " + (str(procent) + "%")
    if procent == 76:
        if con == 3:
            con = 4
            print "====> Descargando " + (str(procent) + "%")
    if procent == 98:
        if con == 4:
            con = 5
            print "====> Descargando " + (str(procent) + "%")
    if procent == 100:
        if con == 5:
            con = 0
            print "====> ¡" + (str(procent) + "% Completado!")


def descargawp():
    url = ("http://wordpress.org/latest.tar.gz")
    filename = url[url.rfind("/") + 1:]
    while not filename:
        filename = raw_input("====> No se ha podido obtener el nombre del "
                                "archivo.\nEspecifique uno: ")
    print ("====> Descargando %s..." % filename)
    urlretrieve(url, filename, status)
    urlcleanup()
    print ("====> %s descargado correctamente." % filename)


def extraertar():
    print("====> Extrayendo...")
    tar = tarfile.open("latest.tar.gz")
    tar.extractall()
    tar.close()
    print("====> Extraido")


def replaceAll(file, searchExp, replaceExp):
    for line in fileinput.input(file, inplace=1):
        if searchExp in line:
            line = line.replace(searchExp, replaceExp)
        sys.stdout.write(line)

if __name__ == "__main__":
    if not os.geteuid() == 0:
        sys.exit('Este programa debe ejecutarse como root')
    else:
        global con
        con = 0
        main()