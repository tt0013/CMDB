#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:Yang Tian Qi

import re,os
import commands



with open('group.conf','r') as files:
    group = []
    for i in files:
        if re.search('FinanceCrs',i):
            lines = i.split("'")[1].replace(' or ',',').replace('S@','')
            group.append(lines)
    # print('\t'.join(group).replace('\t',',').strip())
    print('\t'.join(group).replace('\t',',').strip())
