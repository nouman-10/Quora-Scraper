from selenium import webdriver 
from selenium.webdriver.common.keys import Keys
import pandas as pd


class QuoraScraper:
    SCROLL_PAUSE_TIME = 0.5
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

    def open_url(url):
        self.driver.get(url)

    def initialize_columns(self, columns):
        self.dataframe = pd.DataFrame(columns=columns)

    def set_credentials(self, email, password):
        self.credentials.email = email
        self.credentials.password = password

    def login(self):
        self.driver.open_url('https://www.quora.com/')
        if(self.credentials['email'] and self.credentials['password']):
            email_element = self.driver.find_elements_by_name('email')[1]
            password_element = self.driver.find_elements_by_name('password')[1]
            email_element.send_keys(self.credentials['email'])
            password_element.send_keys(self.credentials['password'])
            button_element = self.driver.find_elements_by_xpath("//input[contains(@class, 'submit_button')]")[1]
            button_element.click()
        else:
            print('Credentials not set')

    def search_for_query(self, query):
        search_container = self.driver.find_element_by_xpath("//div[@class='q-flex']")
        input_element = search_container.find_element_by_tag_name('input')
        input_element.send_keys(query)
        input_element.send_keys(Keys.ENTER)

    def get_href(questions):
        return list(map(lambda ques: ques.get_attribute('href'), questions))

    def get_text(questions):
        return list(map(lambda ques: ques.text, questions))

    def get_questions(self, n_questions):
        question_elements = self.driver.find_elements_by_xpath("//a[@class='q-box qu-cursor--pointer qu-hover--textDecoration--underline qu-userSelect--text']")
        while(len(question_elements) < n_questions):
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        
            time.sleep(SCROLL_PAUSE_TIME)
            question_elements = self.driver.find_elements_by_xpath("//a[@class='q-box qu-cursor--pointer qu-hover--textDecoration--underline qu-userSelect--text']")
            
        question_elements = question_elements[:n_questions]
        question_links = get_href(question_elements)
        question_texts = get_texts(question_elements)

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

    def scrape_answer(answer_element):
        answer = {}
        answer['views'] = answer_element.text.split('\n')[-4].split()[0]
        if(answer['views'] == 'Sponsored' or answer['views'] == 'More'):
            return 'Ad'
        answer['username'] = answer_element.text.split(',')[0].split('\n')[0]
        answer['upvoters'] = answer_element.text.split('\n')[-3]
        answer['date'] = ' '.join(answer_element.text.split('\n')[1].split()[1:]).split('·')[0]
    
        return answer

    def scrape_question_details(self, question, n_answers):
        self.driver.get_url(question['link'])
        answers = self.driver.find_elements_by_xpath("//div[@class='CssComponent-sc-1oskqb9-0 cXjXFI']")[2:]
        previous_length = len(answers)
        while(previous_length < n_answers+int(0.3*n_answers):
            self.driver.execute_script("scrollBy(0, 2000)")
            self.driver.execute_script("scrollBy(0, -200);")
            time.sleep(1)

            answers = self.driver.find_elements_by_xpath("//div[@class='CssComponent-sc-1oskqb9-0 cXjXFI']")[2:]

            if(previous_length == len(answers)):
                time.sleep(3)
                answers = self.driver.find_elements_by_xpath("//div[@class='CssComponent-sc-1oskqb9-0 cXjXFI']")[2:]

            previous_length = len(answers)

        self.answers = list(filter(lambda answer: answer != 'Ad', list(map(scrape_answer, answers))))


if __name__ == "__main__":
    scraper = QuoraScraper()
    scraper.start_driver()
    username = "YOUR_USERNAME"
    password = "YOUR_PASSWORD"
    scraper.set_credentials(username, password)
    scraper.login()
    scraper.search_for_query('football')
    scraper.get_questions(34)
