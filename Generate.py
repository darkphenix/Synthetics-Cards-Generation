#!/usr/bin/env python
# coding: utf-8
#---------------------------------------------------------------------------
#Generated synthetics cards
#
#(c) 2022 D@RK PH3N!X, Frenchabs
#Released under GNU Public Licence (GPL)
#
#--------------------------------------------------------------------------
#Import Libs
import cv2
from PIL import ImageFont, ImageDraw, Image
import numpy as np
#-------------------------------------
from random import randrange
import random
#-------------------------------------
import os
import pandas as pd
#-------------------------------------
import json
import string
from datetime import datetime, date
from datetime import timedelta
from tqdm import tqdm
import itertools

import argparse
#--------------------------------------------------------------------------
#-------------------------------------
def random_date(Start_m, End_m):
    '''
    Return random date

    Parameters
    ----------
    start : Date
    end : Date
    '''
    delta = End_m - Start_m
    return datetime.fromtimestamp(randrange((delta.days * 24 * 60 * 60) + delta.seconds))
#-------------------------------------
def getText(T_Label):
    '''
    Return Text

    Parameters
    ----------
    T_Label : String
    Type of structure in cards
    '''
    ALPHABET = list(string.ascii_uppercase)
    if T_Label == "NOM" or T_Label == "PRENOM" or T_Label == "SIGNATURE":
        SIZE_ = random.randint(3,8)
        return "".join([ALPHABET[random.randint(0,len(ALPHABET)-1)] for i in range(SIZE_)])
    elif T_Label == "CNI_ID":
        return str(random.randint(100000000000,999999999999))
    elif T_Label == "SEXE":
        return ["F","H"][random.randint(0,1)]
    elif T_Label == "YEAR" and random.randint(0,5) == 2:
        d1 = datetime.strptime('1.1.1940', '%d.%m.%Y')
        d2 = datetime.strptime('1.1.2020', '%d.%m.%Y')
        d = random_date(d1, d2).strftime('%d.%m.%Y')
        return str(d)
    elif T_Label == "CHECKSUM":
        DICT_CHECK = ALPHABET
        DICT_CHECK.extend([str(i) for i in range(0,9)])
        DICT_CHECK.append("<")
        return "".join([DICT_CHECK[random.randint(0,len(DICT_CHECK)-1)]+" " for i in range(28)])
    elif T_Label == "ADRESSE":
        SIZE_ = random.randint(3,8)
        return  "".join([str(ALPHABET[random.randint(0,len(ALPHABET)-1)]) for i in range(SIZE_)])+"   ( "+str(random.randint(10,96))+" )"
    elif T_Label == "TAILLE":
        return "1M"+ "".join([str(random.randint(5,9)),str(random.randint(0,9))])
    elif T_Label == "AUTRES":
        SIZE_ = random.randint(3,15)
        return "".join([ALPHABET[random.randint(0,len(ALPHABET)-1)] for i in range(SIZE_)])
    return ""


def main():
    #-------------------------------------
    #0 : CNI OLD
    #1 : CNI OLD verso
    #2 : CNI
    #3 : CNI verso
    #4 : Permis conduire
    #5 : Permis conduire verso
    #6 : PASSPORT
    parser = argparse.ArgumentParser()
    parser.add_argument('structure',type=int, default=0)
    parser.add_argument('iter',type=int, default=10)
    parser.add_argument('path',type=str, default="./GEN")
    parser.add_argument('name',type=str, default="GEN")

    args = parser.parse_args()

    id_index_generate_structure = args.structure
    args_Iteration = args.iter
    args_Path_Gen_Data = args.path
    args_Name_Gen_Data = args.name
    #-------------------------------------
    #Reads structures
    df_update = pd.DataFrame(columns=["filename","label","value"])
    pd_structure = pd.read_csv("./Templates/Generate_Structure.csv")
    #-------------------------------------
    #Load Structure in args
    j_to = json.loads(pd_structure["label"][id_index_generate_structure])
    #-------------------------------------
    #Load pattern
    image = cv2.imread(pd_structure["image"][id_index_generate_structure])
    cv2_im_rgb = cv2.cvtColor(image,cv2.COLOR_RGB2BGR)
    rows,cols = cv2_im_rgb.shape[:-1]
    #
    #-------------------------------------
    #Iteration Args
    #-------------------------------------
    for id_gen in tqdm(range(args_Iteration)):

        pil_im = Image.fromarray(image,"RGB")
        draw = ImageDraw.Draw(pil_im)
        for j in j_to:
            if j["rectanglelabels"][0] == "PHOTO":
                for i in range(rows):
                    for j in range(cols):
                        k = pil_im.getpixel((j,i))
                        if k[0] < 100 and  k[1] >= 200 and k[2] < 150:
                            pil_im.putpixel((j,i),(random.randint(0,150),random.randint(0,150),random.randint(0,150)))
            #-------------------------------------
            else:
                Margin_y = 0
                font_size = int(j["height"] / 100.0 * j["original_height"])
                font = ImageFont.truetype('arial',font_size)
                pixel_x = j["x"] / 100.0 * j["original_width"]
                stroke_width = 0
                pixel_width = j["width"] / 100.0 * j["original_width"]
                pixel_height = j["height"] / 100.0 * j["original_height"]
                #-------------------------------------
                if j["rectanglelabels"][0] == "CHECKSUM":
                    font = ImageFont.truetype('arial',28)
                    Margin_y = 3
                    pixel_y = j["y"] / 100.0 * j["original_height"]+50
                    draw.text((pixel_x, pixel_y), getText(j["rectanglelabels"][0]), font=font, fill=(60,60,60,255))
                #-------------------------------------
                elif j["rectanglelabels"][0] == "SIGNATURE":
                    Margin_y = -40
                    font = ImageFont.truetype('./Templates/Signature.otf',font_size)
                    stroke_width = 1
                #-------------------------------------
                elif j["rectanglelabels"][0] == "SIGNATURE":
                     Margin_y = -1
                #-------------------------------------
                pixel_y = j["y"] / 100.0 * j["original_height"]-Margin_y
                text_gen = getText(j["rectanglelabels"][0])
                #-------------------------------------
                df_update = df_update.append({"filename": "{0}/_{1}.jpg".format(args_Path_Gen_Data,str(id_gen)),"label":j["rectanglelabels"][0],"value":text_gen},ignore_index=True)
                draw.text((pixel_x, pixel_y), text_gen,stroke_width=stroke_width, font=font, fill=(60,60,60,255))

        #-------------------------------------
        cv2_im_processed = np.array(pil_im)
        cv2.imwrite("{0}/_{1}.jpg".format(args_Path_Gen_Data,str(id_gen)),cv2_im_processed,[int(cv2.IMWRITE_JPEG_QUALITY), 70])
    #-------------------------------------
    df_update.to_excel("{0}.xlsx".format(args_Name_Gen_Data))


if __name__ == "__main__":
    main()
