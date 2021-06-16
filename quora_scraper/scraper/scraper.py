from selenium import webdriver 
from selenium.webdriver.common.keys import Keys
import pandas as pd
import time


class QuoraScraper:
    def __init__(self):
        self.driver = ''
        self.dataframe = ''
        self.credentials = {
            'email': '',
            'password': '',
        }
        self.questions = []
        self.answers = []

    def start_driver(self):
        self.driver = webdriver.Firefox(executable_path='/usr/local/bin/geckodriver')

    def close_driver(self):
        self.driver.close()

    def open_url(self, url):
        self.driver.get(url)

    def initialize_columns(self, columns):
        self.dataframe = pd.DataFrame(columns=columns)

    def set_credentials(self, email, password):
        self.credentials['email'] = email
        self.credentials['password'] = password

    def login(self):
        self.open_url('https://www.quora.com/')
        
        if(self.credentials['email'] and self.credentials['password']):
            
            email_element = self.driver.find_element_by_id('email')
            password_element = self.driver.find_element_by_id('password')
            
            email_element.send_keys(self.credentials['email'])
            password_element.send_keys(self.credentials['password'])
            
            password_element.send_keys(Keys.ENTER)
        else:
            print('Credentials not set')
            
            

    def search_for_query(self, query):
        search_container = self.driver.find_element_by_xpath("//div[@class='q-flex']")
        input_element = search_container.find_element_by_tag_name('input')
        input_element.send_keys(query)
        time.sleep(2)
        input_element.send_keys(Keys.ENTER)
    
    def get_href(self, questions):
        return list(map(lambda ques: ques.get_attribute('href'), questions))

    def get_text(self, questions):
        return list(map(lambda ques: ques.text, questions))
        
    def get_questions(self, n_questions):
        SCROLL_PAUSE_TIME = 1

        question_elements = self.driver.find_elements_by_xpath("//a[@class='q-box qu-cursor--pointer qu-hover--textDecoration--underline qu-userSelect--text']")
        while(len(question_elements) < n_questions):
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        
            time.sleep(SCROLL_PAUSE_TIME)
            question_elements = self.driver.find_elements_by_xpath("//a[@class='q-box qu-display--block qu-cursor--pointer qu-hover--textDecoration--underline Link___StyledBox-t2xg9c-0 roKEj']")
            
        question_elements = question_elements[:n_questions]
        question_links = self.get_href(question_elements)
        question_texts = self.get_text(question_elements)
        
        for link, text in zip(question_links, question_texts):
            self.questions.append({
                'link': link,
                'text': text
            })

    def open_details_for_each_answer(self):
        more_buttons = self.driver.find_elements_by_xpath("//span[@class='q-text qu-cursor--pointer qt_read_more qu-color--blue_dark qu-fontFamily--sans qu-hover--textDecoration--underline']")
        for button in more_buttons:
            if button.text == '(more)':
                while(True):
                    self.driver.execute_script("scrollBy(0, 500)")
                    try:
                        button.click()
                        break
                    except:
                        continue

    def scrape_answer(self, answer_element):
        answer = {}
        answer['views'] = answer_element.text.split('\n')[-4].split()[0]
        if(answer['views'] == 'Sponsored' or answer['views'] == 'More'):
            return 'Ad'
        answer['username'] = answer_element.text.split(',')[0].split('\n')[0]
        answer['upvoters'] = answer_element.text.split('\n')[-3]
        answer['date'] = ' '.join(answer_element.text.split('\n')[1].split()[1:]).split('·')[0]

        return answer

    def scrape_question_details(self, question, n_answers):
        self.open_url(question['link'])
        answers = self.driver.find_elements_by_xpath("//div[@class='CssComponent-sc-1oskqb9-0 cXjXFI']")[2:]
        time.sleep(5)
        previous_length = len(answers)
        while(previous_length < n_answers):
            self.driver.execute_script("scrollBy(0, 2000)")
            self.driver.execute_script("scrollBy(0, -200);")
            time.sleep(1)
        
            answers = self.driver.find_elements_by_xpath("//div[@class='CssComponent-sc-1oskqb9-0 cXjXFI']")[2:]
        
            if(previous_length == len(answers)):
                time.sleep(3)
                answers = self.driver.find_elements_by_xpath("//div[@class='CssComponent-sc-1oskqb9-0 cXjXFI']")[2:]
        
            previous_length = len(answers)

        self.open_details_for_each_answer()
        answers = self.driver.find_elements_by_xpath("//div[@class='CssComponent-sc-1oskqb9-0 cXjXFI']")[2:]
        answers = list(filter(lambda answer: answer != 'Ad', list(map(self.scrape_answer, answers))))[:n_answers]
        self.answers.append(answers)
        return answers


    def get_field(dictionary, field):
        return dictionary[field] or ""

    def add_to_dataframe(self, values):
        series = pd.Series(values, index=self.dataframe.columns)
        self.dataframe = self.dataframe.append(series, ignore_index=True)
        
    def store_data(self):
        columns = ['Question Text', 'Question Link', 'Answer 1 Views',
                'Answer 1 username', 'Answer 1 upvoters', 'Answer 1 date',
                'Answer 2 Views', 'Answer 2 username', 'Answer 2 upvoters', 
                'Answer 2 date', 'Answer 3 Views', 'Answer 3 username', 
                'Answer 3 upvoters', 'Answer 3 date',]
        self.initialize_columns(columns)
        
        
        for question, answers in zip(self.questions[:1], self.answers[:1]):
            values = [question['text'], question['link'], answers[0]['views'],
                    answers[0]['username'], answers[0]['upvoters'], answers[0]['date'], 
                    answers[1]['views'], answers[1]['username'], answers[1]['upvoters'], 
                    answers[1]['date'], answers[2]['views'], answers[2]['username'], 
                    answers[2]['upvoters'], answers[2]['date'],]
            
            self.add_to_dataframe(values)
            
        self.dataframe.to_excel('sample.xlsx')
    

if __name__ == "__main__":
    scraper = QuoraScraper()
    scraper.start_driver()
    username = "YOUR_USERNAME"
    password = "YOUR_PASSWORD"
    scraper.set_credentials(username, password)
    scraper.login()
    scraper.search_for_query('football')
    scraper.get_questions(34)
