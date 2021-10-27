import math
def cutText(raw_text):
	#cut from <p> to </p>
	text = ""
	cut_result_start = raw_text.find("<p>")
	while cut_result_start != -1:
		cut_result_end = raw_text.find("</p>",cut_result_start)
		if cut_result_end == -1:
			break;#can't find </p>
		text = text + " " + raw_text[cut_result_start+3:cut_result_end-1]
		cut_result_start = raw_text.find("<p>",cut_result_end)
	return text
	
def stdWord(raw_word):
	return raw_word.lower()
	
def countWord(raw_text,word_TF_dict,word_IDF_dict):
	text = cutText(raw_text)
    #remove some common punctuations
	clearMark = ['/', '!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '_', '+', '[', ']', '{', '}', '|', ':', ';', '<', '>', ',', '.', '?', '\'', '\"']
	for mark in clearMark:
		text = text.replace(mark," ")
	words = text.split(" ")
	wordmark = {}# to mark the word first time exist in this article(to calculate IDF)
	wordCountAll = 0
	for raw_word in words:
		word = stdWord(raw_word)
		if word == "": # to avoid empty word
			continue
		wordCountAll = wordCountAll + 1
		if word not in wordmark:
			wordmark[word] = 0
			#add IDF
			if word in word_IDF_dict:
				word_IDF_dict[word] = word_IDF_dict[word] + 1
			else:
				word_IDF_dict[word] = 1
		#add TF
		if word in word_TF_dict:
			word_TF_dict[word] = word_TF_dict[word] + 1
		else:
			word_TF_dict[word] = 1
	return wordCountAll
			
		
@outputSchema("y:bag{t:tuple(Word:chararray, TFIDF:float)}") 	
def Cal_TFIDF(bag):
	count = 0
	list_posttext = []#To store all raw text
	for ele in bag:
		list_posttext.append(ele[0])
	outBag = []
	word_TF_dict = {}
	word_IDF_dict = {}
	word_TFIDF_dict = {}
	wordCountAll = 0
	#get TF and IDF from each article
	for text in list_posttext:
		wordCount = countWord(text,word_TF_dict,word_IDF_dict)
		wordCountAll = wordCountAll + wordCount
	#calculate TFIDF_value
	for e_word in word_IDF_dict.keys():
		if e_word not in word_TF_dict:# to avoid something wrong in countWord
			continue
		IDF_value = math.log((len(list_posttext)/word_IDF_dict[e_word]),10.0)
		TF_value = float(word_TF_dict[e_word])/float(wordCountAll)
		TFIDF_value = TF_value * IDF_value
		word_TFIDF_dict[e_word] = TFIDF_value
	sort_word_TFIDF_list=sorted(word_TFIDF_dict.items(),key = lambda word_TFIDF_dict:word_TFIDF_dict[1],reverse=True)
	countTop10 = 0
	for key,value in sort_word_TFIDF_list:
		countTop10 = countTop10 + 1
		if countTop10 > 10 :
			break;
		tuple = (key,value)
		outBag.append(tuple)
	return outBag