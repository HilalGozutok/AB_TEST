###############################################
# FACEBOOK BIDDING AB TEST
###############################################

# Problem: average bidding maximum bidding'den daha mı fazla dönüşüm getirecek?
# Çözüm : AB testing


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def check_df(dataframe):
    print("##################### Shape #####################")
    print(dataframe.shape)
    print("##################### Types #####################")
    print(dataframe.dtypes)
    print("##################### Head #####################")
    print(dataframe.head(3))
    print("##################### Tail #####################")
    print(dataframe.tail(3))
    print("##################### NA #####################")
    print(dataframe.isnull().sum())
    print("##################### Quantiles #####################")
    print(dataframe.quantile([0, 0.05, 0.50, 0.95, 0.99, 1]).T)

control = pd.read_excel(r'C:\Users\LENOVO\PycharmProjects\DSMLBC4\HAFTA_05\ab_testing_data.xlsx',
                        sheet_name="Control Group")
check_df(control)


test = pd.read_excel(r'C:\Users\LENOVO\PycharmProjects\DSMLBC4\HAFTA_05\ab_testing_data.xlsx',
                        sheet_name="Test Group")
check_df(test)

# Değişkenler
# Impression : Gösterim
# Click : Tıklama
# Purchase : Satın Alma
# Earning : Kazanç

#Test grubu ve control grubunun betimsel istatistiklerine baktığımızda test grubunun
#Görüntülenme, satın alma ve kazanç noktasında matematiksel olarak önde olduğunu söylebiliriz.
#Bizim baza alacağımız purchase değişkeni için bu farkın şans eseri ortaya çıkıp çıkmadığını
#anlamamıza yardımcı olacak AB Testini uygulamalıyız.

#Varsayımlar
# 1. Normallik Varsayımı
# 2. Varyans Homojenliği

############################
# 1. Normallik Varsayımı
############################

# H0: Normal dağılım varsayımı sağlanmaktadır.
# H1: Normal dağılım varsayımı sağlanmamaktadır.

from scipy.stats import shapiro


test_istatistigi, pvalue = shapiro(control["Purchase"])
print('Test İstatistiği = %.4f, p-değeri = %.4f' % (test_istatistigi, pvalue))
# p-value < ise 0.05'ten HO RED.
# p-value < değilse 0.05 H0 REDDEDILEMEZ.
# ÇIKTI: Test İstatistiği = 0.9773, p-değeri = 0.5891,
# p-value < 0.05 olmadığı için H0 REDDEDİLEMEZ.


test_istatistigi, pvalue = shapiro(test["Purchase"])
print('Test İstatistiği = %.4f, p-değeri = %.4f' % (test_istatistigi, pvalue))
# p-value < ise 0.05'ten HO RED.
# p-value < değilse 0.05 H0 REDDEDILEMEZ.
# ÇIKTI: Test İstatistiği = 0.9589, p-değeri = 0.1541,
# p-value <0.05 olmadığı için H0 REDDEDİLEMEZ.

############################
#2. Varyans Homojenligi Varsayımı
############################
# H0: Varyanslar Homojendir
# H1: Varyanslar Homojen Değildir

from scipy import stats
stats.levene(control["Purchase"],test["Purchase"])

# p-value < ise 0.05'ten HO RED.
# p-value < değilse 0.05 H0 REDDEDILEMEZ.
# ÇIKTI: LeveneResult(statistic=2.6392694728747363, pvalue=0.10828588271874791),
#  p-value <0.05 olmadığı için H0 REDDEDİLEMEZ.


############################
# 2. Hipotezin Uygulanması
############################
# H0: M1 = M2 (... iki grup ortalamaları arasında ist ol.anl.fark yoktur.)
# H1: M1 != M2 (...vardır)

# Her iki varsayımda sağlandığı için bağımsız iki örneklem t testi (parametrik test) yapacağız.


test_istatistigi, pvalue = stats.ttest_ind(control["Purchase"],
                                           test["Purchase"],
                                           equal_var=True)

print('Test İstatistiği = %.4f, p-değeri = %.4f' % (test_istatistigi, pvalue))


# p-value < ise 0.05'ten HO RED.
# p-value < değilse 0.05 H0 REDDEDILEMEZ.
# ÇIKTI: Test İstatistiği = -0.9416, p-değeri = 0.3493
#  p-value <0.05 olmadığı için H0 REDDEDİLEMEZ.


# Yani diyebiliriz ki ; maximum bidding ve average bidding grupları arasında istatistiksel olarak anlamlı bir farklılık yoktur.
# Aralarındaki matematiksel farklılık şans eseri oluşmuştur.
