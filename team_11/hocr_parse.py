#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import hocr_parser.parser as parser
import json
import csv
from shapely.geometry.polygon import Polygon
from shapely.geometry import Point

class boxing:
    def __init__(self, name, pt0, pt1, page, tp):
        self.name = name
        self.pt0 = pt0
        self.pt1 = pt1
        self.page = page
        self.tp = tp
    def __gt__(self, other):
        if self.page > other.page:
            return True
        return False

syntax = "/Users/kim-li/Documents/CityU-Hackathon-2019/Testing/67/hocr/67-%d.hocr"

hocr_files = []     # every element represents a page
json_files = []     # every element represents a page

b_list = []


def generate_json(n, hocr_files, json_files):
    for i in range(3,n-3):
        hocr_file = syntax % i
        hocr_files.append(hocr_file)
        
    for hocr_file in hocr_files:
        #print(hocr_files.index(hocr_file))
        json_file = parser.hocr_to_json(hocr_file)
        json_file = json_file['responses'][0]['textAnnotations']
        del json_file[0]
        json_files.append(json_file)

def generate_blist(json_files, b_list):
    for i in range(len(json_files)):
        json_file = json_files[i]
        page = i+3
        for i in range(len(json_file)):
            e = json_file[i]
            name = e['description']
            pt0 = (e['boundingPoly']['vertices'][0]['x'], e['boundingPoly']['vertices'][0]['y'])
            pt1 = (e['boundingPoly']['vertices'][2]['x'], e['boundingPoly']['vertices'][2]['y'])
            b_list.append(boxing(name, pt0, pt1, page, -1))

def compare_poly(p1, p2, p1_, p2_):
    poly1 = Polygon([p1, (p1[0], p2[1]), p2, (p2[0], p1[1])])
    poly2 = Polygon([p1_, (p1_[0], p2_[1]), p2_, (p2_[0], p1_[1])])
    if poly1.intersects(poly2):
        PT1 = Point(p1)
        PT2 = Point(p2)
        PT1_ = Point(p1_)
        PT2_ = Point(p2_)
        if poly1.contains(PT1_) and poly1.contains(PT2_):
            return True
        elif poly2.contains(PT1) and poly2.contains(PT2):
            return True
        elif poly1.contains(PT1_):
            ul = (p1_[0], p1_[1])
            lr = (p2[0], p2[1])
            area1 = poly1.area
            area2 = poly2.area
            area = (lr[0]-ul[0])*(ul[1]-lr[1])
            if float(area)/float(area1)>=0.5 and float(area)/float(area2)>=0.5:
                return True
        elif poly2.contains(PT1_):
            ul = (p1[0], p1[1])
            lr = (p2_[0], p2_[1])
            area1 = poly1.area
            area2 = poly2.area
            area = (lr[0]-ul[0])*(ul[1]-lr[1])
            if float(area)/float(area1)>=0.5 and float(area)/float(area2)>=0.5:
                return True
        elif p1[0]>p1_[0]:
            ur = (p2_[0], p1_[1])
            ll = (p1[0], p2[1])
            area1 = poly1.area
            area2 = poly2.area
            area = (ur[0]-ll[0])*(ur[1]-ll[1])
            if float(area)/float(area1)>=0.5 and float(area)/float(area2)>=0.5:
                return True
        elif p1_[0]>p1[0]:
            ur = (p2[0], p1[1])
            ll = (p1_[0], p2_[1])
            area1 = poly1.area
            area2 = poly2.area
            area = (ur[0]-ll[0])*(ur[1]-ll[1])
            if float(area)/float(area1)>=0.5 and float(area)/float(area2)>=0.5:
                return True
        
    return False

def write_csv(csv_f, b_list):
    with open(csv_f, mode='w') as f:
        writer = csv.writer(f, delimiter=',')
        for e in b_list:
            writer.writerow([e.pt0[0], e.pt0[1], e.pt1[0], e.pt1[1], e.page, e.tp])

j_list = []

def read_json(jf):
    with open(jf) as load_f:
        d = json.load(load_f)
    load_f.close()
    d = d['pages']      # d is a list
    
    for e in d:
        if len(e['tags'])==0:
            continue
        for tag in e['tags']:
            if 'entityType' in tag:
                j_list.append(boxing("", tag['pt0'], tag['pt1'], e['pageId']+1, tag['entityType']))
            else:
                j_list.append(boxing("", tag['pt0'], tag['pt1'], e['pageId']+1, ""))
    return j_list

def toint(j_list, b_list):
    for i in range(len(j_list)):
        x1 = float(j_list[i].pt0[0])
        y1 = float(j_list[i].pt0[1])
        x2 = float(j_list[i].pt1[0])
        y2 = float(j_list[i].pt1[1])
        j_list[i].pt0 = (x1, y1)
        j_list[i].pt1 = (x2, y2)
    for i in range(len(b_list)):
        x1 = float(b_list[i].pt0[0])
        y1 = float(b_list[i].pt0[1])
        x2 = float(b_list[i].pt1[0])
        y2 = float(b_list[i].pt1[1])
        b_list[i].pt0 = (x1, y1)
        b_list[i].pt1 = (x2, y2)

def determine_type(j_list, b_list):
    #x = b_list[-1].page
    #y = j_list[-1].page
    for i in range(len(j_list)):
        for j in range(len(b_list)):
            e1 = j_list[i]
            e2 = b_list[j]
            if compare_poly(e1.pt0, e1.pt1, e2.pt0, e2.pt1)==True:
                if abs(b_list[j].page-j_list[i].page)<2:
                    b_list[j].tp = j_list[i].tp
                
    """
    i = 0
    j = 0
    while i<len(b_list) and j<len(j_list):
        if b_list[i].page<j_list[j].page:
            i += 1
        elif j<i:
            j += 1
        else:
            if compare_poly(b_list[i].pt0, b_list[i].pt1, j_list[j].pt0, j_list[j].pt1)==True:
                b_list[i].tp = j_list[i].tp
            i += 1
            j += 1
    """




