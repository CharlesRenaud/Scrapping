import requests
from bs4 import BeautifulSoup
import re
import numpy

def Links():
    links = []
    for i in range (1):
        url = 'https://frscan.cc/manga-list/2/2?page=' + str(i)
        response = requests.get(url)
        soup = BeautifulSoup(response.text)
        mydivs = soup.findAll("a", {"class": "chart-title"})
        for mydiv in mydivs:
            link = mydiv['href']
            links.append(link)
    return links            


def Covers():
    covers = []
    links = Links()

    for link in links:
        url = str(link)
        response = requests.get(url)
        soup = BeautifulSoup(response.text)
        mydivs = soup.findAll("img", {"class": "img-responsive"})
        for mydiv in mydivs:
            cover = mydiv['src']    
            covers.append(cover)
    return covers
    


def Names():
    names = []
    for i in range (1):
        url = 'https://frscan.cc/manga-list/2/2?page=' + str(i)
        response = requests.get(url)
        soup = BeautifulSoup(response.text)
        mydivs = soup.findAll("a", {"class": "chart-title"})
        for mydiv in mydivs:
            text = mydiv.text
            names.append(text)
    return names 

def NbrOfVolumes():
    nbrvolumes = []
    links = Links()
    sortie = []
    for link in links:
        url=str(link)
        response = requests.get(url)
        soup = BeautifulSoup(response.text)
        mydivs = soup.findAll("h5", {"class": "chapter-title-rtl"})
        sortie.append(len(mydivs))
    return sortie

def VolumesID():
    numbers = []
    links = Links()
    volumes = []
    volux = []
    for link in links:
        url = str(link)
        response = requests.get(url)
        soup = BeautifulSoup(response.text)
        mydivs = soup.findAll("h5", {"class": "chapter-title-rtl"})
        for mydiv in mydivs:
            oi = mydiv.findAll("a")
            for o in oi:
                io = o['href']
                caca = io[-5:]
                stylax = re.findall(r"[-+]?\d*\.\d+|\d+", caca)
                volux.append(''.join(stylax))
    return volux

def VolumeIdArray():
    volux = VolumesID()
    nbrOfVolumes = NbrOfVolumes()
    store = []
    stored = []
    iterator = 0
    count = -1
    for nbrOfVolume in nbrOfVolumes:
        print(nbrOfVolume)
        for volu in volux:
            count += 1
            print(count)
            iterator += 1
            if iterator <= nbrOfVolume:
                store.append(volux[count])
            else:
                iterator=0
                count-=1
                stored.append(store)
                store = []
                break
    return stored
                

def NbrPagePerChapter():
    links = Links()
    nbrvolumes = NbrOfVolumes()
    volux = VolumesID()
    store = []
    iterator = 1
    count = -1
    stored = []
    for link, nbrvolume in zip(links, nbrvolumes):
        for volumeID in volux:
            if count == len(volux)-1:
                return stored
            count +=1
            print(str(count) + " " +'count')
            url2 = str(link) + '/' + volux[count] + '/1'
            print(str(nbrvolume) + " " + 'nombre de volume')
            print(str(iterator) + " " + 'iterarteur')
            if iterator <= nbrvolume:
                iterator += 1
                print(url2)
                response = requests.get(url2)
                soup = BeautifulSoup(response.text)
                try:
                    mydivs = soup.find("select", {"id": "page-list"}).findAll('option')    
                except:
                    mydivs = [0]
                store.append(len(mydivs))
            else:
                iterator = 1
                count -= 1
                stored.append(store)
                store = []
                break
        print(stored)

def ComboScore():
    links = Links()
    comboScore = []
    for i in range(len(links)):
        comboScore.append(i)
    return comboScore

def MixexIdArray():
    volumes = VolumeIdArray()
    ty = []
    result = []

    for volume in volumes:
        for volu in volume:
            if "." in volu:
                ty.append(float(volu))
            else:
                ty.append(int(volu))

        result.append(ty)
        ty = []
    print(result)
    return result

def MangaDescription():
    links = Links()
    descriptions = []
    for link in links:
        url = str(link)
        response = requests.get(url)
        soup = BeautifulSoup(response.text)
        try:
            mydivs = soup.find("div", {"class": "well"}).find("p").text
            test = mydivs.replace('"', "'")
            descriptions.append(test)
            print(test)
        except:
            mydivs = "À venir..."    
            descriptions.append(mydivs)
    return descriptions       

def Action():
    covers = Covers()
    links = Links()
    names = Names()
    volumes = NbrOfVolumes()
    nbrofpages = NbrPagePerChapter()
    comboScores = ComboScore()
    volumesID = VolumesID()
    volumeIdArrays = MixexIdArray()
    mangaDescriptions = MangaDescription()
    with open('V2.json', "w", encoding="utf-8") as file:
        for link, name, volume, nbrofpage, comboScore, volumeID, volumeIdArray, cover, mangaDescription in zip(links, names, volumes, nbrofpages, comboScores, volumesID, volumeIdArrays, covers, mangaDescriptions):
            vv = str(volume)
            file.write('{' + '\n' +
                            '"name":'+ '"' + name + '",' + '\n' +
                            '"cover":'+ '"' + cover + '",' + '\n' +
                            '"link":' + '"' + link + '",' + '\n' +
                            '"description":' + '"' + mangaDescription + '",' + '\n' +
                            '"nbrChapter":' + '"' + vv + '",' + '\n' + 
                            '"ChapterId":' + str(volumeIdArrays[comboScore]) + ',' + '\n' + 
                            '"pagePerChapter":' + str(nbrofpages[comboScore]) + '\n' +
                        '},' + '\n') 

Action()
