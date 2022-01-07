import re, os, collections, time, googletrans, langid

translator = googletrans.Translator()
alphabet = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'

def words(text):
    return re.findall('[0-z]+', text) 

def train(features):
    model = collections.defaultdict(lambda: 1)
    for f in features:
        model[f] += 1
    return model

dic = open('words.txt','r',encoding="utf-8")
NWORDS = train(words(dic.read()))

def edits1(word):
    n = len(word)
    return set([word[0:i]+word[i+1:] for i in range(n)] +                     # deletion
               [word[0:i]+word[i+1]+word[i]+word[i+2:] for i in range(n-1)] + # transposition
               [word[0:i]+c+word[i+1:] for i in range(n) for c in alphabet] + # alteration
               [word[0:i]+c+word[i:] for i in range(n+1) for c in alphabet])  # insertion

def known_edits2(word):
    return set(e2 for e1 in edits1(word) for e2 in edits1(e1) if e2 in NWORDS)

def known(words):
    return set(w for w in words if w in NWORDS)

def correct(word):
    candidates = known([word]) or known(edits1(word)) or known_edits2(word) or [word]
    return str(max(candidates, key=lambda w: NWORDS[w]))

def correct_all(word):
    candidates = known([word]) or known(edits1(word)) or known_edits2(word) or [word]
    return candidates

while True:
    print('')
    print('==================== 尋找單字 ====================')
    x = input('>>> ')
    if langid.classify(x)[0] != 'en':
        try:
            x = translator.translate(str(x), dest='en').text
            print('==================== 翻譯結果 ====================')
            print('>>> ' + str(x))
        except:
            pass
    else:
        pass
    start = time.time()
    x = x + ' '
    xl = []
    aw = []
    xw = ''
    dw = ''
    at = True
    for j in range(len(x)):
        if x[j] != ' ':
            xw = xw + xw.join(x[j])
        else:
            xl.append(xw)
            xw = ''
    for j in range(len(xl)):
        if correct(xl[j]) != 'n' and correct(xl[j]) != 's':
            dw = dw + correct(xl[j]) + ' '
            if len(xl) == 1:
                aw = correct_all(xl[j])
            else:
                at = False
    try:
        twd = translator.translate(dw, dest='zh-tw').text
        print('==================== 相似結果 ====================')
        print('>>> ' + str(dw) + '' + str(twd))
        if at:
            print('==================== 更多結果 ====================')
            for j in aw:
                twd = translator.translate(j, dest='zh-tw').text
                print('>>> ' + str(j) + ' ' + str(twd))
    except:
        print('==================== 相似結果 ====================')
        print('>>> ' + str(dw))
        if at:
            print('==================== 更多結果 ====================')
            for j in aw:
                print('>>> ' + str(j))
    end = time.time()
    print('==================================================')
    print('耗費時間: '+str(end - start)+' 秒')
    print('==================================================')
    print(input('按 Enter 鍵返回'))
    os.system('cls')
        
