# import library
from flask import Flask, render_template, request
from modules.tokopedia import Tokopedia


# data dummy
dataDummy=[['https://www.lazada.co.id/products/lampu-motor-h4-headlight-led-hs1-6w-6500k-1-pcs-lampu-motor-led-variasi-depan-costum-proji-super-terang-tahan-lama-i1258130229-s2127146926.html?search=1',
  'Lampu Motor H4 Headlight LED Hs1 6W 6500K 1 PCS, Lampu motor led variasi depan costum proji super terang tahan lama',
  '47500',
  ['1', '0', '0', '0', '0']],
 ['https://www.lazada.co.id/products/cod-sepasang-lampu-led-t10-mobil-motor-rgb-plus-remote-16-warna-lampu-led-motor-lampu-led-mobil-lampu-led-lampu-led-t10-remote-wireless-rgb-lampu-kota-senja-motor-mobil-dengan-remot-control-universal-isi-2-i1068348059-s1657028393.html?search=1',
  'COD - SEPASANG LAMPU LED T10 MOBIL MOTOR RGB PLUS REMOTE 16 WARNA / LAMPU LED MOTOR / LAMPU LED MOBIL / LAMPU LED / LAMPU LED T10 REMOTE WIRELESS RGB LAMPU KOTA SENJA MOTOR MOBIL DENGAN REMOT CONTROL UNIVERSAL ISI 2',
  '14800',
  ['8', '0', '0', '0', '0']],
 ['https://www.lazada.co.id/products/lampu-depan-led-lampu-utama-h6-cahaya-putih-de-biru-motor-matic-bebek-i1230532552-s2028896504.html?search=1',
  'Lampu Depan LED Lampu Utama H6 Cahaya Putih DE Biru Motor Matic Bebek',
  '38500',
  ['1', '0', '0', '0', '0']],
 ['https://www.lazada.co.id/products/lampu-utama-projie-bulat-biru-rainbow-merah-proji-35inc-i1222936211-s2001390368.html?search=1',
  'Lampu utama projie BULAT BIRU rainbow merah proji 3.5INC',
  '75000',
  ['2', '0', '0', '0', '0']],
 ['https://www.lazada.co.id/products/lampu-led-t10-senja-rgb-strobe-flash-mobil-motor-gel-jelly-red-blue-i1208736708-s1954152882.html?search=1',
  'Lampu LED T10 Senja RGB Strobe Flash Mobil Motor Gel Jelly Red Blue',
  '12000',
  ['5', '0', '0', '0', '0']],
 ['https://www.lazada.co.id/products/lampu-led-mata-elang-motor-dan-mobil-2-pcs-i1245266445-s2075102749.html?search=1',
  'lampu LED mata elang motor dan mobil 2 pcs',
  '16500',
  ['3', '0', '0', '0', '0']],
 ['https://www.lazada.co.id/products/lampu-depan-led-lampu-utama-h6-cahaya-putih-motor-matic-bebek-i1230572209-s2028882546.html?search=1',
  'Lampu Depan LED Lampu Utama H6 Cahaya Putih Motor Matic Bebek',
  '34000',
  ['2', '0', '0', '0', '0']],
 ['https://www.lazada.co.id/products/lampu-senja-2-warna-led-t10-2-warna-r213-i1163226078-s1834394740.html?search=1',
  'Lampu senja 2 Warna Led T10 2 Warna R213',
  '20855',
  ['1', '0', '0', '0', '0']],
 ['https://www.lazada.co.id/products/paket-ganteng-rx-king-biyangkerok-lampu-depan-6-mata-berikut-breket-plus-kumis-berikut-breket-i1221848679-s1997992102.html?search=1',
  'paket ganteng rx king biyangkerok lampu depan 6 mata berikut breket plus kumis berikut breket',
  '220000',
  ['1', '0', '0', '0', '0']],
 ['https://www.lazada.co.id/products/led-lampu-depan-led-lampu-utama-model-h6-cahaya-putih-2-sisi-devil-eyes-biru-motor-matic-bebek-i1250302580-s2093400749.html?search=1',
  'LED Lampu Depan LED Lampu Utama model H6 Cahaya Putih 2 sisi Devil Eyes Biru Motor Matic Bebek',
  '38500',
  ['1', '0', '0', '0', '0']]]

app=Flask(__name__,template_folder='page')



@app.route('/',methods=['GET','POST'])
def home():
  

  selectProxy="option1"
  if request.method == 'POST':
      barang=request.form['barang']
      selectProxy = request.form['inlineRadioOptions']
      print(selectProxy)
      return render_template('index.html',proxy=selectProxy,dataTokopedia=dataDummy,dataBukalapak=dataDummy,dataLazada=dataDummy)
  return render_template('index.html',proxy=selectProxy,dataTokopedia=dataDummy,dataBukalapak=dataDummy,dataLazada=dataDummy)
app.run(debug=True)