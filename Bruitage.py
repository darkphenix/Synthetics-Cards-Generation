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
import numpy as np
import imutils
import random
from PIL import ImageFont, ImageDraw, Image, ImageFilter, ImageEnhance
import glob
import pandas as pd
import json
from tqdm import tqdm
import argparse
#--------------------------------------------------------------------------
def gaussian_noise(Image_m, Sigma_m):
    '''
    Return Image noise

    Parameters
    ----------
    Image_m : Matrix
    Sigma_m : Level Noise
    Type of structure in cards
    '''
    img = np.array(Image_m)
    noise = np.random.randn(img.shape[0], img.shape[1], img.shape[2])
    img = img.astype('int16')
    img_noise = np.clip(img + noise * Sigma_m, 0, 255).astype('uint8')
    return Image.fromarray(img_noise)

#-------------------------------------------------------------------------
def poisson_noise(Image_m, Factor_m):
    '''
    Return Image noise

    Parameters
    ----------
    Image_m : Matrix
    Factor_m : Level Noise
    Type of structure in cards
    '''
    factor = 1 / Factor_m
    img = np.array(Image_m).astype('int16')
    img_noise = np.random.poisson(img * factor) / float(factor)
    np.clip(img_noise, 0, 255, img_noise)
    img_noise = img_noise.astype('uint8')
    return Image.fromarray(img_noise)



def main():
    #Lecture des structures
    pd_structure = pd.read_csv("./Templates/Generate_Structure.csv")

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
    #---------------------------------------------------
    parser.add_argument('--rezize_min',type=int, default=500)
    parser.add_argument('--rezize_max',type=int, default=700)
    #-------------------
    parser.add_argument('--blur_back',type=int, default=10)
    parser.add_argument('--line_back',type=int, default=700)
    #---------------------------------------------------
    parser.add_argument('--noise',type=int, default=15)
    parser.add_argument('--blur',type=float, default=1.5)
    #-------------------
    parser.add_argument('--color',type=float, default=1.5)
    parser.add_argument('--constrast_max',type=float, default=1.5)
    parser.add_argument('--brightness_max',type=float, default=1.5)

    parser.add_argument('--constrast_min',type=float, default=0.5)
    parser.add_argument('--brightness_min',type=float, default=0.5)

    parser.add_argument('path',type=str, default="./GEN")
    parser.add_argument('name',type=str, default="GEN")

    args = parser.parse_args()

    id_index_generate_structure = args.structure
    args_Path_Gen_Data = args.path
    args_Name_Gen_Data = args.name
    #------------------------------------
    #Param Noise
    rezize_min = args.rezize_min
    rezize_max = args.rezize_max

    blur_back = args.blur_back
    line_back = args.line_back

    noise = args.noise
    blur = args.blur
    color = args.color

    constrast_max = args.constrast_max
    brightness_max = args.brightness_max

    constrast_min = args.constrast_min
    brightness_min = args.brightness_min


    '''
    id_index_generate_structure = 0
    args_Path_Gen_Data = "./GEN"
    args_Name_Gen_Data = "GEN"
    #------------------------------------
    #Param Noise
    rezize_min = 500
    rezize_max = 700

    blur_back = 5
    line_back = 50

    noise = 5
    blur = 1.5
    color = 1.5

    constrast_max = 1.5
    brightness_max = 1.5

    constrast_min = 0.5
    brightness_min = 0.5
    #-------------------------------------
    '''
    #-------------------------------------
    j_to = json.loads(pd_structure["label"][id_index_generate_structure])
    df_update =pd.read_excel("{0}.xlsx".format(args_Name_Gen_Data))

    for file in tqdm(glob.glob("{0}/*.jpg".format(args_Path_Gen_Data))):

        back_im = (np.random.standard_normal([1000, 1000, 3]) * random.randint(0,250)).astype(np.uint8)

        file = file.replace("\\","/")
        #----------------------------------------------------------------
        img = cv2.imread(file)
        #img = cv2.cvtColor(img,cv2.COLOR_RGB2BGR)
        img = cv2.cvtColor(img, cv2.COLOR_RGB2RGBA)
        img = cv2.resize(img,None,fx=2, fy=2, interpolation = cv2.INTER_CUBIC)
        #OR
        rows_orig,cols_orig = img.shape[:2]

        #MIN - MAX = 500 -700
        img = imutils.resize(img, width=random.randint(rezize_min,rezize_max))

        rows,cols = img.shape[:2]

        pil_im = Image.fromarray(img,"RGBA")
        back_im = Image.fromarray(back_im,"RGB")


        #Blur Back 10
        back_im = back_im.filter(ImageFilter.BoxBlur(random.randint(1,blur_back)))

        img1 = ImageDraw.Draw(back_im)
        #Random Line = 100
        for i_line in range(random.randint(0,line_back)):
            alea_line = random.randint(0,3)
            if alea_line == 0:
                row_line =random.randint(0,cols_orig)
                shape = [(0, row_line), (cols_orig, row_line)]
                img1.line(shape, fill ="white", width = random.randint(0,4))
            elif alea_line == 1:
                row_line =random.randint(0,rows_orig)
                shape = [(row_line,0), (row_line, rows_orig)]
                img1.line(shape, fill ="white", width = random.randint(0,4))
            elif alea_line == 2:
                row_line =random.randint(0,cols_orig)
                cols_line =random.randint(0,rows_orig)
                row_line_b =random.randint(0,cols_orig)
                cols_line_b =random.randint(0,rows_orig)
                shape = [(row_line, cols_line), (row_line_b, cols_line_b)]
                img1.line(shape, fill ="white", width = random.randint(0,4))

        #Random Noise = 15
        pil_im = poisson_noise(pil_im,random.randint(1,noise))
        #Random Blur  = 1.5
        pil_im = pil_im.filter(ImageFilter.BoxBlur(random.uniform(0,blur)))
        #Random Color  = 1.5
        pil_im = ImageEnhance.Color(pil_im).enhance(random.uniform(0,color))
        #Random contrast  = 1.5
        pil_im = ImageEnhance.Contrast(pil_im).enhance(random.uniform(constrast_min,constrast_max))
        #Random Brightness  = 1.5
        pil_im = ImageEnhance.Brightness(pil_im).enhance(random.uniform(brightness_min,brightness_max))

        past_x = (random.randint(-200,200)+500)-int(rows/2)
        past_y = (random.randint(-200,200)+500)-int(cols/2)

        back_im.paste(pil_im,(past_x,past_y ),pil_im)

        id_past = 0
        past = ""

        for j in j_to:
                Margin_x = 0
                Margin_y = 0

                if j["rectanglelabels"][0] == "SIGNATURE":
                    Margin_y = 40 * (rows/rows_orig)

                pixel_x = (j["x"] / 100.0 * cols )+ past_x +Margin_x

                pixel_y = (j["y"] / 100.0 *  rows )+ past_y + Margin_y
                pixel_width = j["width"] / 100.0 * cols
                pixel_height = j["height"] / 100.0 * rows

                if past == j["rectanglelabels"][0]:
                    id_past +=1
                else:
                    id_past =0

                past = j["rectanglelabels"][0]

                value_rows = df_update[df_update["filename"] == file]
                value_rows = value_rows[value_rows["label"] == j["rectanglelabels"][0]]
                #val = value_rows["value"]
                value_rows = value_rows.reset_index(drop=True)

                if len(value_rows) !=0:
                    index_rows = value_rows["Unnamed: 0"][id_past]
                    df_update.at[index_rows,"x"] = pixel_x
                    df_update.at[index_rows,"y"] = pixel_y
                    df_update.at[index_rows,"w"] = pixel_width
                    df_update.at[index_rows,"h"] = pixel_height

        cv2_im_processed = np.array(back_im)
        cv2.imwrite(file,cv2_im_processed,[int(cv2.IMWRITE_JPEG_QUALITY), 80])


    df_update.to_excel("{0}_Noise.xlsx".format(args_Name_Gen_Data))


if __name__ == "__main__":
    main()
