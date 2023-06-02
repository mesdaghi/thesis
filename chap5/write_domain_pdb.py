import shutil


pfam_domains={}
with open('./pfam_domains.txt') as f:
    content=f.readlines()
    for x in content:
        a,b=x.split('\t')
        pfam_domains[a]=b.strip()

sword_domains={}
with open('./sword_domains.txt') as f:
    content=f.readlines()
    for x in content:
        a=x.split('\t')
        sword_domains[a[0]]=[]
        b=a[1].split('*')
        for y in b:
            c=y.split('&')
            for z in c:
                if z=='' or z=='\n':
                    c.remove(z)
            if c != []:
                sword_domains[a[0]].append(c)

for x,y in sword_domains.items():
    b = list()
    for sublist in y:
        if sublist not in b:
            b.append(sublist)
    sword_domains[x]=b
    
cnt=0

final_bound={}
no_sword=[]
for x, y in pfam_domains.items():
    print(x + ' ' + y)
    start, finish = y.split('_')
    start = int(start)
    finish = int(finish)
    mid = int(start + ((finish-start)/2))
    temp_list=[]
    try:
        for i in sword_domains[x]:
            for j in i:
                s ,f = j.split('-')
                s=int(s)
                f=int(f)
                if ((s+mid<f) and s<start and f>finish)  and ((f-mid>s) and f>finish and s<start):
                    temp_list.append(j)                    
            
    except:
        print(temp_list)
    
    temp_dic={}
    for z in temp_list:
        a,b=z.split('-')
        a=int(a)
        b=int(b)
        length=b-a
        temp_dic[z]=length
    print(temp_dic)
    if temp_dic!={}:
        temp_dic = dict(sorted(temp_dic.items(), key=lambda item: item[1]))
        print(temp_dic)
        values_view = temp_dic.values()
        value_iterator = iter(values_view)
        first_value = next(value_iterator)
        for key, value in temp_dic.items():
            if first_value==value:
                print(key)
                final_bound[x]=key
    else:
        cnt+=1
        print(temp_dic)
        final_bound[x]=y
        a,b=x.split('_')
        no_sword.append(x)

print(final_bound)
print(len(final_bound))
print(cnt)


##################search for 301 that dont have sword domain
#seq_pfam=[]
#with open('/media/shah/sdb/db/pfam_sql/pfamA_reg_full_significant.txt') as f:
 #   content=f.readlines()
  #  for x in content:
   #     a =x.split('\t')
    #    temp=[]
     #   temp.append(a[1])
      #  temp.append(a[2])
       # seq_pfam.append(temp)

#cnt1=0
#pfam_tally={}
#for x in no_sword:
 #   cnt=0
  #  cnt1+=1
   # print(cnt1)
    #for y in seq_pfam:
     #   a,b=x.split('_')
      #  if b==y[1]:
       #     cnt+=1
   # pfam_tally[x]=cnt

#print(pfam_tally)
#print(len(pfam_tally))


pfam_tally={'PF12166_F6YWN4': 2, 'PF06454_Q8LMS2': 1, 'PF19149_A0A2K9R7H0': 1, 'PF17369_A0A1X7GDP1': 1, 'PF01496_G8BIQ0': 1, 'PF03303_Q96WS1': 1, 'PF11872_F6AF83': 1, 'PF12250_Q9CDA6': 2, 'PF16955_Q4J7V8': 1, 'PF15190_C3XRM4': 1, 'PF03825_P0AFF4': 2, 'PF10726_B0C2B3': 1, 'PF06836_A0A384KZH3': 1, 'PF02077_O15260': 1, 'PF11023_F2F9W4': 1, 'PF12534_W5MLZ0': 5, 'PF06198_Q9HDU1': 1, 'PF06781_X5DHK3': 1, 'PF17626_P0DJI5': 1, 'PF16972_Q29D71': 1, 'PF03653_Q9PGU6': 1, 'PF10319_Q966G6': 4, 'PF03616_A0A0A7S9K6': 1, 'PF14967_F7D286': 1, 'PF10762_J7TN87': 1, 'PF11289_D5HJV9': 1, 'PF10954_I2BBV9': 1, 'PF19217_U5KNA9': 28, 'PF16995_B2HR11': 4, 'PF14589_E4U7K8': 1, 'PF03817_B0UKK0': 1, 'PF07556_R6ETG2': 2, 'PF09742_H3AL71': 2, 'PF16962_R5YGF6': 1, 'PF16949_B4D3C0': 1, 'PF06358_Q65676': 1, 'PF11070_Q8XH88': 1, 'PF15113_A7SWN0': 1, 'PF11139_Q8YA43': 1, 'PF05297_P03230': 1, 'PF04791_A0A088ALU8': 1, 'PF10190_J9KAY3': 1, 'PF10125_Q8TY36': 2, 'PF12698_W7XGR7': 6, 'PF13321_Q81JV1': 4, 'PF10060_A9W9T1': 6, 'PF05640_I3KLE6': 1, 'PF11239_S5T3L8': 1, 'PF09679_D4EA35': 1, 'PF11038_Q4DPN1': 1, 'PF17582_F5H9Z4': 1, 'PF10812_B2HGW5': 1, 'PF10322_A8Y0S1': 2, 'PF12805_Q9PC07': 2, 'PF04173_F4B442': 2, 'PF07399_Q2IF09': 1, 'PF18179_A0A0U1QPG8': 1, 'PF04550_A6TE69': 1, 'PF05817_J9JRR5': 1, 'PF03155_N1JGC6': 1, 'PF17453_Q65LY8': 1, 'PF00798_P09991': 1, 'PF00822_P54851': 2, 'PF07415_P13285': 1, 'PF07123_J3L4K4': 1, 'PF16214_O95622': 4, 'PF05934_Q96S66': 1, 'PF05251_A0A0E9NAR6': 1, 'PF06808_Q2YRV7': 2, 'PF04123_D8J5V3': 1, 'PF10854_Q88426': 1, 'PF05038_G1N766': 1, 'PF12084_A8ANW3': 1, 'PF17461_O84008': 1, 'PF01741_C4LE79': 1, 'PF16185_H2XYB3': 3, 'PF06168_K9UYJ3': 1, 'PF17431_Q65IC5': 1, 'PF12670_R5U525': 1, 'PF03839_X2J9A4': 1, 'PF06900_Q2FX29': 1, 'PF15345_G3N8E7': 1, 'PF10255_A7AN02': 1, 'PF02447_Q65CW3': 2, 'PF07663_C9ACL7': 2, 'PF17368_A8FIP3': 1, 'PF03040_K9STU1': 1, 'PF04163_Q04746': 1, 'PF03596_Q8DNY0': 1, 'PF11460_K9VQE8': 1, 'PF10856_F7DFW2': 1, 'PF04846_Q77MT0': 1, 'PF07095_Q6CZP9': 1, 'PF00122_R7FRH4': 2, 'PF10951_W5WM19': 1, 'PF10943_O90305': 1, 'PF08285_R4XJ34': 1, 'PF04632_Q9I570': 2, 'PF16212_C3YZU3': 6, 'PF01005_P17763': 14, 'PF11127_A8ZZA8': 1, 'PF07086_B3RY75': 1, 'PF02544_P18405': 2, 'PF05758_Q2PMP0': 2, 'PF07214_P46119': 1, 'PF06638_H2YB63': 1, 'PF05805_A9UL52': 1, 'PF01002_P17763': 14, 'PF11377_H6RPW8': 1, 'PF06269_Q6TVM9': 1, 'PF12077_W5T927': 1, 'PF10439_B7GL22': 1, 'PF15824_G1U5F7': 1, 'PF17717_H2QJU6': 1, 'PF19213_B6VDX7': 21, 'PF06532_A0A0J1CMQ3': 1, 'PF04093_Q8DMY3': 1, 'PF09586_R6NFF7': 1, 'PF03408_Q87041': 1, 'PF01127_Q884A1': 1, 'PF16311_H3ATP7': 1, 'PF04842_F4IHL4': 1, 'PF09583_D8MLW1': 1, 'PF15968_P03759': 1, 'PF03125_Q9U2J1': 1, 'PF10643_B4S5H2': 1, 'PF04211_D3E047': 1, 'PF13303_R6RMS6': 1, 'PF05879_Q9UTE0': 3, 'PF04148_G3AMZ7': 1, 'PF05977_Q9I0E1': 3, 'PF10292_P91475': 2, 'PF06899_Q2NQC5': 1, 'PF07296_Q93GN8': 1, 'PF02364_I1HRP2': 3, 'PF07779_X1WW08': 1, 'PF12270_E1VW80': 1, 'PF17629_Q9ZE49': 1, 'PF17350_D5VS99': 1, 'PF10625_Q9KVR0': 1, 'PF11286_Q12QP7': 1, 'PF12297_W4YZ64': 1, 'PF07330_W0AEL0': 1, 'PF12292_B7VLK9': 1, 'PF11670_B9KIE7': 1, 'PF12430_A5DWL8': 2, 'PF11076_P0AAW5': 1, 'PF13962_U5FHP1': 4, 'PF19144_E4WMB3': 1, 'PF04971_Q2NSB8': 1, 'PF06149_R5XDB4': 1, 'PF07254_Q6D959': 1, 'PF17272_B6B472': 1, 'PF10710_Q8CUR3': 1, 'PF07242_A7GNK2': 1, 'PF07343_Q5VPL8': 1, 'PF04279_V6EVY8': 1, 'PF15940_D8MLZ8': 1, 'PF13779_Q2YR84': 1, 'PF07158_Q9L0A3': 2, 'PF01350_P17763': 14, 'PF08602_P25573': 2, 'PF05628_O50696': 1, 'PF05695_P61241': 2, 'PF01001_O41892': 10, 'PF11847_G0HCS2': 1, 'PF09971_L0JSQ2': 1, 'PF04483_A0A3N7FDD6': 1, 'PF10034_A7S2M0': 2, 'PF16357_Q87JU1': 2, 'PF03213_Q6TVR1': 1, 'PF00510_P00415': 1, 'PF05478_F1Q8X9': 1, 'PF01004_P03314': 14, 'PF17685_A0A3Q3FYV1': 1, 'PF04184_Q19337': 1, 'PF00695_Q76R62': 1, 'PF06374_G3I5D2': 1, 'PF06379_Q8ZIZ8': 1, 'PF03268_A0A2H2IE21': 2, 'PF11117_D6XW46': 1, 'PF07854_O29471': 1, 'PF14985_G1QCH6': 1, 'PF01528_P03215': 1, 'PF13063_A0A073JSG9': 1, 'PF05776_Q02267': 1, 'PF10624_Q93GM0': 1, 'PF15164_E2RD26': 1, 'PF17349_Q8EVY2': 1, 'PF05529_L8G5T8': 2, 'PF17394_I1YLT1': 1, 'PF17592_P20205': 1, 'PF12750_G2T5J5': 1, 'PF06151_P83294': 2, 'PF07584_V6F1P3': 2, 'PF05514_Q8H080': 1, 'PF17608_Q74KI2': 1, 'PF09928_Q6N1K0': 1, 'PF00876_G0NJM8': 2, 'PF10808_P64536': 1, 'PF03820_V3Z355': 1, 'PF15444_G1U6D9': 1, 'PF07271_P75330': 1, 'PF14068_X5A4Q2': 1, 'PF06450_Q87N04': 1, 'PF19218_U5KNA9': 28, 'PF10149_Q3U284': 1, 'PF02517_W6FH86': 1, 'PF13268_Q8E1R0': 1, 'PF08405_Q83883': 4, 'PF16933_H2J5Y7': 1, 'PF18969_A0A2A2Z2X6': 1, 'PF17009_I3EJ40': 1, 'PF06459_W5N4D0': 14, 'PF17597_P20200': 1, 'PF03699_E3GIB4': 1, 'PF05052_G8QMM0': 1, 'PF06139_P0C1T3': 1, 'PF12553_C4L9U4': 1, 'PF13705_A8XKW2': 4, 'PF17336_W8S7X7': 1, 'PF06653_B6IKT4': 1, 'PF05084_A0A074STF0': 1, 'PF17434_Q21AN7': 1, 'PF12794_H2IYY2': 3, 'PF17534_P47274': 1, 'PF02554_B9M2N4': 2, 'PF11916_Q7RCD2': 1, 'PF04976_P45002': 1, 'PF17343_G0MK63': 1, 'PF05313_Q08FN4': 1, 'PF13272_Q6D3G4': 1, 'PF03062_Q9VWV9': 1, 'PF04420_E9H4N0': 1, 'PF15156_I3JWS4': 1, 'PF17627_P0DJI4': 1, 'PF16504_A0A1L3KK13': 1, 'PF13515_R6QW63': 1, 'PF10151_W5NHM0': 1, 'PF11188_F6DQW6': 1, 'PF02723_Q0ZME5': 1, 'PF05602_W5M6Y6': 1, 'PF05620_Q0UEV9': 1, 'PF01349_P17763': 14, 'PF13965_F7FZS1': 1, 'PF07698_W6FW89': 3, 'PF17260_V4IYV3': 1, 'PF09622_K9W4S6': 1, 'PF13126_Q81M18': 1, 'PF04188_Q6NKT6': 1, 'PF02101_I3KGD9': 2, 'PF16965_Q6FQN7': 1, 'PF11982_A4XPJ8': 7, 'PF05767_Q070B5': 1, 'PF10337_Q4WU84': 3, 'PF17439_Q58007': 1, 'PF02109_O14238': 1, 'PF03916_P32709': 1, 'PF07349_Q672I0': 1, 'PF09786_M1AE63': 1, 'PF06066_D2TKF8': 1, 'PF01435_P44840': 1, 'PF11683_Q03TZ7': 1, 'PF15746_Q68D42': 1, 'PF17628_P0DJI3': 1, 'PF09490_D8IXQ2': 1, 'PF01452_A2T3Q0': 1, 'PF05513_A6TIT3': 1, 'PF03248_I3EIM1': 1, 'PF17113_I2BCQ6': 1, 'PF18893_C9RC03': 1, 'PF06728_A0A125YKP3': 1, 'PF04307_U5L8V8': 1, 'PF10953_A6T5A3': 1, 'PF01864_O28534': 2, 'PF09773_P0C152': 1, 'PF06790_Q8D2I9': 1, 'PF04982_L0E9T6': 1, 'PF10777_D3VC66': 1, 'PF01222_P32462': 2, 'PF09685_K9VKS1': 1, 'PF17259_Q65K27': 1, 'PF07260_F1Q528': 1, 'PF07402_Q9WT38': 1, 'PF05061_Q8V3J7': 1, 'PF15099_H9H1Z7': 1, 'PF15471_L5KIF5': 1, 'PF15033_D3ZM98': 1, 'PF13803_C7R2G7': 2, 'PF10267_F7CWT2': 1, 'PF01124_W6FP49': 1, 'PF06341_A0JQE6': 1, 'PF06795_P0DJZ1': 1, 'PF14798_U3K8Z0': 1, 'PF06837_Q9YX37': 1, 'PF11364_A4VTJ6': 1, 'PF08006_U5L5I2': 1, 'PF06161_Q9A1L7': 1, 'PF05296_G3V6Q7': 1, 'PF16165_W5MHL5': 8, 'PF00689_Q8RAK0': 6}

#print(len(pfam_tally))

for x, y in pfam_tally.items():
    if y==1:
        final_bound[x]='full'
    elif y>1:
        final_bound[x]=pfam_domains[x]

cnt=0
for x,y in final_bound.items():
    if y=='full':
        cnt+=1

print(final_bound)
print(cnt)


import re
#######create reent pdb files
cnt=0
for x,y in final_bound.items():
    a,b = x.split('_')

    pdb_code = '/media/shah/sdc/data/pfam_reloop_screen/pfam_models/' + a + '.pdb'


#######################################################
    
    if y != 'full':
        print(x + ' ' +y)
        try:
            c,d=y.split('_')
            e=int(d)-int(c) 
            window = [i for i in range(int(c), int(d)+1)]
        except:
            c,d=y.split('-')
            e=int(d)-int(c)+2
            window = [i for i in range(int(c),int(d)+1)]
            print(window)
        pdb_data = []
        try:
            with open(pdb_code) as file:
                for line in file:
                    pdb_data.append(line.strip())
        except:
            #cnt += 1
            print(x +','+ str(cnt)+ ' pdb file not found')


        coord_data=[]
        for z in pdb_data:
            z.split(' ')
            match = re.search('ATOM', z)
            if (match):
                coord_data.append(z)

        pdb_file = []
        for i in window:
            for res_number in coord_data:
                number = int(res_number[22:29].strip())
                if i == number:
                    pdb_file.append(res_number)

        with open('/media/shah/sdc/data/pfam_reloop_screen/all_v_all/pfam_models/' + x + '_' + c + '_' + d + '.pdb', "w") as f:
            for j in pdb_file:
                f.write(j + '\n')
                cnt+=1
                

#####################################

    elif y == 'full':
        try:
            shutil.copyfile(pdb_code,'/media/shah/sdc/data/pfam_reloop_screen/all_v_all/pfam_models/' + x + '.pdb')
        except:
            #cnt+=1
            print(x)

print(cnt)
