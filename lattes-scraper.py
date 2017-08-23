from selenium import webdriver
from io import BytesIO
import zipfile
import csv
import time
import urllib.request
from urllib.error import HTTPError

def getLattesXML(curriculo,driver):
    id = curriculo['ID']
  
    driver.get('http://buscacv.cnpq.br/buscacv/#/espelho?nro_id_cnpq_cp_s=%s' % id)
    elem = driver.find_element_by_xpath('//a[@title="Currículo em XML"]')
    url = elem.get_attribute('href')
    curriculoXML = urllib.request.urlopen("http://buscacv.cnpq.br" + url)
    
    zipFile = zipfile.ZipFile(BytesIO(curriculoXML.read()))
    curriculoXML = zipFile.read('curriculo.xml')
    zipFile.close()

    file = open('dados/xml/%s.xml' % id, 'wb')
    file.write(curriculoXML)
    file.close()

    time.sleep(5)
    
    print ('Lattes de ID %s criado!' % id)

    
def main():
    curriculos = csv.DictReader(open('dados/ids_lattes.csv', 'r'),delimiter=';')
    driver = webdriver.PhantomJS(executable_path='phantomjs.exe')

    for curriculo in curriculos:

        if curriculo['CODAREA'] != '10300007' or curriculo['DATAATUALIZACAO'] < '01/01/2015' or curriculo['DATAATUALIZACAO'] > '30/06/2017':
            continue
        else:
            try:
                getLattesXML(curriculo, driver)            
            except Exception as e:
                print ("Ocorreu uma exceção: %s" % e)
                driver.quit()
                time.sleep(100)
                driver = webdriver.PhantomJS(executable_path='phantomjs.exe')
                getLattesXML(curriculo, driver)            
    driver.quit()



if __name__ == '__main__':
    main()


    

