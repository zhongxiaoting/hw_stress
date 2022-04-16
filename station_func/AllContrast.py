# -*- coding: utf-8 -*-
from __future__ import print_function
import os
import sys
import io
import commands
from main.item import Item
from common import constants as c


sys.path.append("..")



class cmpFile(Item):

    def __init__(self, file1, file2):

        self.file1 = file1
        self.file2 = file2

    def run_item(self):
        #self.hebing()
        self.fileExists()
        self.compare()


    def hebing(self):
        for filename in os.listdir('/home/hw_stress/good'):
            print(filename)
            with io.open(c.xgy_check + '/' + filename, encoding='utf-8') as f:
                for line in f.readlines():
                    with open(c.xgy_check, "a") as fp:
                        fp.write(line)




    def fileExists(self):
        if os.path.exists(self.file1) and \
                os.path.exists(self.file2):
            return True
        else:
            return False

    #
    def compare(self):
        if cmpFile(self.file1, self.file2).fileExists() == False:
            return []

        fp1 = open(self.file1)
        fp2 = open(self.file2)
        flist1 = [i for i in fp1]
        flist2 = [x for x in fp2]
        fp1.close()
        fp2.close()
        flines1 = len(flist1)
        flines2 = len(flist2)

        if flines1 < flines2:
            flist1[flines1:flines2+1] = ' ' * (flines2 - flines1)
        if flines2 < flines1:
            flist2[flines2:flines1+1] = ' ' * (flines1 - flines2)

        counter = 1
        cmpreses = []
        for x in zip(flist1, flist2):
            if x[0] == x[1]:
                counter +=1
                continue
            if x[0] != x[1]:
                cmpres = ' the %s is error, this is: %s --> %s' % \
                         (counter, x[0].strip(), x[1].strip())
                cmpreses.append(cmpres)
                counter +=1
        for i in range(len(cmpreses)):
            print(cmpreses[i],end='\n')
                
        return cmpreses

