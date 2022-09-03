from PyQt5.QtWidgets import QApplication
from veri_cekme_2 import veri_cekme
import sys



# tabloda güncelle buton tabloda değiştir.

app=QApplication([])

kullanicilar=veri_cekme()
kullanicilar.show()


app.exec_()