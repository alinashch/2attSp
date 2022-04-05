from flask import Flask, render_template, request, redirect, url_for
from data.processor import Processor
import json
from types import SimpleNamespace
import re
M=9

app = Flask(__name__)


@app.route('/')
def root():
    return '<h1>Hello World!</h1><p>Welcome to the world of Flask!</p>'


@app.route('/notfound')
def notfound():
    return render_template('notfound.html')


@app.route('/hello')
@app.route('/hello/<user>')
def hello_world(user=None):
    user = Processor().find_user(user)
    if user is None:
        return redirect(url_for('notfound'))
    return render_template('index.html', user=user)


@app.route('/api/hello/<user>')
def hello_json(user=None):
    user = user or 'Anonymous'
    return {
        "username": user,
        "message": 'hello world'
    }


@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    name = data.get('name')
    password = data.get('password')

    x = json.loads(request.data, object_hook=lambda d: SimpleNamespace(**d))
    print(x.name, x.password)

    return {
        "username": name,
        "hash" : hash(password),
        "message": 'Success'
    }, 200


def FindNumber(a):
    num = re.findall(r'\d+', a)
    q = [0] * (len(num) + 1)
    for i in range(0, len(num)):
        q[i] = int(num[i])
    a = 9
    arr = [0] * a
    for i in range(a):
        arr[i] = [0] * a
    for i in range(0, len(num) - 2):
        if i % 3 == 0:
            arr[q[i]][q[i + 1]] = int(q[i + 2])
    return arr


def puzzle(a):
    for i in range(M):
        for j in range(M):
            print(a[i][j], end=" ")
        print()


def solve(grid, row, col, num):
    for x in range(9):
        if grid[row][x] == num:
            return False

    for x in range(9):
        if grid[x][col] == num:
            return False

    startRow = row - row % 3
    startCol = col - col % 3
    for i in range(3):
        for j in range(3):
            if grid[i + startRow][j + startCol] == num:
                return False
    return True


def Suduko(grid, row, col):
    if (row == M - 1 and col == M):
        return True
    if col == M:
        row += 1
        col = 0
    if grid[row][col] > 0:
        return Suduko(grid, row, col + 1)
    for num in range(1, M + 1, 1):

        if solve(grid, row, col, num):

            grid[row][col] = num
            if Suduko(grid, row, col + 1):
                return True
        grid[row][col] = 0
    return False

@app.route('/search', methods=['GET', 'POST'])
def search_form():
    if request.method == 'POST':
        a=request.form.get('search')
        arr=FindNumber(a)
        print(arr)
        Suduko(arr, 0, 0)
        print(arr)
        return render_template('search.html', data=arr)
    return render_template('search.html')

if __name__ == '__main__':
    app.run()
