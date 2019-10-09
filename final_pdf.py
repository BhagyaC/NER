from pdf2txt import call

result = call()

#result.split(",")
print("calling results")
for line in result:
    print("line:::::::::::::::::::::",line[0])