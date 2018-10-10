from selenium import webdriver
import time

def main():
    URL = 'https://datingproduction.com/en/en_profilesbg_onl_ofl_01/?cep=AQFcE2nmpoViLpEaAR0vuPevPdZvr5PLKd0mXATDcezPdd-gImtopKdlLnzTgv1vmrUVEGXLqzCTb-xm1c5OziigJ34Cheh7Ryf7Jsp39AI5cvau1K7N-nn5t0bUbvE7v8FFVVdpUAuwrBYRWW9gO7GfEgBscJr5LjfKO9-2kT43GYgrmj0Wrseek_5qCALBbBvaf8WY0WYU1Zwy3JouD2uEFgFMUf1Wx9g_bahGMvM8VnoqKlWBUfdMcgJnJAOrceZFCA-4qj3gjR5wrqc_XvMhL5blYvWM9qTGsxSzdTgm4HFM5kpaTTTqvxXLGFdv0VQOa-qxeNV2P_D4r8n-Qg&s1=36465&s2=171639&s3=2909&s4=&s5=96612&s6=%7Bs6%7D&s7=%7Bs7%7D&s8=%7Bs8%7D&s9=%7Bs9%7D&s10=7cda8192&cid=%5Btracking%5D'
    PROXY = "78.94.183.114:47538" # IP:PORT or HOST:PORT

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--proxy-server=%s' % PROXY)

    driver = webdriver.Chrome(options=chrome_options)
    driver.get(URL)
    driver.close()

if __name__ == '__main__':
    main()
