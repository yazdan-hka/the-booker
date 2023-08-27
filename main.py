from selenium import webdriver
from selenium.webdriver.common.by import By
import sqlite3
from time import sleep
from selenium.webdriver.common.keys import Keys


con = sqlite3.connect('words.db')
cur = con.cursor()


def SeeMeaningByWord(word, book):

	mean = cur.execute(f"SELECT m,p FROM {book} WHERE w =('{word}')")
	mean = mean.fetchall()
	for i in mean:
		for i in i:
			print(i)


def SeeMeaningById(id, book):

	mean = cur.execute(f"select w, m, p from {book} where id =({id})")
	mean = mean.fetchall()
	for i in mean:
	
		print(f'P.{i[2]}, {i[0]}\n______________\n{i[1]}')


def SeeMeaningByBook(book):

	mean = cur.execute(f"select id, w, p from {book}")
	mean = mean.fetchall()
	for i in mean:
	
		print(f'{i[0]}\tP.{i[2]}\t{i[1]}')

	i = input('\nChoose:\n\n\n1. See Meaning By Id\n2. Replace A Word\n3. Exit\n>>')

	if i == "1":
		i = input('enter the id:\n>>')

		SeeMeaningById(i,book)

	elif i == '2':
		i = input('enter the id:\n>>')
		word = input('enter the new word:\n>>')

		ReplaceWordById(i, word, book)

	elif i == '3':
		main()

	main()

def SeeMeaningByPage(page, book):

    mean = cur.execute(f"select id, w, p from {book} where p =({page})")
    mean = mean.fetchall()
    for i in mean:
	
        print(f'{i[0]}\tP.{i[2]}\t{i[1]}')

    i = input('\nChoose:\n\n\n1. See Meaning By Id\n2. Replace A Word\n3. Exit\n>>')

    if i == "1":

        i = input('enter the id:\n>>')

        SeeMeaningById(i,book)

    elif i == '2':
        while i != '0':
            i = input('enter the id:\n>>')
            word = input('enter the new word:\n>>')
            ReplaceWordById(i, word, book)

    elif i == '3':	
        main()

    main()

def ReplaceWordByPage(page, book):

	
	cur.execute(f"""UPDATE {book}
					SET m = 'None'
					WHERE p = {page};""")

	print(f'meanings of the page {page} are deleted.')
	con.commit()
	

def ReplaceWordById(id, word, book):

	try:
		cur.execute(f"""UPDATE {book}
						SET m = 'None',
						    w = '{word}'
						WHERE
						    id = {id};""")
		print(f'{word} has been updated successfully.')
		con.commit()
	except:
		print(f'error! {word} still exist.')

def DropTable(name):
	cur.execute(f"DROP TABLE {name}")


def CreateNewTable(name):
	cur.execute(f"""CREATE TABLE {name}(
	id integer PRIMARY KEY,
	w text NOT NULL,
	p integer DEFAULT(0),
	m text DEFAULT('None')
		)""")


def SeeTables():

	cur.execute('SELECT name from sqlite_master where type= "table"')
	return cur.fetchall()


def EnterNewWord(word, page, book):

	cur.execute(f"INSERT INTO {book} (w,p) VALUES ('{word}', {page})")
	con.commit()


def FindMeaning(wordORwords, book):

    
    print(wordORwords)
    
    path = r'C:\Users\cmos\Desktop\ColdRider\codes\The Booker\chromedriver.exe'
    driver = webdriver.Chrome(path)
    driver.implicitly_wait(10)
    words = []
    driver.get(f'https://www.vocabulary.com/dictionary/')
    b = 0

    for word in wordORwords:

        if b == 4 or 8 or 12 or 16 or 20 or 24 or 28 or 32:
            driver.get(f'https://www.vocabulary.com/dictionary/')

        print(word)
        search = driver.find_element(By.ID, "search")
        search.send_keys(word)
        sleep(8)
        search.send_keys(Keys.RETURN)
        sleep(8)

        meaning = driver.find_element(By.CLASS_NAME, 'short')
        details = driver.find_element(By.CLASS_NAME, 'long')

        res = f"\nExplanation:\n________________________\n{meaning.text}\n\nDetails:\n________________________\n{details.text}\n".replace('"', '^').replace("'", '`')
        print(res)

        search.clear()

        b = b + 1


        InsertMeaning(book, word, res)


def MeaningLessFinder(book):

    meaning_less_words = cur.execute(f"SELECT w FROM {book} WHERE m ='None'")
    words = []
    for i in meaning_less_words.fetchall():
        words.append(i[0])
    for i in words:
        try:
            words.remove('')
        except:
        	pass
    return words

def InsertMeaning(book, word, mean):

    cur.execute(f"""
        UPDATE {book} 
        SET m = '{mean}'
        WHERE w = '{word}'
        """)
    print(f'the meaning of {word} has been successfully inserted')

  
    con.commit()


def GetWord():

    print(SeeTables())

    print('\nthese are existing books.\n')
    book = input('enter one of the above books name or a new one:\n>>')
    page = ''
    word = ''

    books = str(SeeTables())

    if book in SeeTables():
        pass
    else:
        try:
            CreateNewTable(book)
            print(f'the book |{book}| has been added.')
        except:
            print(f'the book |{book}| is already added.')
    while True:

        word = input('Enter the word or words separated by ", ":\n>>')

        if ',' in word:
            word = word.replace(' ', '')
            words = word.split(',')
            print(words,type(words))

        if word == '0':
           break

        if words:
            page = input('Enter the page:\n>>')

            for i in words:

                try:
                    exist = cur.execute(f'SELECT * FROM {book} WHERE w={i}')
                except:
                	pass

                try:
                    if exist.fetchall():
                        print('word {i} is already in the table.')
                    pass
                except:
                    
                    EnterNewWord(i, page, book)
                    print(f'The word <{i}> on the -{page}- page, in |{book}| book, is saved.')

        else:

            page = input('enter the page:\n>>')
            EnterNewWord(word, page, book)
            print(f'The word <{word}> on the -{page}- page, in |{book}| book, is saved.')


def main():

    i = input('''\nChoose:\n
    1. Enter Words
    2. Find Current Words Meanings
    3. Search For Words
    4. See All The Words By Order
    5. See Words For A Specific Page
    6. See All Words Of A Book
    7. Delete A Book And All Its Contents
    8. Clear meanings of a page\n
____________________________________________________________\n
                !!! To Exit Enter ZERO !!!\n>>''').title()

    if i == '1':
        GetWord()
        main()
    elif i == '2':
        print(SeeTables())
        print('\nthese are existing books.\n')

        book = input('enter one of the above books name to insert the meaning to the meaning less words:\n>>')

        print(FindMeaning(MeaningLessFinder(book), book))
        main()
    elif i == '3':
        word = ''
        while True:

            word = input('\nenter the word:\n>>')
# here you can change the bellow variable to your book after compeleting a book.
            book = 'TheBook'
            if word == '0':
                break
            else:
                SeeMeaningByWord(word, book)
        main()

    elif i == '4':
        print('enter words')
        main()



    elif i == '5':

        print(SeeTables())

        print('\nthese are existing books.\n')

        book = input('enter one of the above books name:\n>>')
        page = input('enter the page:\n>>')


        SeeMeaningByPage(page,book)
        main()

    elif i == '6':

        print(SeeTables())

        print('\nthese are existing books.\n')

        book = input('enter one of the above books name:\n>>')

        SeeMeaningByBook(book)
        main()

    elif i == '7':

        print(SeeTables())
        print('\nthese are existing books.\n')

        book = input('enter one of the above books name:\n>>')

        DropTable(book)
        main()

    elif i == '8':

        print(SeeTables())

        book = input('these are the books. enter the name of your preferred book\n>>')
        ReplaceWordByPage(input('enter the page\n>>').title(), book)
        main()

    elif i == '0':
        exit()

    else:
        input('?')
        main()

main()
con.close()



















