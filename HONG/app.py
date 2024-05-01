# 필요한 모듈 임포트
from flask import Flask, render_template, request, redirect, url_for, session
import requests
from bs4 import BeautifulSoup

# Flask 애플리케이션 생성
app = Flask(__name__)
app.secret_key = "your_secret_key"  # 세션을 위한 시크릿 키 설정

# 사용자 데이터베이스
users = {
    'hong': 'password'
}

# 사용자가 게시한 게시물 수 저장
users_post = {
    'hong': ['stocks', 'sports']
}

# url = {
#     'stocks': 'https://search.naver.com/search.naver?ssc=tab.news.all&where=news&sm=tab_jum&query=%EC%A3%BC%EC%8B%9D',
#     'sports': 'https://search.naver.com/search.naver?ssc=tab.news.all&where=news&sm=tab_jum&query=%EC%95%BC%EA%B5%AC'
# }

# 웹사이트에서 공지사항을 크롤링하는 함수
def get_announcements(category):
    url = {
    'stocks': 'https://search.naver.com/search.naver?ssc=tab.news.all&where=news&sm=tab_jum&query=%EC%A3%BC%EC%8B%9D',
    'sports': 'https://search.naver.com/search.naver?ssc=tab.news.all&where=news&sm=tab_jum&query=%EC%95%BC%EA%B5%AC'
    }
    category_url = url[category]
    response = requests.get(category_url)
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    announcements = []
    links = soup.select(".news_tit")
    for link in links:
        title = link.text
        url = link.attrs['href']
        announcements.append({'title': title, 'url': url})
    return announcements

# 로그인 페이지
@app.route('/')
def login():
    if 'username' in session:
        return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/sign_up')
def sign_up():
    return render_template('sign_up.html')

# 회원가입 처리
@app.route('/sign_up', methods=['POST'])
def do_sign_up():
    username = request.form['username']
    password = request.form['password']
    users[username] = password
    return redirect(url_for('login'))

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
    return render_template('dashboard.html', username=session['username'], users_post=users_post)
# 선택 페이지(GET 요청)
@app.route('/select')
def select():
    if 'username' not in session:
        return redirect(url_for('login'))
    category = request.args.get('category')
    if category:
        announcements = get_announcements(category)
        return render_template('select.html', username=session['username'], category=category, announcements=announcements)
    else:
        return render_template('select.html', username=session['username'])

# 로그아웃 처리
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

# 애플리케이션 실행
if __name__ == '__main__':
    app.run(debug=True)
