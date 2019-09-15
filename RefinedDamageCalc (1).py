import numpy as np
import matplotlib.pyplot as plt
import xlrd as xl
import itertools as it
import time


def extract_data():
    data = 'VGSP.xlsx'  # load data from the excel sheet
    workbook = xl.open_workbook(data)
    worksheet = workbook.sheet_by_name("Hero Stats")  # Load data from diff worksheets
    ItemsWorksheet = workbook.sheet_by_name("Items")
    HeroNameList = []  # Creating lists to store data extracted from the Hero worksheet
    WPatLVL1 = []  # Weapon Power lvl.1
    WPatLVL12 = []  # Weapon Power Lvl.12
    AttackDelay = []
    AttackSpeedLVL12 = []  # Attack speed lvl.12
    AttackSpeedModifier = []  # Attack Speed Modifier
    AttackCooldown = []  # Attack Cooldown
    StutterStep = []  # Stutterstep bonus
    ItemNameList = []  # Creating lists to extract data from items worksheet
    ItemHealth = []  # Health provided by each item
    ItemArmour = []
    ItemWP = []
    ItemAttackspeed = []  # Attack speed
    ItemPierce = []  # Pierce
    ItemCriticalChance = []  # Critical Chance
    ItemCriticalDamage = []  # Critical Damage
    ItemLifesteal = []  # Life-steal
    ItemTotalItemCost = []  # Item TotalItemCost

    for i in range(36):  # Adding all the data to the lists
        dat = worksheet.cell_value(i + 1, 0)
        HeroNameList.append(dat)
        WPatLVL1.append(int(worksheet.cell_value(i + 1, 7)))
        WPatLVL12.append(int(worksheet.cell_value(i + 1, 8)))
        AttackDelay.append(worksheet.cell_value(i + 1, 12))
        AttackSpeedLVL12.append(worksheet.cell_value(i + 1, 10))
        AttackSpeedModifier.append(worksheet.cell_value(i + 1, 14))
        AttackCooldown.append(worksheet.cell_value(i + 1, 11))
        StutterStep.append(worksheet.cell_value(i + 1, 13))
    for i in range(69):
        ItemNameList.append(ItemsWorksheet.cell_value(i + 1, 0))
        ItemWP.append(ItemsWorksheet.cell_value(i + 1, 1))
        ItemArmour.append(ItemsWorksheet.cell_value(i + 1, 16))
        ItemAttackspeed.append(ItemsWorksheet.cell_value(i + 1, 4))
        ItemHealth.append(ItemsWorksheet.cell_value(i + 1, 17))
        ItemCriticalChance.append(ItemsWorksheet.cell_value(i + 1, 5))
        ItemCriticalDamage.append(ItemsWorksheet.cell_value(i + 1, 6))
        ItemPierce.append(ItemsWorksheet.cell_value(i + 1, 3))
        ItemLifesteal.append(ItemsWorksheet.cell_value(i + 1, 2))
        ItemTotalItemCost.append(ItemsWorksheet.cell_value(i + 1, 18))

    t1 = np.column_stack((WPatLVL1, WPatLVL12, AttackSpeedLVL12, AttackDelay, AttackSpeedModifier, AttackCooldown, StutterStep))  # Combined all Hero data into a matrix
    t1 = np.matrix(t1)
    HeroStats = t1.astype(float)  # Converted all data to float
    t2 = np.column_stack((ItemWP, ItemAttackspeed, ItemPierce, ItemCriticalDamage, ItemCriticalChance, ItemHealth, ItemArmour, ItemLifesteal, ItemTotalItemCost))  # Combined all Iteam data into a matrix
    t2 = np.matrix(t2)
    ItemStats = t2.astype(float)

    main(HeroStats, ItemStats, HeroNameList, ItemNameList)



def breaking_point(InitialHeroWP, WeaponPower, DamageDealt, CarryOverDamage, NumberofBPstacks, DmgReqForNextStack):

    if NumberofBPstacks <35:
        if DamageDealt < DmgReqForNextStack:
            CarryOverDamage = DamageDealt
        else:
            while DamageDealt >= DmgReqForNextStack:
                DamageDealt = DamageDealt - DmgReqForNextStack
                NumberofBPstacks += 1
                if NumberofBPstacks > 35:
                    NumberofBPstacks = 35
                    break
                DmgReqForNextStack = 100 + NumberofBPstacks * 10

            WeaponPower = InitialHeroWP + NumberofBPstacks * 5
            CarryOverDamage = DamageDealt

    UpdatedBPvalues = (WeaponPower, CarryOverDamage, NumberofBPstacks, DmgReqForNextStack)
    return UpdatedBPvalues


def damage_dealt(TotalHeroWeaponPower, TotalHeroPierce, TotalHeroCritChance, TotalHeroCritDamage, TargetArmor):

    DamageDealt = TotalHeroWeaponPower / (1 + (1 - TotalHeroPierce) * TargetArmor / 100)
    DamageDealt = TotalHeroCritChance * (DamageDealt + DamageDealt * TotalHeroCritDamage) + (1 - TotalHeroCritChance) * DamageDealt

    return DamageDealt



def ManualItems(ItemStats):

    Item1 = 0
    Item2 = 0
    Item3 = 0
    Item4 = 0
    Item5 = 0

    Item1 = int(input("Enter item 1: (Enter -1 when finished): "))
    if Item1 != -1:
        Item2 = int(input("Enter item 2: (Enter -1 when finished): "))
        if Item2 != -1:
            Item3 = int(input("Enter item 3: (Enter -1 when finished): "))
            if Item3 != -1:
                Item4 = int(input("Enter item 4: (Enter -1 when finished): "))
                if Item4 != -1:
                    Item5 = int(input("Enter item 5: (Enter -1 when finished): "))

    ItemBuild = (Item1, Item2, Item3, Item4, Item5)

    return ItemCalc(ItemStats, ItemBuild)


def AutoItems(ItemStats, NumberofSlots):

    AllBuilds = list(it.permutations([68, 8, 46, 50, 55, 61, 63, 60, 66, 31, 53, 39, 41, 59, 5, 45, 6], NumberofSlots))
    TotalItemsData = []
    for ItemBuild in AllBuilds:
        ItemData = ItemCalc(ItemStats, ItemBuild)
        TotalItemsData.append(ItemData)

    AutoData = (TotalItemsData, AllBuilds)
    return AutoData






def ItemCalc(ItemStats, ItemBuild):
    isBreakingPoint = 0
    isTensionBow = 0
    isBoneSaw = 0
    TotalItemWP = 0
    TotalItemAttackSpeed = 0
    TotalItemPierce = 0
    TotalItemCriticalDamage = 0
    TotalItemCriticalChance = 0
    TotalItemHealth = 0
    TotalItemArmor = 0
    TotalItemLifesteal = 0
    TotalItemCost = 0
    for ItemIndex in ItemBuild:  # Add all item stats together

        Index = ItemIndex  # int(input("Enter the items' Indexex one by one: (Enter -1 when done)"))
        if Index == 8:
            isBreakingPoint = 1
        if Index == 6:
            isBoneSaw = 1
        if Index == 60:
            isTensionBow = 1
        if Index == -1:
            break
        else:
            TotalItemWP = TotalItemWP + ItemStats[Index, 0]
            TotalItemAttackSpeed = TotalItemAttackSpeed + ItemStats[Index, 1]
            if ItemStats[Index, 2] > TotalItemPierce:
                TotalItemPierce = ItemStats[Index, 2]
            TotalItemCriticalDamage = TotalItemCriticalDamage + ItemStats[Index, 3]
            TotalItemCriticalChance = TotalItemCriticalChance + ItemStats[Index, 4]
            TotalItemHealth = TotalItemHealth + ItemStats[Index, 5]
            TotalItemArmor = TotalItemArmor + ItemStats[Index, 6]
            TotalItemCost = TotalItemCost + ItemStats[Index, 8]

            if ItemStats[Index, 7] > TotalItemLifesteal:
                TotalItemLifesteal = ItemStats[Index, 7]

    TotalItemData = (isBreakingPoint,
    isTensionBow,
    isBoneSaw,
    TotalItemWP,
    TotalItemAttackSpeed,
    TotalItemPierce,
    TotalItemCriticalDamage,
    TotalItemCriticalChance,
    TotalItemHealth,
    TotalItemArmor,
    TotalItemLifesteal,
    TotalItemCost)

    return TotalItemData



def Gwen(TotalHeroData, TotalItemData, TotalDummyData):

    isBreakingPoint = TotalItemData[0]
    isTensionBow = TotalItemData[1]
    isBoneSaw = TotalItemData[2]
    TotalItemWP = TotalItemData[3]
    TotalItemAttackSpeed = TotalItemData[4]
    TotalItemPierce = TotalItemData[5]
    TotalItemCriticalDamage = TotalItemData[6]
    TotalItemCriticalChance = TotalItemData[7]
    TotalItemHealth = TotalItemData[8]
    TotalItemArmor = TotalItemData[9]
    TotalItemLIfesteal = TotalItemData[10]
    TotalItemCost = TotalItemData[11]

    HeroName = TotalHeroData[0]
    Level = TotalHeroData[1]
    HeroBaseWP = TotalHeroData[2]
    HeroTotalWP = TotalHeroData[3]
    HeroTotalAttackSpeed = TotalHeroData[4]
    SecondsPerAttack = TotalHeroData[5]

    PerkSecondsPerAttack = 1.4 / (1 + TotalItemAttackSpeed)



    for isGwenPerk in (0,1):

        DummyHP = TotalDummyData[0]
        DummyArmor = TotalDummyData[1]

        NumberOfHits = 0
        TotalWP = HeroTotalWP
        TensionBowTime = 0
        CarryOverDamage = 0
        NumberofBPstacks = 0
        DmgReqForNextStack = 100
        NumberofBSstacks = 0

        while DummyHP > 0:

            AdditionalHeroWP = TotalWP - HeroBaseWP

            DamageDealt = damage_dealt(TotalWP, TotalItemPierce, TotalItemCriticalChance,TotalItemCriticalDamage, DummyArmor)

            if isGwenPerk == 1:
                GwenPerkBonus = 25 + 55 * (Level - 1)/11 + 0.4 * AdditionalHeroWP
                BonusDamageDealt = damage_dealt(GwenPerkBonus, TotalItemPierce, TotalItemCriticalChance,TotalItemCriticalDamage, DummyArmor)

                DamageDealt = DamageDealt + BonusDamageDealt

            if TensionBowTime >= 6:
                TensionBowTime = TensionBowTime - 6
                TensionBowBonus = 100 + 1 * AdditionalHeroWP
                BonusDamageDealt = damage_dealt(TensionBowBonus, TotalItemPierce, TotalItemCriticalChance,TotalItemCriticalDamage, DummyArmor)
                DamageDealt = DamageDealt + BonusDamageDealt

            if isBoneSaw == 1:
                if NumberofBSstacks < 4:
                    DummyArmor = 0.9 * DummyArmor
                    NumberofBSstacks = NumberofBSstacks + 1

            if isBreakingPoint != 0:

                UpdatedBPvalues = breaking_point(HeroTotalWP, TotalWP, DamageDealt, CarryOverDamage, NumberofBPstacks, DmgReqForNextStack)

                TotalWP = UpdatedBPvalues[0]
                CarryOverDamage = UpdatedBPvalues[1]
                NumberofBPstacks = UpdatedBPvalues[2]
                DmgReqForNextStack = UpdatedBPvalues[3]

            DummyHP = DummyHP - DamageDealt
            NumberOfHits = NumberOfHits + 1

            if isGwenPerk == 1:
                TensionBowTime += PerkSecondsPerAttack
            else:
                TensionBowTime += SecondsPerAttack

        if isGwenPerk == 1:
            PerkTimeToKill = PerkSecondsPerAttack * NumberOfHits
            #print(PerkSecondsPerAttack, NumberOfHits, 'perk')

        else:
            TimeToKill = SecondsPerAttack * NumberOfHits
           # print(SecondsPerAttack, NumberOfHits, 'noperk')

    if TimeToKill < PerkTimeToKill:
        KillData = ('%.3f' % TimeToKill, 'Perk used')
    elif TimeToKill > PerkTimeToKill:
        KillData = ('%.3f' % PerkTimeToKill, 'Perk not used')
    else:
        KillData = ('%.3f' % TimeToKill, 'Same if perk used or not')

    return KillData


def Kinetic(TotalHeroData, TotalItemData, TotalDummyData):
    isBreakingPoint = TotalItemData[0]
    isTensionBow = TotalItemData[1]
    isBoneSaw = TotalItemData[2]
    TotalItemWP = TotalItemData[3]
    TotalItemAttackSpeed = TotalItemData[4]
    TotalItemPierce = TotalItemData[5]
    TotalItemCriticalDamage = TotalItemData[6]
    TotalItemCriticalChance = TotalItemData[7]
    TotalItemHealth = TotalItemData[8]
    TotalItemArmor = TotalItemData[9]
    TotalItemLIfesteal = TotalItemData[10]
    TotalItemCost = TotalItemData[11]

    HeroName = TotalHeroData[0]
    Level = TotalHeroData[1]
    HeroBaseWP = TotalHeroData[2]
    HeroTotalWP = TotalHeroData[3]
    HeroTotalAttackSpeed = TotalHeroData[4]
    SecondsPerAttack = TotalHeroData[5]

    DummyHP = TotalDummyData[0]
    DummyArmor = TotalDummyData[1]

    NumberOfHits = 0
    TotalWP = HeroTotalWP
    TensionBowTime = 6
    CarryOverDamage = 0
    NumberofBPstacks = 0
    DmgReqForNextStack = 100
    NumberofBSstacks = 0

    KineStacks = 4

    while DummyHP > 0:

        AdditionalHeroWP = TotalWP - HeroBaseWP


        DamageDealt = damage_dealt(TotalWP, TotalItemPierce, TotalItemCriticalChance, TotalItemCriticalDamage,
                                   DummyArmor)

        BonusDamageDealt = damage_dealt(4 + 11/11 * Level + 0.0625 * AdditionalHeroWP, TotalItemPierce, TotalItemCriticalChance, TotalItemCriticalDamage,
                                   DummyArmor)

        DamageDealt = DamageDealt + KineStacks * BonusDamageDealt

        if TensionBowTime >= 6:
            TensionBowTime = TensionBowTime - 6
            TensionBowBonus = 100 + 1 * AdditionalHeroWP
            BonusDamageDealt = damage_dealt(TensionBowBonus, TotalItemPierce, TotalItemCriticalChance,
                                            TotalItemCriticalDamage, DummyArmor)
            DamageDealt = DamageDealt + BonusDamageDealt

        if isBoneSaw == 1:
            if NumberofBSstacks < 4:
                DummyArmor = 0.9 * DummyArmor
                NumberofBSstacks = NumberofBSstacks + 1

        if isBreakingPoint != 0:
            UpdatedBPvalues = breaking_point(HeroTotalWP, TotalWP, DamageDealt, CarryOverDamage, NumberofBPstacks,
                                             DmgReqForNextStack)

            TotalWP = UpdatedBPvalues[0]
            CarryOverDamage = UpdatedBPvalues[1]
            NumberofBPstacks = UpdatedBPvalues[2]
            DmgReqForNextStack = UpdatedBPvalues[3]

        DummyHP = DummyHP - DamageDealt
        NumberOfHits = NumberOfHits + 1

        TensionBowTime += SecondsPerAttack



    TimeToKill = SecondsPerAttack * NumberOfHits
    KillData = ('%.3f' % TimeToKill, 'Perk used')
    return KillData


def Baron(TotalHeroData, TotalItemData, TotalDummyData):
    isBreakingPoint = TotalItemData[0]
    isTensionBow = TotalItemData[1]
    isBoneSaw = TotalItemData[2]
    TotalItemWP = TotalItemData[3]
    TotalItemAttackSpeed = TotalItemData[4]
    TotalItemPierce = TotalItemData[5]
    TotalItemCriticalDamage = TotalItemData[6]
    TotalItemCriticalChance = TotalItemData[7]
    TotalItemHealth = TotalItemData[8]
    TotalItemArmor = TotalItemData[9]
    TotalItemLIfesteal = TotalItemData[10]
    TotalItemCost = TotalItemData[11]

    HeroName = TotalHeroData[0]
    Level = TotalHeroData[1]
    HeroBaseWP = TotalHeroData[2]
    HeroTotalWP = TotalHeroData[3]
    HeroTotalAttackSpeed = TotalHeroData[4]
    SecondsPerAttack = TotalHeroData[5]

    DummyHP = TotalDummyData[0]
    DummyArmor = TotalDummyData[1]

    NumberOfHits = 0
    TotalWP = HeroTotalWP
    TensionBowTime = 6
    CarryOverDamage = 0
    NumberofBPstacks = 0
    DmgReqForNextStack = 100
    NumberofBSstacks = 0


    while DummyHP > 0:

        AdditionalHeroWP = TotalWP - HeroBaseWP

        DamageDealt = damage_dealt(1.25 * TotalWP, TotalItemPierce, TotalItemCriticalChance, TotalItemCriticalDamage,
                                   DummyArmor)

        if TensionBowTime >= 6:
            TensionBowTime = TensionBowTime - 6
            TensionBowBonus = 100 + 1 * AdditionalHeroWP
            BonusDamageDealt = damage_dealt(TensionBowBonus, TotalItemPierce, TotalItemCriticalChance,
                                            TotalItemCriticalDamage, DummyArmor)
            DamageDealt = DamageDealt + BonusDamageDealt

        if isBoneSaw == 1:
            if NumberofBSstacks < 4:
                DummyArmor = 0.9 * DummyArmor
                NumberofBSstacks = NumberofBSstacks + 1

        if isBreakingPoint != 0:
            UpdatedBPvalues = breaking_point(HeroTotalWP, TotalWP, DamageDealt, CarryOverDamage, NumberofBPstacks,
                                             DmgReqForNextStack)

            TotalWP = UpdatedBPvalues[0]
            CarryOverDamage = UpdatedBPvalues[1]
            NumberofBPstacks = UpdatedBPvalues[2]
            DmgReqForNextStack = UpdatedBPvalues[3]

        DummyHP = DummyHP - DamageDealt
        NumberOfHits = NumberOfHits + 1

        TensionBowTime += SecondsPerAttack

    TimeToKill = SecondsPerAttack * NumberOfHits
    KillData = ('%.3f' % TimeToKill, 'Perk used')
    return KillData



def initial_calcs(TotalItemData, WPatLVL1, WPatLVL12, AttackSpeedLVL12 ,AttackDelay ,AttackSpeedModifier, AttackCooldown,StutterStep, Level, HeroName):
    HeroBaseWP = WPatLVL1 + (WPatLVL12 - WPatLVL1) / 11 * (Level - 1)
    HeroBaseAttackSpeed = 1 + (AttackSpeedLVL12 - 1) / 11 * (Level - 1)
    isBreakingPoint = TotalItemData[0]
    isTensionBow = TotalItemData[1]
    isBoneSaw = TotalItemData[2]
    TotalItemWP = TotalItemData[3]
    TotalItemAttackSpeed = TotalItemData[4]
    TotalItemPierce = TotalItemData[5]
    TotalItemCriticalDamage = TotalItemData[6]
    TotalItemCriticalChance = TotalItemData[7]
    TotalItemHealth = TotalItemData[8]
    TotalItemArmor = TotalItemData[9]
    TotalItemLIfesteal = TotalItemData[10]
    TotalItemCost = TotalItemData[11]

    SecondsPerAttack = 1 / (1 / (
                (AttackCooldown + AttackDelay) / ((TotalItemAttackSpeed * AttackSpeedModifier) + HeroBaseAttackSpeed)))
    #print(SecondsPerAttack, 'SecondsperAttack')
    HeroTotalWP = HeroBaseWP + TotalItemWP
    HeroTotalAttackSpeed = HeroBaseAttackSpeed + TotalItemAttackSpeed

    TotalHeroData = (HeroName, Level, HeroBaseWP, HeroTotalWP, HeroTotalAttackSpeed, SecondsPerAttack)

    return TotalHeroData


def main(HeroStats, ItemStats, HeroNameList, ItemNameList):
    for count in range(68):
        print(count, "-", ItemNameList[count])
    HeroName = input('\nEnter the name of the hero: ')
    Level = int(input('Enter the level: '))


    for i in range(38):
        if HeroNameList[i] == HeroName:
            break

    WPatLVL1 = HeroStats[i, 0]
    WPatLVL12 = HeroStats[i, 1]
    AttackSpeedLVL12 = HeroStats[i, 2]
    AttackDelay = HeroStats[i, 3]
    AttackSpeedModifier = HeroStats[i, 4]
    AttackCooldown = HeroStats[i, 5]
    StutterStep = HeroStats[i, 6]
    HeroIndex = i
    choice = int(input('Enter 1 for  manual Build compare: \nEnter 2 to find the build with the least time to kill: '))

    if choice == 1:
        NumberOfBuilds = int(input('Enter number of builds that you want to test: "'))

        for count in range(NumberOfBuilds):

            TotalItemData = ManualItems(ItemStats)
            TotalHeroData = initial_calcs(TotalItemData, WPatLVL1, WPatLVL12, AttackSpeedLVL12, AttackDelay, AttackSpeedModifier, AttackCooldown, StutterStep, Level, HeroName)

            DummyHP = 2000
            DummyArmor = 100
            TotalDummyData = (DummyHP, DummyArmor)

            if HeroName == 'Baron':
                KillData = Baron(TotalHeroData, TotalItemData, TotalDummyData)
                print(KillData)

            if HeroName == 'Gwen':
                KillData = Gwen(TotalHeroData, TotalItemData, TotalDummyData)
                print(KillData)

            if HeroName == 'Kinetic':
                KillData = Kinetic(TotalHeroData, TotalItemData, TotalDummyData)
                print(KillData)



    elif choice ==2:
        NumberofSlots = int(input('Enter the number of slots: '))
        start = time.time()
        AutoData = AutoItems(ItemStats, NumberofSlots)
        AllBuildsData = AutoData[0]
        AllBuilds = AutoData[1]
        mid = time.time()
        count = 0
        PerkUsage = []
        TimeToKillList = []
        for TotalItemData in AllBuildsData:
            TotalHeroData = initial_calcs(TotalItemData, WPatLVL1, WPatLVL12, AttackSpeedLVL12 ,AttackDelay ,AttackSpeedModifier, AttackCooldown,StutterStep, Level, HeroName)

            DummyHP = 2000
            DummyArmor = 100
            TotalDummyData = (DummyHP, DummyArmor)

            if HeroName == 'Gwen':

                KillData = Gwen(TotalHeroData, TotalItemData, TotalDummyData)
                PerkUsage.append(KillData[1])
                TimeToKillList.append(KillData[0])
        IndexMin = TimeToKillList.index(min(TimeToKillList))

        LeastTTKbuild = (AllBuilds[IndexMin], TimeToKillList[IndexMin], PerkUsage[IndexMin])
        print(LeastTTKbuild)
        end = time.time()

extract_data()

#following fragment is code for killdata without perk
#def hero_name(TotalHeroData, TotalItemData, TotalDummyData):
    # isBreakingPoint = TotalItemData[0]
    # isTensionBow = TotalItemData[1]
    # isBoneSaw = TotalItemData[2]
    # TotalItemWP = TotalItemData[3]
    # TotalItemAttackSpeed = TotalItemData[4]
    # TotalItemPierce = TotalItemData[5]
    # TotalItemCriticalDamage = TotalItemData[6]
    # TotalItemCriticalChance = TotalItemData[7]
    # TotalItemHealth = TotalItemData[8]
    # TotalItemArmor = TotalItemData[9]
    # TotalItemLIfesteal = TotalItemData[10]
    # TotalItemCost = TotalItemData[11]
    #
    # HeroName = TotalHeroData[0]
    # Level = TotalHeroData[1]
    # HeroBaseWP = TotalHeroData[2]
    # HeroTotalWP = TotalHeroData[3]
    # HeroTotalAttackSpeed = TotalHeroData[4]
    # SecondsPerAttack = TotalHeroData[5]
    #
    # DummyHP = TotalDummyData[0]
    # DummyArmor = TotalDummyData[1]
    #
    # NumberOfHits = 0
    # TotalWP = HeroTotalWP
    # TensionBowTime = 6
    # CarryOverDamage = 0
    # NumberofBPstacks = 0
    # DmgReqForNextStack = 100
    # NumberofBSstacks = 0
    #
    # while DummyHP > 0:
    #
    #     AdditionalHeroWP = TotalWP - HeroBaseWP
    #
    #     DamageDealt = damage_dealt(TotalWP, TotalItemPierce, TotalItemCriticalChance, TotalItemCriticalDamage,
    #                                DummyArmor)
    #
    #     if TensionBowTime >= 6:
    #         TensionBowTime = TensionBowTime - 6
    #         TensionBowBonus = 100 + 1 * AdditionalHeroWP
    #         BonusDamageDealt = damage_dealt(TensionBowBonus, TotalItemPierce, TotalItemCriticalChance,
    #                                         TotalItemCriticalDamage, DummyArmor)
    #         DamageDealt = DamageDealt + BonusDamageDealt
    #
    #     if isBoneSaw == 1:
    #         if NumberofBSstacks < 4:
    #             DummyArmor = 0.9 * DummyArmor
    #             NumberofBSstacks = NumberofBSstacks + 1
    #
    #     if isBreakingPoint != 0:
    #         UpdatedBPvalues = breaking_point(HeroTotalWP, TotalWP, DamageDealt, CarryOverDamage, NumberofBPstacks,
    #                                          DmgReqForNextStack)
    #
    #         TotalWP = UpdatedBPvalues[0]
    #         CarryOverDamage = UpdatedBPvalues[1]
    #         NumberofBPstacks = UpdatedBPvalues[2]
    #         DmgReqForNextStack = UpdatedBPvalues[3]
    #
    #     DummyHP = DummyHP - DamageDealt
    #     NumberOfHits = NumberOfHits + 1
    #
    #     TensionBowTime += SecondsPerAttack
    # TimeToKill = SecondsPerAttack * NumberOfHits
    # KillData = (TimeToKill, 'Perk used')
    # return KillData


