from flask import Flask, render_template, request, redirect, url_for, session
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)
app.secret_key = "your_secret_key"  # 세션을 위한 시크릿 키 설정

# 사용자 데이터베이스 (간단하게 사용자 정보를 저장하는 대신 실제 데이터베이스를 사용할 수 있습니다)
users = {
    'hong': 'password'
}

# 웹사이트에서 공지사항을 크롤링하는 함수
def get_announcements():
    url = 'https://search.naver.com/search.naver?ssc=tab.news.all&where=news&sm=tab_jum&query=%EC%95%BC%EA%B5%AC'  # 공지사항이 있는 웹페이지의 URL을 입력하세요
    response=requests.get(url)
    html = response.text

    soup=BeautifulSoup(html, 'html.parser')
    announcements = []
    links=soup.select(".news_tit") #결과 리스트
    for link in links:
        title = link.text # 태그 안에 텍스트 요소를 가져온다
        url = link.attrs['href'] #href의 속성값을 가져온다
        announcements.append({'title': title, 'url': url})
    
    return announcements

# 로그인 페이지
@app.route('/')
def login():
    if 'username' in session:
        return redirect(url_for('dashboard'))
    return render_template('login.html')

# 로그인 처리
@app.route('/', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    if username in users and users[username] == password:
        session['username'] = username
        return redirect(url_for('dashboard'))
    return 'Invalid username/password combination'

# 대시보드 페이지
@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    announcements = get_announcements()  # 공지사항을 가져옵니다.
    return render_template('dashboard.html', username=session['username'], announcements=announcements)

# 로그아웃 처리
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
