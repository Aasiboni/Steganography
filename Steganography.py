import SteganographyFunction as func
flag = 1
while flag:
    userSelect = raw_input('would you like to encode or decode?\n1 - for decode   2 - for encode\n')

    if userSelect != '2' and userSelect != '1':
        continue

    SelectedImage = func.filesList(userSelect)
    if userSelect == '1':
        func.decodeImage(SelectedImage)
        proceed = raw_input('would you like to continue encoding/decoding ?\n1 - for yes   2 - for no\n')
        if proceed == '1':
            continue
        else:
            flag = 0
    if userSelect == '2':
        secretMassage = raw_input('Enter your secret massage: ')
        func.encodeImage(secretMassage, SelectedImage)