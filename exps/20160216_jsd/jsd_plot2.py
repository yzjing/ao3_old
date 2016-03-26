import matplotlib.pyplot as plt

work_count = [4,
 225,
 235,
 210,
 309,
 364,
 604,
 462,
 319,
 443,
 432,
 401,
 515,
 561,
 600,
 854,
 699,
 1208,
 2446,
 2314,
 2615,
 3279,
 2525,
 3508,
 3794,
 2995,
 2587,
 2465,
 3044,
 3999,
 5224,
 4724,
 4332,
 4336,
 3986,
 4548,
 4710,
 2803,
 3603,
 4419,
 3444,
 6895,
 8196,
 7352,
 8865,
 8786,
 7390,
 5309,
 5721,
 5708,
 4137,
 4144,
 4027,
 4242,
 4098,
 3758,
 3603,
 3178,
 3353,
 2981,
 3268,
 2602,
 2392,
 2401,
 1915]

jsd = [(0.26061413508380532, 0.20670497370828259, 0.31213169091454107),
(0.30961156020117225, 0.30728714480999253, 0.31187179919134633),
(0.30878504820221253, 0.30635659852678465, 0.31118510669072158),
(0.30463239658381613, 0.30236136250936163, 0.30689306184394299),
(0.31961666459508298, 0.31712718698690456, 0.32233687265254379),
(0.33388124358214433, 0.33054223977713387, 0.33693934203306841),
(0.28704473519536139, 0.28406846813334063, 0.28988966054334048),
(0.31802523537802885, 0.315677517271434, 0.32042766120496535),
(0.30552512318942782, 0.30297367587228996, 0.3080258893127592),
(0.28764939912929943, 0.28505694553485905, 0.2899885915703746),
(0.30785741867512312, 0.30596903485073662, 0.30976447504020249),
(0.30716772607557724, 0.30487912548805846, 0.3094092304347793),
(0.30967419743954411, 0.30683311754906217, 0.31234967184325613),
(0.32612320546158913, 0.32352094453277297, 0.32862073571951234),
(0.31206785756206162, 0.30974974848935072, 0.31436481395622656),
(0.31385972029946735, 0.31013039792051034, 0.31729152117625337),
(0.31221875941719995, 0.30987427964991165, 0.31459733085323516),
(0.3086689604518949, 0.30578401138123595, 0.31178876785770887),
(0.33709130143106003, 0.33479897741861248, 0.33947128617753491),
(0.3260620260200649, 0.32379549938783642, 0.328539355473913),
(0.32055810356033076, 0.31784567492261895, 0.32300073527759249),
(0.29614646127875371, 0.29372436368119392, 0.29858503181556717),
(0.33347585414831654, 0.33118407536818756, 0.33578712559698676),
(0.30764716846079415, 0.30503290878508238, 0.31035613638869569),
(0.31041246485416302, 0.30775281901390583, 0.31298956757227858),
(0.3301359488621754, 0.32766578982927658, 0.33271937947860697),
(0.30571024759608206, 0.30364531996147592, 0.3080892734098854),
(0.31209644513204587, 0.30993421650423464, 0.3142537079818572),
(0.32514675634775797, 0.32265105611230488, 0.32774789887936495),
(0.33227251862383744, 0.32997276018762467, 0.33444265713292953),
(0.29877970753425082, 0.29645954470498748, 0.30106398966303588),
(0.32538209414008612, 0.32258575879404267, 0.32812065166197513),
(0.31729164876154736, 0.31529452209889985, 0.31930912882556284),
(0.31746849655464193, 0.31471916367777469, 0.32005945577321321),
(0.33177622450709282, 0.32942597843242649, 0.33433668542319311),
(0.31245640025092014, 0.31038831852314774, 0.31467971884785378),
(0.32410389916622706, 0.32179376280158317, 0.32625726641361413),
(0.30582627306965832, 0.3040724321423936, 0.3077327196197438),
(0.31947907708562834, 0.31708794007819263, 0.32186633814531412),
(0.31347936978589347, 0.31089108059813764, 0.31603616603103896),
(0.30821614928122898, 0.30611009725943134, 0.3102791361961163),
(0.3134070227631896, 0.31085523427032957, 0.31575103928503795),
(0.33293501444886053, 0.33081547328566574, 0.33513026585653133),
(0.32316674019513214, 0.32097341236235205, 0.3252948204760977),
(0.33519276767014772, 0.33274830406923567, 0.33756573709877813),
(0.33504435797868709, 0.33291186887853047, 0.33709916227186698),
(0.34189154869977484, 0.33954955385519203, 0.34415718195767275),
(0.30512980384934307, 0.30254164474746137, 0.30753606746410844),
(0.31681595573407528, 0.31481032912706008, 0.31893258642964861),
(0.32097564113594934, 0.31857985113339216, 0.32328465455524169),
(0.34196618926945249, 0.33963825237128858, 0.34411444754954557),
(0.3222677383126466, 0.31975031774421514, 0.32470538465624915),
(0.32761083004077107, 0.32521992180169962, 0.33004695058211353),
(0.32326654190294091, 0.32106156239431854, 0.32566697289672203),
(0.31378027557718413, 0.31133898235945884, 0.31612993594527616),
(0.33107208995034415, 0.32883259658416514, 0.33323464935328817),
(0.33547047619919207, 0.33330900379175876, 0.33769417042610839),
(0.32331680589991985, 0.32103183680431929, 0.32558573382870704),
(0.32926991003747164, 0.32721553967830924, 0.33149810880449881),
(0.33580896430845358, 0.3336464292756165, 0.33797998659501088),
(0.31628769760518366, 0.31354967890677132, 0.3185794719905321),
(0.3142166938220069, 0.31196529589813771, 0.31655372928951447),
(0.31683980999199951, 0.31413149826257464, 0.31952391059298513),
(0.34378186921213238, 0.3403769726635586, 0.34700484144786858),
(0.32772061118715518, 0.3243864125061508, 0.33106360492006798)]

x = work_count
y = [i[0] for i in jsd]

fig = plt.figure(figsize = (10, 7))
ax = fig.add_subplot(111)
ax.plot(y, c = 'r')
ax.plot([float(i)/10000 for i in x], c = 'b')
# plt.yscale('log')
plt.legend(['jsd', 'work count'], loc='upper left')

plt.show()